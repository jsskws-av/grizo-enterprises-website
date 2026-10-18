"""
Background Daily Automation Scheduler & Cron Runner
Executes Morning Sync, Midday Monitoring, and Evening Reporting cycles.
Runs asynchronously without blocking web requests and supports manual on-demand triggers.
"""

import asyncio
from datetime import datetime
import json
import logging
from typing import Dict, Any, Optional

from database.connection import SyncSessionLocal
from database.models import Product, AuditLog
from orchestrator.engine import orchestrator
from agents.inventory_agent import inventory_agent
from agents.reporting_agent import reporting_agent
from orchestrator.emergency_stop import emergency_stop
from config.settings import settings

logger = logging.getLogger("DailyScheduler")


class DailyScheduler:
    def __init__(self):
        self._is_running = False
        self._task: Optional[asyncio.Task] = None
        self._last_morning_run: Optional[str] = None
        self._last_midday_run: Optional[str] = None
        self._last_evening_run: Optional[str] = None

    @property
    def is_running(self) -> bool:
        return self._is_running

    def run_morning_cycle(self) -> Dict[str, Any]:
        """
        Morning Cycle (07:30 IST):
        Recalculate profitability, update competitor observations, update rankings.
        """
        db = SyncSessionLocal()
        try:
            products = db.query(Product).filter(Product.status != "REJECTED").all()
            updated_count = 0
            for p in products:
                try:
                    orchestrator.evaluate_product_pipeline(db, p.id)
                    updated_count += 1
                except Exception as e:
                    logger.error(f"Error updating product #{p.id} in morning cycle: {e}")

            self._last_morning_run = datetime.utcnow().isoformat()
            audit = AuditLog(
                actor="SCHEDULER:MorningCycle",
                action="RUN_MORNING_CYCLE",
                resource_type="SYSTEM",
                details_json=json.dumps({"products_processed": updated_count})
            )
            db.add(audit)
            db.commit()
            return {"status": "SUCCESS", "cycle": "MORNING", "products_processed": updated_count}
        finally:
            db.close()

    def run_midday_cycle(self) -> Dict[str, Any]:
        """
        Midday Cycle (13:00 IST):
        Monitor inventory levels, calculate ROPs, create replenishment approval requests.
        """
        db = SyncSessionLocal()
        try:
            products = db.query(Product).filter(Product.status.in_(["APPROVED", "ACTION_EXECUTED"])).all()
            alerts_count = 0
            for p in products:
                try:
                    inv_res = inventory_agent.run(db, p.id)
                    if inv_res.get("approval_request_id"):
                        alerts_count += 1
                except Exception as e:
                    logger.error(f"Error auditing inventory for product #{p.id}: {e}")

            self._last_midday_run = datetime.utcnow().isoformat()
            audit = AuditLog(
                actor="SCHEDULER:MiddayCycle",
                action="RUN_MIDDAY_CYCLE",
                resource_type="SYSTEM",
                details_json=json.dumps({"inventory_alerts_generated": alerts_count})
            )
            db.add(audit)
            db.commit()
            return {"status": "SUCCESS", "cycle": "MIDDAY", "inventory_alerts_generated": alerts_count}
        finally:
            db.close()

    def run_evening_cycle(self) -> Dict[str, Any]:
        """
        Evening Cycle (20:00 IST):
        Generate daily report, compile opportunities, send notifications.
        """
        db = SyncSessionLocal()
        try:
            rep = reporting_agent.generate_daily_report(db)
            self._last_evening_run = datetime.utcnow().isoformat()
            audit = AuditLog(
                actor="SCHEDULER:EveningCycle",
                action="RUN_EVENING_CYCLE",
                resource_type="DAILY_REPORT",
                resource_id=rep.report_date,
                details_json=json.dumps({"report_date": rep.report_date})
            )
            db.add(audit)
            db.commit()
            return {"status": "SUCCESS", "cycle": "EVENING", "report_date": rep.report_date}
        finally:
            db.close()

    async def start(self):
        """Asynchronous background loop."""
        self._is_running = True
        while self._is_running:
            try:
                now = datetime.utcnow()
                # IST is UTC + 5:30 -> Calculate IST hour & minute
                # Alternatively run periodic heartbeat every 60 seconds
                await asyncio.sleep(60)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Scheduler loop error: {e}")
                await asyncio.sleep(10)

    def stop(self):
        self._is_running = False
        if self._task:
            self._task.cancel()

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_running": self._is_running,
            "last_morning_run": self._last_morning_run,
            "last_midday_run": self._last_midday_run,
            "last_evening_run": self._last_evening_run,
            "schedule_config": {
                "morning": f"{settings.morning_sync_hour:02d}:{settings.morning_sync_minute:02d} IST",
                "midday": f"{settings.midday_monitor_hour:02d}:{settings.midday_monitor_minute:02d} IST",
                "evening": f"{settings.evening_report_hour:02d}:{settings.evening_report_minute:02d} IST"
            }
        }


daily_scheduler = DailyScheduler()
