"""
AGENT 9: Inventory Management Agent
Deterministic mathematical inventory control and replenishment recommendations.
Formula: Reorder Point (ROP) = (Average Daily Demand * Supplier Lead Time) + Safety Stock.
Creates structured purchase recommendations for human approval.
PROHIBITION: Never automatically places purchase orders or transfers money.
"""

import math
from typing import Dict, Any, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent, DataType, ConfidenceLevel
from database.models import InventoryItem, Product, SupplierQuote, ApprovalRequest
from orchestrator.approval_engine import approval_engine


class InventoryManagementAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="InventoryManagementAgent",
            description="Monitors stock levels, calculates ROP and safety stock, drafts replenishment proposals"
        )

    def calculate_inventory_metrics(
        self,
        current_stock: int,
        reserved_stock: int,
        daily_sales_rate: float,
        lead_time_days: int,
        sales_std_dev: float = 2.0,
        service_level_z: float = 1.65,  # 95% service level
        moq: int = 50
    ) -> Dict[str, Any]:
        """
        Deterministic inventory math:
        - Available Stock = current_stock - reserved_stock
        - Days of Supply = Available Stock / daily_sales_rate
        - Safety Stock = Z * sqrt(Lead Time) * std_dev(Daily Demand)
        - Reorder Point (ROP) = (daily_sales_rate * lead_time_days) + safety_stock
        """
        available_stock = max(0, current_stock - reserved_stock)
        daily_sales = max(0.1, daily_sales_rate)
        lead_time = max(1, lead_time_days)

        days_of_supply = round(available_stock / daily_sales, 1)

        # Safety Stock formula accounting for demand variability
        safety_stock = math.ceil(service_level_z * math.sqrt(lead_time) * sales_std_dev)
        safety_stock = max(10, safety_stock)  # Baseline minimum floor

        lead_time_demand = math.ceil(daily_sales * lead_time)
        reorder_point = lead_time_demand + safety_stock

        needs_reorder = available_stock <= reorder_point

        # Recommended batch: coverage for lead time + 30 days buffer, rounded up to MOQ
        target_cycle_demand = math.ceil(daily_sales * (lead_time + 30))
        deficit = max(0, (reorder_point + target_cycle_demand) - available_stock)
        recommended_order_qty = math.ceil(deficit / moq) * moq if deficit > 0 else 0

        # Risk scoring (0.0 to 1.0)
        stockout_risk = 0.0
        if available_stock <= (safety_stock * 0.5):
            stockout_risk = 0.95
        elif available_stock <= safety_stock:
            stockout_risk = 0.80
        elif available_stock <= reorder_point:
            stockout_risk = 0.60
        else:
            stockout_risk = max(0.0, round(1.0 - (days_of_supply / 60.0), 2))

        excess_risk = 0.0
        if days_of_supply > 90.0:
            excess_risk = min(1.0, round((days_of_supply - 90.0) / 90.0, 2))

        return {
            "available_stock": available_stock,
            "days_of_supply": days_of_supply,
            "safety_stock": safety_stock,
            "lead_time_demand": lead_time_demand,
            "reorder_point": reorder_point,
            "needs_reorder": needs_reorder,
            "recommended_order_qty": recommended_order_qty,
            "stockout_risk": stockout_risk,
            "excess_risk": excess_risk
        }

    def run(self, db: Session, product_id: int, **kwargs) -> Dict[str, Any]:
        """Audit stock levels for product and generate approval request if ROP breached."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        inv = db.query(InventoryItem).filter(InventoryItem.product_id == product_id).first()
        if not inv:
            inv = InventoryItem(
                product_id=product_id,
                sku=product.sku or f"SKU-{product.id}",
                current_stock_units=50,
                reserved_stock_units=0,
                average_daily_sales=5.0,
                supplier_lead_time_days=10
            )
            db.add(inv)
            db.flush()

        quote = db.query(SupplierQuote).filter(
            SupplierQuote.product_id == product_id
        ).order_by(SupplierQuote.created_at.desc()).first()

        moq = quote.moq if quote else 50
        lead_time = quote.lead_time_days if quote else inv.supplier_lead_time_days

        metrics = self.calculate_inventory_metrics(
            current_stock=inv.current_stock_units,
            reserved_stock=inv.reserved_stock_units,
            daily_sales_rate=inv.average_daily_sales,
            lead_time_days=lead_time,
            moq=moq
        )

        # Update inventory record
        inv.days_of_supply_remaining = metrics["days_of_supply"]
        inv.safety_stock_units = metrics["safety_stock"]
        inv.reorder_point_units = metrics["reorder_point"]
        inv.recommended_reorder_qty = metrics["recommended_order_qty"]
        inv.stockout_risk_score = metrics["stockout_risk"]
        inv.excess_stock_risk_score = metrics["excess_risk"]
        inv.updated_at = datetime.utcnow()

        replenishment_request_id = None
        if metrics["needs_reorder"] and metrics["recommended_order_qty"] > 0:
            unit_cost = quote.quoted_price_inr if quote else 300.0
            supplier_name = quote.supplier_name if quote else "Unassigned Supplier"
            total_outlay = round(unit_cost * metrics["recommended_order_qty"], 2)

            # Check if pending approval request already exists to prevent duplicate actions
            existing_req = db.query(ApprovalRequest).filter(
                ApprovalRequest.action_type == "PURCHASE_INVENTORY",
                ApprovalRequest.entity_id == product_id,
                ApprovalRequest.status == "PENDING"
            ).first()

            if not existing_req:
                req = approval_engine.create_request(
                    db=db,
                    action_type="PURCHASE_INVENTORY",
                    entity_id=product_id,
                    title=f"Restock {metrics['recommended_order_qty']} units of {product.title[:60]}",
                    details={
                        "supplier": supplier_name,
                        "units": metrics["recommended_order_qty"],
                        "unit_price_inr": unit_cost,
                        "total_outlay_inr": total_outlay,
                        "current_stock": inv.current_stock_units,
                        "days_of_supply": metrics["days_of_supply"],
                        "reorder_point": metrics["reorder_point"],
                        "safety_stock": metrics["safety_stock"]
                    },
                    financial_impact_inr=total_outlay,
                    requested_by=f"AGENT:{self.agent_name}"
                )
                replenishment_request_id = req.id

        db.commit()

        self.log_action(
            db,
            action="CHECK_INVENTORY_HEALTH",
            resource_type="INVENTORY",
            resource_id=str(inv.id),
            details={
                "current_stock": inv.current_stock_units,
                "reorder_point": metrics["reorder_point"],
                "needs_reorder": metrics["needs_reorder"],
                "approval_request_id": replenishment_request_id
            }
        )

        return {
            "product_id": product_id,
            "sku": inv.sku,
            "metrics": metrics,
            "approval_request_id": replenishment_request_id
        }


inventory_agent = InventoryManagementAgent()
