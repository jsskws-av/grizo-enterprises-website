"""
Automated Test Suite for Mandatory Rejection Gates
Ensures that a candidate failing ANY rejection rule (unverified supplier,
hazmat, low margin, fragile) is immediately rejected.
"""

import pytest
from database.connection import SyncSessionLocal, init_db
from database.models import Product, ProfitabilityAnalysis, SupplierQuote, ComplianceCheck, ProductScore
from orchestrator.scoring_engine import scoring_engine


@pytest.fixture(scope="module")
def db_session():
    init_db()
    session = SyncSessionLocal()
    yield session
    session.close()


def test_mandatory_rejection_on_sub_par_margin(db_session):
    """Product with net margin < 15% must be rejected regardless of high demand."""
    product = Product(
        title="Low Margin High Volume Item",
        category="Consumer Electronics & Accessories",
        status="DISCOVERED"
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    # Margin = 8.5% (Below 15% floor)
    prof = ProfitabilityAnalysis(
        product_id=product.id,
        target_selling_price_inr=500.0,
        supplier_cost_inr=350.0,
        referral_fee_inr=50.0,
        closing_fee_inr=15.0,
        weight_handling_fee_inr=74.0,
        amazon_fee_gst_inr=25.02,
        product_output_gst_inr=76.27,
        product_input_gst_credit_inr=53.39,
        net_gst_payable_inr=22.88,
        contribution_per_unit_inr=42.5,  # Below 50 floor
        net_operating_profit_inr=42.5,
        net_profit_margin_pct=8.5,
        roi_pct=12.1,
        optimistic_profit_inr=60.0,
        pessimistic_profit_inr=10.0,
        breakeven_selling_price_inr=480.0,
        max_affordable_ad_cost_inr=42.5,
        cash_required_initial_batch=35000.0
    )
    db_session.add(prof)

    sup = SupplierQuote(
        product_id=product.id,
        supplier_name="Verified Supplier Co.",
        quoted_price_inr=350.0,
        is_verified=True
    )
    db_session.add(sup)

    comp = ComplianceCheck(
        product_id=product.id,
        category_restricted=False,
        special_handling="STANDARD",
        fragility_tier=1
    )
    db_session.add(comp)
    db_session.commit()

    score = scoring_engine.score_product(db=db_session, product_id=product.id)

    db_session.refresh(product)
    assert score.rejection_gate_passed is False
    assert product.status == "REJECTED"
    assert "Net profit margin" in product.rejection_reason


def test_mandatory_rejection_on_hazmat_item(db_session):
    """Hazmat item must be immediately rejected."""
    product = Product(
        title="Flammable Chemical Solvent",
        category="Automotive Accessories",
        status="DISCOVERED"
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    comp = ComplianceCheck(
        product_id=product.id,
        category_restricted=True,
        special_handling="HAZMAT",
        fragility_tier=1
    )
    db_session.add(comp)
    db_session.commit()

    score = scoring_engine.score_product(db=db_session, product_id=product.id)

    db_session.refresh(product)
    assert score.rejection_gate_passed is False
    assert product.status == "REJECTED"
    assert "HAZMAT" in product.rejection_reason
