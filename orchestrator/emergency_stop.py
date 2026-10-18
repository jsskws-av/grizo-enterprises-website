"""
Emergency Stop & Operational Circuit Breaker
Provides a fail-safe mechanism that instantly blocks all automated write operations
(orders, price adjustments, ad budget increases, listing uploads) without losing business data.
"""

import threading
from typing import Dict, Any
from datetime import datetime

class EmergencyStopController:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._is_stopped = False
                cls._instance._reason = ""
                cls._instance._stopped_at = None
                cls._instance._stopped_by = ""
        return cls._instance

    @property
    def is_active(self) -> bool:
        """Returns True if emergency stop is engaged."""
        return self._is_stopped

    def trigger(self, triggered_by: str = "USER", reason: str = "Manual Emergency Stop triggered") -> Dict[str, Any]:
        """Activate Emergency Stop: immediately freeze write operations."""
        with self._lock:
            self._is_stopped = True
            self._reason = reason
            self._stopped_at = datetime.utcnow()
            self._stopped_by = triggered_by
            return self.get_status()

    def reset(self, reset_by: str = "USER") -> Dict[str, Any]:
        """Disengage Emergency Stop and return to normal operation."""
        with self._lock:
            self._is_stopped = False
            self._reason = ""
            self._stopped_at = None
            self._stopped_by = ""
            return self.get_status()

    def assert_can_write(self, operation_name: str):
        """
        Safety Guard: raises RuntimeError if emergency stop is active.
        Must be called prior to ANY mutating operation against external services.
        """
        if self._is_stopped:
            raise RuntimeError(
                f"OPERATION BLOCKED: Emergency Stop is ACTIVE. "
                f"Cannot execute write operation '{operation_name}'. "
                f"Reason: {self._reason} (Engaged at: {self._stopped_at} by {self._stopped_by})"
            )

    def get_status(self) -> Dict[str, Any]:
        return {
            "emergency_stop_active": self._is_stopped,
            "reason": self._reason,
            "stopped_at": self._stopped_at.isoformat() if self._stopped_at else None,
            "stopped_by": self._stopped_by
        }


emergency_stop = EmergencyStopController()
