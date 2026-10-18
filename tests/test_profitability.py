"""
Automated Test Suite for Amazon India Financial & Fee Calculations
Ensures 100% mathematical precision and zero fee calculation regressions.
"""

import pytest
from config.fee_schedules import (
    get_referral_fee, get_closing_fee, get_shipping_fee, AMAZON_FEE_GST_RATE
)
from agents.cost_profit_agent import cost_profit_agent


def test_referral_fee_slabs_home_and_kitchen():
    """Verify Home & Kitchen referral fee slabs."""
    # Slab 1: <= 300 @ 6%, min 5.0
    assert get_referral_fee("Home & Kitchen", 50.0) == 5.0    # Min fee applies
    assert get_referral_fee("Home & Kitchen", 250.0) == 15.0  # 6% of 250 = 15.0

    # Slab 2: 301 - 1000 @ 9.5%
    assert get_referral_fee("Home & Kitchen", 999.0) == 94.91 # 9.5% of 999 = 94.905 -> 94.91

    # Slab 3: > 1000 @ 12.5%
    assert get_referral_fee("Home & Kitchen", 2000.0) == 250.0 # 12.5% of 2000 = 250.0


def test_closing_fee_slabs():
    """Verify closing fee slabs across fulfilment channels."""
    # Easy Ship Slabs
    assert get_closing_fee("EASY_SHIP", 199.0) == 5.0
    assert get_closing_fee("EASY_SHIP", 450.0) == 9.0
    assert get_closing_fee("EASY_SHIP", 999.0) == 24.0
    assert get_closing_fee("EASY_SHIP", 1500.0) == 55.0

    # FBA Slabs
    assert get_closing_fee("FBA", 199.0) == 6.0
    assert get_closing_fee("FBA", 450.0) == 11.0
    assert get_closing_fee("FBA", 999.0) == 22.0
    assert get_closing_fee("FBA", 1500.0) == 38.0


def test_weight_handling_easy_ship_national():
    """Verify weight handling fee calculations for Easy Ship National zone."""
    # Under 500g: 74.0
    assert get_shipping_fee("EASY_SHIP", 450.0, "NATIONAL") == 74.0

    # Between 500g and 1000g: 74 + 25 = 99.0
    assert get_shipping_fee("EASY_SHIP", 850.0, "NATIONAL") == 99.0

    # 2100g: 74 + 25 + 3 * 33 = 198.0
    assert get_shipping_fee("EASY_SHIP", 2100.0, "NATIONAL") == 198.0


def test_unit_economics_deterministic_properties():
    """Verify unit economics math logic, GST, and scenario monotonicity."""
    res = cost_profit_agent.calculate_unit_economics(
        category="Home & Kitchen",
        selling_price=999.0,
        supplier_cost=320.0,
        package_weight_grams=2100.0,
        fulfilment_channel="EASY_SHIP",
        inbound_shipping_per_unit=35.0,
        packaging_labelling_cost=25.0,
        estimated_ad_cost_per_unit=60.0
    )

    # 1. Total Amazon Fees
    assert res["referral_fee"] == 94.91
    assert res["closing_fee"] == 24.0
    assert res["weight_handling_fee"] == 198.0
    assert res["total_amazon_fees"] == 316.91
    assert res["amazon_fee_gst"] == round(316.91 * 0.18, 2)  # 57.04

    # 2. Margin & Contribution must be mathematically consistent
    assert res["contribution_per_unit"] > res["net_operating_profit"]
    assert res["net_profit_margin_pct"] == round((res["net_operating_profit"] / 999.0) * 100.0, 2)

    # 3. Scenario Monotonicity: Optimistic > Base Case > Pessimistic
    assert res["optimistic_profit"] > res["net_operating_profit"]
    assert res["net_operating_profit"] > res["pessimistic_profit"]

    # 4. Break-even price and advertising limit must be reasonable
    assert res["breakeven_selling_price"] < 999.0
    assert res["max_affordable_ad_cost"] >= res["estimated_ad_cost_per_unit"]


def test_zero_or_negative_price_resilience():
    """Ensure calculator does not raise DivisionByZero on invalid price."""
    res = cost_profit_agent.calculate_unit_economics(
        category="Home & Kitchen",
        selling_price=0.0,
        supplier_cost=100.0,
        package_weight_grams=300.0
    )
    assert res["net_profit_margin_pct"] == 0.0
    assert res["net_operating_profit"] < 0
