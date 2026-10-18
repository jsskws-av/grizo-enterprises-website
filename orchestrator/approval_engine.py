"""
Human-in-the-Loop Approval Centre & Permission State Machine
Enforces strict human governance over financially and publicly impactful decisions.
Workflow: DISCOVERED -> ANALYSED -> RISK_CHECKED -> AWAITING_APPROVAL -> APPROVED -> ACTION_EXECUTED -> VERIFIED
"""

from datetime import datetime
import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from database.models import ApprovalRequest, Product, AuditLog
from orchestrator.emergency_stop import emergency_stop

# Permitted actions that MUST be human-approved
MANDATORY_APPROVAL_ACTIONS = {
    "PURCHASE_INVENTORY",
    "PAY_SUPPLIER",
    "PUBLISH_LISTING",
    "CREATE_AD_CAMPAIGN",
    "INCREASE_AD_BUDGET",
    "CHANGE_PRICE",
    "DELETE_PRODUCT"
}

ALLOWED_STATUS_TRANSITIONS = {
    "PENDING": ["APPROVED", "REJECTED", "CANCELLED"],
    "APPROVED": ["EXECUTED", "CANCELLED"],
    "REJECTED": ["PENDING"],  # Resubmission
    "EXECUTED": ["VERIFIED"],
    "CANCELLED": []
}


class ApprovalEngine:
    @staticmethod
    def create_request(
        db: Session,
        action_type: str,
        entity_id: int,
        title: str,
        details: Dict[str, Any],
        financial_impact_inr: float = 0.0,
        requested_by: str = "AGENT",
        entity_type: str = "PRODUCT"
    ) -> ApprovalRequest:
        """Create a pending approval request that halts execution until human review."""
        if action_type not in MANDATORY_APPROVAL_ACTIONS:
            raise ValueError(f"Action '{action_type}' is not recognized as an approval action")

        req = ApprovalRequest(
            action_type=action_type,
            entity_type=entity_type,
            entity_id=entity_id,
            title=title,
            details_json=json.dumps(details),
            financial_impact_inr=financial_impact_inr,
            status="PENDING",
            requested_by=requested_by,
            created_at=datetime.utcnow()
        )
        db.add(req)

        # If it's a product, update product status to AWAITING_APPROVAL
        if entity_type == "PRODUCT":
            product = db.query(Product).filter(Product.id == entity_id).first()
            if product:
                product.status = "AWAITING_APPROVAL"

        # Audit log entry
        audit = AuditLog(
            actor=requested_by,
            action="REQUEST_APPROVAL",
            resource_type=entity_type,
            resource_id=str(entity_id),
            details_json=json.dumps({
                "action_type": action_type,
                "title": title,
                "financial_impact_inr": financial_impact_inr
            })
        )
        db.add(audit)
        db.commit()
        db.refresh(req)
        return req

    @staticmethod
    def approve_request(
        db: Session,
        request_id: int,
        user_name: str,
        decision_notes: Optional[str] = None
    ) -> ApprovalRequest:
        """Explicit human approval."""
        req = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
        if not req:
            raise ValueError(f"Approval request #{request_id} not found")

        if req.status != "PENDING":
            raise ValueError(f"Cannot approve request #{request_id} in status '{req.status}'")

        req.status = "APPROVED"
        req.decision_notes = decision_notes or f"Approved by {user_name}"
        req.decided_at = datetime.utcnow()

        if req.entity_type == "PRODUCT":
            product = db.query(Product).filter(Product.id == req.entity_id).first()
            if product:
                product.status = "APPROVED"

        audit = AuditLog(
            actor=user_name,
            action="APPROVE_REQUEST",
            resource_type=req.entity_type,
            resource_id=str(req.entity_id),
            details_json=json.dumps({"request_id": request_id, "action_type": req.action_type})
        )
        db.add(audit)
        db.commit()
        db.refresh(req)
        return req

    @staticmethod
    def reject_request(
        db: Session,
        request_id: int,
        user_name: str,
        reason: str
    ) -> ApprovalRequest:
        """Explicit human rejection."""
        if not reason:
            raise ValueError("Rejection reason is mandatory")

        req = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
        if not req:
            raise ValueError(f"Approval request #{request_id} not found")

        req.status = "REJECTED"
        req.decision_notes = f"Rejected by {user_name}: {reason}"
        req.decided_at = datetime.utcnow()

        if req.entity_type == "PRODUCT":
            product = db.query(Product).filter(Product.id == req.entity_id).first()
            if product:
                product.status = "REJECTED"
                product.rejection_reason = reason

        audit = AuditLog(
            actor=user_name,
            action="REJECT_REQUEST",
            resource_type=req.entity_type,
            resource_id=str(req.entity_id),
            details_json=json.dumps({"request_id": request_id, "reason": reason})
        )
        db.add(audit)
        db.commit()
        db.refresh(req)
        return req

    @staticmethod
    def mark_executed(
        db: Session,
        request_id: int,
        actor: str = "SYSTEM",
        execution_result: Optional[Dict[str, Any]] = None
    ) -> ApprovalRequest:
        """Mark an approved action as executed after external API call."""
        emergency_stop.assert_can_write(f"Execute Approval Request #{request_id}")

        req = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
        if not req or req.status != "APPROVED":
            raise ValueError(f"Request #{request_id} must be in APPROVED status before execution")

        req.status = "EXECUTED"

        if req.entity_type == "PRODUCT":
            product = db.query(Product).filter(Product.id == req.entity_id).first()
            if product:
                product.status = "ACTION_EXECUTED"

        audit = AuditLog(
            actor=actor,
            action="EXECUTE_APPROVED_ACTION",
            resource_type=req.entity_type,
            resource_id=str(req.entity_id),
            details_json=json.dumps(execution_result or {})
        )
        db.add(audit)
        db.commit()
        db.refresh(req)
        return req


approval_engine = ApprovalEngine()
