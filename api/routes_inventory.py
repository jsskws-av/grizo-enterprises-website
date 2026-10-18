"""
Inventory Management, Stock Levels, and Replenishment Proposals API
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.connection import get_sync_db
from database.models import InventoryItem, Product
from agents.inventory_agent import inventory_agent

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


class UpdateStockRequest(BaseModel):
    current_stock_units: int
    reserved_stock_units: int = 0
    average_daily_sales: float = 5.0
    supplier_lead_time_days: int = 10


@router.get("")
def list_inventory():
    db = get_sync_db()
    try:
        items = db.query(InventoryItem).all()
        return [
            {
                "id": i.id,
                "product_id": i.product_id,
                "sku": i.sku,
                "title": i.product.title if i.product else i.sku,
                "category": i.product.category if i.product else "General",
                "current_stock": i.current_stock_units,
                "reserved_stock": i.reserved_stock_units,
                "available_stock": max(0, i.current_stock_units - i.reserved_stock_units),
                "daily_sales": i.average_daily_sales,
                "days_of_supply": i.days_of_supply_remaining,
                "lead_time_days": i.supplier_lead_time_days,
                "safety_stock": i.safety_stock_units,
                "reorder_point": i.reorder_point_units,
                "recommended_reorder_qty": i.recommended_reorder_qty,
                "stockout_risk": i.stockout_risk_score,
                "needs_reorder": i.current_stock_units <= i.reorder_point_units,
                "updated_at": i.updated_at.strftime("%Y-%m-%d %H:%M")
            }
            for i in items
        ]
    finally:
        db.close()


@router.post("/{product_id}/audit")
def audit_product_inventory(product_id: int):
    db = get_sync_db()
    try:
        return inventory_agent.run(db, product_id)
    finally:
        db.close()


@router.put("/{product_id}")
def update_stock(product_id: int, req: UpdateStockRequest):
    db = get_sync_db()
    try:
        inv = db.query(InventoryItem).filter(InventoryItem.product_id == product_id).first()
        if not inv:
            inv = InventoryItem(product_id=product_id, sku=f"SKU-{product_id}")
            db.add(inv)

        inv.current_stock_units = req.current_stock_units
        inv.reserved_stock_units = req.reserved_stock_units
        inv.average_daily_sales = req.average_daily_sales
        inv.supplier_lead_time_days = req.supplier_lead_time_days
        db.commit()

        # Recalculate
        return inventory_agent.run(db, product_id)
    finally:
        db.close()
