"""
Automated Test Suite for Human-in-the-Loop Approval Workflow
Tests state transitions, rejection reasons, execution guards, and audit trails.
"""

import pytest
from database.connection import SyncSessionLocal, init_db
from database.models import Product, ApprovalRequest
from orchestrator.approval_engine import approval_engine
from orchestrator.emergency_stop import emergency_stop


@pytest.fixture(scope="module")
def db_session():
    init_db()
    session = SyncSessionLocal()
    yield session
    session.close()


def test_approval_lifecycle_and_state_transitions(db_session):
    """Verify approval creation, human sign-off, and execution."""
    emergency_stop.reset("TEST_RUNNER")

    # Create test product
    product = Product(
        title="Test Ergonomic Desk Lamp",
        category="Home & Kitchen",
        status="DISCOVERED"
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    # 1. Agent creates approval request -> Product transitions to AWAITING_APPROVAL
    req = approval_engine.create_request(
        db=db_session,
        action_type="PUBLISH_LISTING",
        entity_id=product.id,
        title="Publish listing for Test Ergonomic Desk Lamp",
        details={"sku": "TEST-LAMP-01", "price": 899.0},
        financial_impact_inr=0.0,
        requested_by="AGENT:ListingCreation"
    )

    db_session.refresh(product)
    assert req.status == "PENDING"
    assert product.status == "AWAITING_APPROVAL"

    # Cannot execute while still PENDING
    with pytest.raises(ValueError):
        approval_engine.mark_executed(db=db_session, request_id=req.id)

    # 2. Human Approves
    approved_req = approval_engine.approve_request(
        db=db_session,
        request_id=req.id,
        user_name="Abhishek (Admin)",
        decision_notes="Reviewed copy and compliance attributes. Ready to launch."
    )
    db_session.refresh(product)
    assert approved_req.status == "APPROVED"
    assert product.status == "APPROVED"

    # 3. Action executed
    executed_req = approval_engine.mark_executed(
        db=db_session,
        request_id=req.id,
        actor="SYSTEM:SP-API",
        execution_result={"feed_id": "FEED_987654321"}
    )
    db_session.refresh(product)
    assert executed_req.status == "EXECUTED"
    assert product.status == "ACTION_EXECUTED"


def test_rejection_workflow(db_session):
    """Verify rejection records mandatory reason."""
    product = Product(
        title="Test Defective Product",
        category="Consumer Electronics & Accessories",
        status="DISCOVERED"
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    req = approval_engine.create_request(
        db=db_session,
        action_type="PURCHASE_INVENTORY",
        entity_id=product.id,
        title="Purchase 200 units",
        details={"price": 400.0},
        financial_impact_inr=80000.0,
        requested_by="AGENT:Inventory"
    )

    # Reject without reason must fail
    with pytest.raises(ValueError):
        approval_engine.reject_request(db=db_session, request_id=req.id, user_name="Admin", reason="")

    # Reject with reason
    rejected_req = approval_engine.reject_request(
        db=db_session,
        request_id=req.id,
        user_name="Admin",
        reason="Supplier unverified and MOQ terms unfavorable"
    )
    db_session.refresh(product)
    assert rejected_req.status == "REJECTED"
    assert product.status == "REJECTED"
    assert "Supplier unverified" in product.rejection_reason
