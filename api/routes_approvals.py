"""
Human Approval Centre and Operational Emergency Stop API
"""

from typing import List, Optional, Dict, Any
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.connection import get_sync_db
from database.models import ApprovalRequest, Product
from orchestrator.approval_engine import approval_engine
from orchestrator.emergency_stop import emergency_stop
from integrations.amazon_sp_api import amazon_sp_api

router = APIRouter(prefix="/api/approvals", tags=["Approvals"])


class ApprovalDecisionRequest(BaseModel):
    user_name: str = "Abhishek (Admin)"
    notes: Optional[str] = None


class RejectionRequest(BaseModel):
    user_name: str = "Abhishek (Admin)"
    reason: str


class EmergencyStopTriggerRequest(BaseModel):
    triggered_by: str = "Abhishek (Admin)"
    reason: str = "User initiated Emergency Stop from Dashboard"


@router.get("")
def list_approvals(status: Optional[str] = None):
    db = get_sync_db()
    try:
        query = db.query(ApprovalRequest)
        if status:
            query = query.filter(ApprovalRequest.status == status)
        requests = query.order_by(ApprovalRequest.created_at.desc()).all()
        return [
            {
                "id": r.id,
                "action_type": r.action_type,
                "entity_type": r.entity_type,
                "entity_id": r.entity_id,
                "title": r.title,
                "details": json.loads(r.details_json) if r.details_json else {},
                "financial_impact_inr": r.financial_impact_inr,
                "status": r.status,
                "requested_by": r.requested_by,
                "decision_notes": r.decision_notes,
                "decided_at": r.decided_at.strftime("%Y-%m-%d %H:%M") if r.decided_at else None,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M")
            }
            for r in requests
        ]
    finally:
        db.close()


@router.post("/{request_id}/approve")
def approve_request(request_id: int, req: ApprovalDecisionRequest):
    db = get_sync_db()
    try:
        res = approval_engine.approve_request(
            db=db,
            request_id=request_id,
            user_name=req.user_name,
            decision_notes=req.notes
        )
        return {
            "status": "SUCCESS",
            "request_id": res.id,
            "approval_status": res.status,
            "message": f"Request #{request_id} successfully approved."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@router.post("/{request_id}/reject")
def reject_request(request_id: int, req: RejectionRequest):
    db = get_sync_db()
    try:
        res = approval_engine.reject_request(
            db=db,
            request_id=request_id,
            user_name=req.user_name,
            reason=req.reason
        )
        return {
            "status": "SUCCESS",
            "request_id": res.id,
            "approval_status": res.status,
            "message": f"Request #{request_id} rejected."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@router.post("/{request_id}/execute")
def execute_approved_action(request_id: int):
    """
    Execute an approved action.
    Enforces that emergency stop is inactive and checks marketplace integration status.
    """
    db = get_sync_db()
    try:
        emergency_stop.assert_can_write(f"Execute Request #{request_id}")

        req = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
        if not req or req.status != "APPROVED":
            raise HTTPException(status_code=400, detail="Action must be in APPROVED status before execution")

        details = json.loads(req.details_json) if req.details_json else {}

        # If publishing a listing
        if req.action_type == "PUBLISH_LISTING":
            sp_status = amazon_sp_api.get_connection_status()
            if not sp_status["connected"]:
                # Cannot publish without valid credentials; mark as simulated execution with clear warning
                simulated_result = {
                    "mode": "SIMULATED_EXECUTION",
                    "reason": "Amazon SP-API live credentials not configured. Verified draft stored locally."
                }
                res = approval_engine.mark_executed(db, request_id, actor="SYSTEM:Simulation", execution_result=simulated_result)
                return {
                    "status": "SIMULATED_EXECUTION",
                    "request_id": res.id,
                    "message": "Action marked executed in simulation mode (SP-API not connected)."
                }
            else:
                # Call live SP-API
                live_res = amazon_sp_api.publish_listing(details.get("sku", "UNKNOWN"), details)
                res = approval_engine.mark_executed(db, request_id, actor="SYSTEM:SP-API", execution_result=live_res)
                return {
                    "status": "LIVE_EXECUTED",
                    "request_id": res.id,
                    "result": live_res
                }
        else:
            # Generic execution (e.g. inventory restock marked)
            res = approval_engine.mark_executed(db, request_id, actor="SYSTEM:Operator", execution_result={"status": "order_logged"})
            return {"status": "EXECUTED", "request_id": res.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


# Emergency Stop Endpoints
@router.get("/emergency-stop/status")
def get_emergency_stop():
    return emergency_stop.get_status()


@router.post("/emergency-stop/trigger")
def trigger_emergency_stop(req: EmergencyStopTriggerRequest):
    return emergency_stop.trigger(triggered_by=req.triggered_by, reason=req.reason)


@router.post("/emergency-stop/reset")
def reset_emergency_stop(triggered_by: str = "Abhishek (Admin)"):
    return emergency_stop.reset(reset_by=triggered_by)
