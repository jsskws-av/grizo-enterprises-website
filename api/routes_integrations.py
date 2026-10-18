"""
Integration Settings and Credential Vault API
Manages Amazon SP-API, Gemini AI, Telegram Bot, and Keepa API credentials with transparent status audits.
"""

from typing import List, Optional, Dict, Any
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.connection import get_sync_db
from database.models import IntegrationCredential
from orchestrator.vault import vault
from integrations.amazon_sp_api import amazon_sp_api
from integrations.ai_client import ai_client
from integrations.notification_hub import notification_hub

router = APIRouter(prefix="/api/integrations", tags=["Integrations"])


class UpdateCredentialRequest(BaseModel):
    service_name: str
    credentials: Dict[str, str]
    is_sandbox: bool = True


@router.get("/status")
def get_integrations_status():
    db = get_sync_db()
    try:
        sp_status = amazon_sp_api.get_connection_status()
        gemini_configured = ai_client.is_configured()

        tg_configured = bool(notification_hub.telegram_bot_token and notification_hub.telegram_chat_id)

        return {
            "amazon_sp_api": sp_status,
            "gemini_api": {
                "status": "CONFIGURED" if gemini_configured else "NOT_CONFIGURED",
                "connected": gemini_configured,
                "model": ai_client.model,
                "message": "AI analysis and listing drafting active" if gemini_configured else "Using deterministic rule-based synthesis"
            },
            "telegram_bot": {
                "status": "CONFIGURED" if tg_configured else "NOT_CONFIGURED",
                "connected": tg_configured,
                "message": "Instant briefings enabled" if tg_configured else "Telegram token not configured"
            }
        }
    finally:
        db.close()


@router.post("/update")
def update_credentials(req: UpdateCredentialRequest):
    db = get_sync_db()
    try:
        record = db.query(IntegrationCredential).filter(
            IntegrationCredential.service_name == req.service_name
        ).first()

        encrypted = vault.encrypt(req.credentials)
        if not record:
            record = IntegrationCredential(
                service_name=req.service_name,
                is_active=True,
                is_sandbox=req.is_sandbox,
                encrypted_credentials=encrypted,
                last_status="UPDATED"
            )
            db.add(record)
        else:
            record.encrypted_credentials = encrypted
            record.is_sandbox = req.is_sandbox
            record.is_active = True
            record.last_status = "UPDATED"

        db.commit()

        # Re-test connection
        if req.service_name == "AMAZON_SP_API":
            status = amazon_sp_api.get_connection_status()
        else:
            status = {"status": "UPDATED"}

        return {
            "status": "SUCCESS",
            "service_name": req.service_name,
            "connection_status": status
        }
    finally:
        db.close()
