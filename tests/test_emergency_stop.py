"""
Automated Test Suite for Emergency Stop Circuit Breaker
Verifies that when Emergency Stop is engaged, all write operations are halted.
"""

import pytest
from orchestrator.emergency_stop import emergency_stop


def test_emergency_stop_lifecycle():
    """Test engaging, assertion, and reset of emergency stop."""
    # Ensure initially reset
    emergency_stop.reset("TEST_RUNNER")
    assert emergency_stop.is_active is False

    # Should not raise when inactive
    emergency_stop.assert_can_write("TEST_WRITE_OPERATION")

    # Engage emergency stop
    status = emergency_stop.trigger(triggered_by="ADMIN_USER", reason="Test halt")
    assert emergency_stop.is_active is True
    assert status["emergency_stop_active"] is True
    assert status["reason"] == "Test halt"

    # Must raise RuntimeError on attempted write operation
    with pytest.raises(RuntimeError) as exc_info:
        emergency_stop.assert_can_write("PUBLISH_LISTING_TO_AMAZON")
    assert "OPERATION BLOCKED: Emergency Stop is ACTIVE" in str(exc_info.value)

    # Disengage and verify write operations resume safely
    reset_status = emergency_stop.reset("ADMIN_USER")
    assert reset_status["emergency_stop_active"] is False
    emergency_stop.assert_can_write("PUBLISH_LISTING_TO_AMAZON")
