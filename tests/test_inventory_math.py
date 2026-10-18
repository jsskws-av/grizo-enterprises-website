"""
Automated Test Suite for Inventory Mathematics
Verifies Reorder Point (ROP = LeadTimeDemand + SafetyStock), Days of Supply,
and MOQ alignment.
"""

import pytest
from agents.inventory_agent import inventory_agent


def test_reorder_point_and_safety_stock_formula():
    """Verify that ROP = (daily_sales * lead_time) + safety_stock."""
    daily_sales = 10.0
    lead_time = 7
    metrics = inventory_agent.calculate_inventory_metrics(
        current_stock=150,
        reserved_stock=0,
        daily_sales_rate=daily_sales,
        lead_time_days=lead_time,
        sales_std_dev=2.0,
        service_level_z=1.65,
        moq=50
    )

    lead_time_demand = 10 * 7  # 70
    assert metrics["lead_time_demand"] == lead_time_demand
    assert metrics["safety_stock"] >= 10
    assert metrics["reorder_point"] == lead_time_demand + metrics["safety_stock"]
    assert metrics["days_of_supply"] == 15.0
    assert metrics["needs_reorder"] is False


def test_reorder_trigger_when_stock_below_rop():
    """Verify that needs_reorder triggers when available stock <= ROP."""
    metrics = inventory_agent.calculate_inventory_metrics(
        current_stock=40,
        reserved_stock=10,  # Available = 30
        daily_sales_rate=5.0,
        lead_time_days=10,
        moq=50
    )
    # Lead time demand = 50, safety stock >= 10 -> ROP >= 60
    # Available stock = 30 <= 60 -> needs_reorder must be True
    assert metrics["available_stock"] == 30
    assert metrics["needs_reorder"] is True
    assert metrics["recommended_order_qty"] % 50 == 0  # Multiple of MOQ
    assert metrics["recommended_order_qty"] > 0
    assert metrics["stockout_risk"] > 0.50
