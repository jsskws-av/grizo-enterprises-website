"""
AGENT 10: Price and Sales Optimisation Agent
Recommends profitable selling prices within configured minimum and maximum limits.
Guards against destructive price wars and enforces human approval for price revisions.
PROHIBITION: Never adjusts live marketplace prices outside user guardrails.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent, DataType, ConfidenceLevel
from database.models import Product, ProfitabilityAnalysis, MarketObservation, ApprovalRequest
from orchestrator.approval_engine import approval_engine
from config.business_rules import DEFAULT_OPERATIONAL_GUARDRAILS


class PriceAndSalesOptimisationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="PriceAndSalesOptimisationAgent",
            description="Recommends profitable selling prices within safety bounds and monitors buy-box dynamics"
        )

    def compute_optimal_price(
        self,
        current_price: float,
        breakeven_price: float,
        competitor_price: Optional[float],
        inventory_days_of_supply: float,
        min_margin_pct: float = 15.0
    ) -> Dict[str, Any]:
        """
        Calculates recommended price:
        - Floor: Breakeven price + minimum margin buffer
        - Ceil: +15% of current price
        - If excess stock (>60 days), slight discount (-3% to -5%) to boost sales velocity
        - If low stock (<15 days), slight premium (+3% to +5%) to preserve inventory and maximize profit
        """
        # Hard floor
        price_floor = round(breakeven_price * 1.15, 2)
        price_ceiling = round(current_price * 1.20, 2)

        target = current_price

        # Stock velocity balancing
        if inventory_days_of_supply > 60.0:
            target = max(price_floor, round(current_price * 0.95, 2))
            reason = "High inventory coverage (>60 days); recommending 5% price reduction to accelerate sales velocity."
        elif inventory_days_of_supply < 15.0 and inventory_days_of_supply > 0.0:
            target = min(price_ceiling, round(current_price * 1.05, 2))
            reason = "Low stock buffer (<15 days); recommending 5% price increase to capture higher margin."
        elif competitor_price and competitor_price < current_price:
            matched = max(price_floor, round(competitor_price, 2))
            if matched < current_price:
                target = matched
                reason = f"Matching observable competitor price (₹{competitor_price:.2f}) while maintaining margin floor (₹{price_floor:.2f})."
            else:
                reason = f"Competitor price (₹{competitor_price:.2f}) is below our safety floor (₹{price_floor:.2f}); refusing destructive price war."
        else:
            reason = "Current price is optimal and aligned with market demand."

        change_pct = round(((target - current_price) / current_price) * 100.0, 2) if current_price > 0 else 0.0

        return {
            "current_price": current_price,
            "recommended_price": target,
            "price_floor": price_floor,
            "price_ceiling": price_ceiling,
            "change_pct": change_pct,
            "reason": reason,
            "requires_human_approval": True
        }

    def run(self, db: Session, product_id: int, **kwargs) -> Dict[str, Any]:
        """Audit pricing and generate price change recommendation."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        obs = db.query(MarketObservation).filter(
            MarketObservation.product_id == product_id
        ).order_by(MarketObservation.observed_at.desc()).first()

        prof = db.query(ProfitabilityAnalysis).filter(
            ProfitabilityAnalysis.product_id == product_id
        ).first()

        current_price = prof.target_selling_price_inr if prof else (obs.selling_price_inr if obs else 599.0)
        breakeven = prof.breakeven_selling_price_inr if prof else round(current_price * 0.70, 2)
        comp_price = obs.selling_price_inr if obs and obs.selling_price_inr != current_price else None

        days_supply = product.inventory.days_of_supply_remaining if product.inventory else 30.0

        rec = self.compute_optimal_price(
            current_price=current_price,
            breakeven_price=breakeven,
            competitor_price=comp_price,
            inventory_days_of_supply=days_supply
        )

        approval_req_id = None
        if abs(rec["change_pct"]) >= 3.0:
            # Check existing request
            existing_req = db.query(ApprovalRequest).filter(
                ApprovalRequest.action_type == "CHANGE_PRICE",
                ApprovalRequest.entity_id == product_id,
                ApprovalRequest.status == "PENDING"
            ).first()

            if not existing_req:
                app_req = approval_engine.create_request(
                    db=db,
                    action_type="CHANGE_PRICE",
                    entity_id=product_id,
                    title=f"Update Price for {product.title[:50]} from ₹{current_price} to ₹{rec['recommended_price']}",
                    details=rec,
                    financial_impact_inr=round(rec["recommended_price"] - current_price, 2),
                    requested_by=f"AGENT:{self.agent_name}"
                )
                approval_req_id = app_req.id

        self.log_action(
            db,
            action="EVALUATE_PRICING",
            resource_type="PRODUCT",
            resource_id=str(product_id),
            details={"current": current_price, "recommended": rec["recommended_price"], "reason": rec["reason"]}
        )

        return {
            "product_id": product_id,
            "pricing_recommendation": rec,
            "approval_request_id": approval_req_id
        }


price_agent = PriceAndSalesOptimisationAgent()
