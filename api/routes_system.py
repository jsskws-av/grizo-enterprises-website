"""
System Configuration, Configurable Business Rules, Audit Logs, and Scheduler Controls API
"""

from typing import List, Optional, Dict, Any
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.connection import get_sync_db
from database.models import AuditLog
from config.business_rules import (
    ScoringWeights, RejectionThresholds, OperationalGuardrails,
    DEFAULT_SCORING_WEIGHTS, DEFAULT_REJECTION_THRESHOLDS, DEFAULT_OPERATIONAL_GUARDRAILS
)
from orchestrator.scoring_engine import scoring_engine
from scheduler.daily_runner import daily_scheduler

router = APIRouter(prefix="/api/system", tags=["System"])


@router.get("/rules")
def get_business_rules():
    return {
        "scoring_weights": scoring_engine.weights.model_dump(),
        "rejection_thresholds": scoring_engine.thresholds.model_dump()
    }


@router.put("/rules/weights")
def update_scoring_weights(weights: ScoringWeights):
    # Verify sum approximately equals 1.0
    total = sum(weights.model_dump().values())
    if abs(total - 1.0) > 0.05:
        raise HTTPException(status_code=400, detail=f"Scoring weights must sum to approximately 1.0 (Current sum: {total:.2f})")
    scoring_engine.weights = weights
    return {"status": "SUCCESS", "updated_weights": weights.model_dump()}


@router.put("/rules/thresholds")
def update_rejection_thresholds(thresholds: RejectionThresholds):
    scoring_engine.thresholds = thresholds
    return {"status": "SUCCESS", "updated_thresholds": thresholds.model_dump()}


@router.get("/audit-logs")
def get_audit_logs(limit: int = 50):
    db = get_sync_db()
    try:
        logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
        return [
            {
                "id": l.id,
                "timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M:%S IST"),
                "actor": l.actor,
                "action": l.action,
                "resource_type": l.resource_type,
                "resource_id": l.resource_id,
                "details": json.loads(l.details_json) if l.details_json else {},
                "ip_address": l.ip_address
            }
            for l in logs
        ]
    finally:
        db.close()


@router.get("/scheduler")
def get_scheduler_status():
    return daily_scheduler.get_status()


@router.post("/scheduler/run-cycle")
def run_scheduler_cycle(cycle: str):
    cycle = cycle.upper()
    if cycle == "MORNING":
        return daily_scheduler.run_morning_cycle()
    elif cycle == "MIDDAY":
        return daily_scheduler.run_midday_cycle()
    elif cycle == "EVENING":
        return daily_scheduler.run_evening_cycle()
    else:
        raise HTTPException(status_code=400, detail=f"Unknown cycle '{cycle}'. Allowed: MORNING, MIDDAY, EVENING")
