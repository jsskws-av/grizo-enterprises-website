"""
Interactive Profitability Calculator API
Allows interactive unit economics modeling and what-if scenario testing.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from agents.cost_profit_agent import cost_profit_agent

router = APIRouter(prefix="/api/calculator", tags=["Calculator"])


class CalculationRequest(BaseModel):
    category: str = "Home & Kitchen"
    selling_price: float = Field(..., ge=0.0)
    supplier_cost: float = Field(..., ge=0.0)
    package_weight_grams: float = Field(default=350.0, ge=50.0)
    fulfilment_channel: str = "EASY_SHIP"  # EASY_SHIP, FBA, SELF_SHIP
    shipping_zone: str = "NATIONAL"        # LOCAL, REGIONAL, NATIONAL
    inbound_shipping_per_unit: float = 20.0
    packaging_labelling_cost: float = 15.0
    estimated_ad_cost_per_unit: float = 40.0
    return_rate_pct: float = 5.0
    damaged_inventory_rate_pct: float = 1.5
    product_gst_rate_pct: float = 18.0
    moq: int = 50


@router.post("")
def calculate_economics(req: CalculationRequest) -> Dict[str, Any]:
    return cost_profit_agent.calculate_unit_economics(
        category=req.category,
        selling_price=req.selling_price,
        supplier_cost=req.supplier_cost,
        package_weight_grams=req.package_weight_grams,
        fulfilment_channel=req.fulfilment_channel,
        inbound_shipping_per_unit=req.inbound_shipping_per_unit,
        packaging_labelling_cost=req.packaging_labelling_cost,
        estimated_ad_cost_per_unit=req.estimated_ad_cost_per_unit,
        return_rate_pct=req.return_rate_pct,
        damaged_inventory_rate_pct=req.damaged_inventory_rate_pct,
        product_gst_rate_pct=req.product_gst_rate_pct,
        shipping_zone=req.shipping_zone,
        moq=req.moq
    )
