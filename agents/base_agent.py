"""
Base Agent Interface & Evidence Tagging Engine
Enforces:
1. Strict Provenance (Source, Timestamp, Confidence, Data Type)
2. Anti-Prompt-Injection Sanitization of untrusted web/review text
3. Audit logging of all agent actions
4. Deterministic fallback when data is unavailable (never fabricate numbers)
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import json
import re
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from database.models import AuditLog


class DataType(str, Enum):
    ACTUAL = "ACTUAL"                       # Directly observed / recorded (e.g., actual buy-box price, verified supplier quote)
    REPORTED_ESTIMATE = "REPORTED_ESTIMATE" # Defensible calculation from observable data (e.g., BSR sales curve)
    AI_HYPOTHESIS = "AI_HYPOTHESIS"         # Agent synthesized classification or suggestion


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


def sanitize_untrusted_text(text: str, max_chars: int = 2000) -> str:
    """
    Sanitize external product descriptions, customer reviews, and web scrapes.
    Neutralizes prompt injection vectors such as 'SYSTEM:', 'IGNORE PREVIOUS', backticks, and control chars.
    """
    if not text:
        return ""
    # Truncate
    cleaned = text[:max_chars]
    # Remove control characters
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', cleaned)
    # Neutralize injection keywords
    injection_patterns = [
        (r'(?i)ignore\s+(all\s+)?(previous|prior)\s+instructions', '[SANITIZED_INSTRUCTION]'),
        (r'(?i)system\s*:', '[SANITIZED_ROLE]:'),
        (r'(?i)assistant\s*:', '[SANITIZED_ROLE]:'),
        (r'```', "'''")
    ]
    for pattern, repl in injection_patterns:
        cleaned = re.sub(pattern, repl, cleaned)
    return cleaned.strip()


class BaseAgent(ABC):
    def __init__(self, agent_name: str, description: str):
        self.agent_name = agent_name
        self.description = description

    def tag_evidence(
        self,
        value: Any,
        source: str,
        data_type: DataType,
        confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Wrap any metric with explicit provenance."""
        return {
            "value": value,
            "source": source,
            "data_type": data_type.value,
            "confidence": confidence.value,
            "observed_at": datetime.utcnow().isoformat(),
            "notes": notes
        }

    def log_action(
        self,
        db: Session,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Record agent action to immutable audit log."""
        audit = AuditLog(
            actor=f"AGENT:{self.agent_name}",
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details_json=json.dumps(details or {}),
            timestamp=datetime.utcnow()
        )
        db.add(audit)
        db.commit()

    @abstractmethod
    def run(self, db: Session, **kwargs) -> Dict[str, Any]:
        """Execute agent workflow."""
        pass
