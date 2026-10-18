"""
AGENT 12: Daily Reporting Agent
Aggregates enterprise performance, candidate product scores, pending human approvals,
inventory reorder alerts, and compliance flags into an actionable daily executive report.
Delivers briefings to the dashboard and sends instant alerts via Telegram / Email.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime, date
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent, DataType, ConfidenceLevel
from database.models import (
    Product, DailyReportRecord, ApprovalRequest, InventoryItem, ProductScore,
    ProfitabilityAnalysis, SupplierQuote
)
from integrations.notification_hub import notification_hub


class DailyReportingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="DailyReportingAgent",
            description="Compiles daily 12-point executive intelligence report, replenishment alerts, and sends briefings"
        )

    def generate_daily_report(self, db: Session, target_date: Optional[str] = None) -> DailyReportRecord:
        """
        Compile full 12-point daily business report for India marketplace operations.
        """
        report_date_str = target_date or datetime.utcnow().strftime("%Y-%m-%d")

        # 1. Total products & statuses
        products = db.query(Product).all()
        total_products = len(products)
        discovered_count = sum(1 for p in products if p.status == "DISCOVERED")
        awaiting_approval_count = sum(1 for p in products if p.status == "AWAITING_APPROVAL")
        approved_count = sum(1 for p in products if p.status in ["APPROVED", "ACTION_EXECUTED"])
        rejected_count = sum(1 for p in products if p.status == "REJECTED")

        # 2. Top-ranked opportunities
        ranked_scores = db.query(ProductScore).filter(
            ProductScore.rejection_gate_passed == True
        ).order_by(ProductScore.overall_score.desc()).limit(5).all()

        top_opportunities = []
        for s in ranked_scores:
            p = s.product
            prof = p.profitability
            top_opportunities.append({
                "product_id": p.id,
                "title": p.title,
                "score": s.overall_score,
                "demand_score": s.demand_score,
                "profitability_score": s.profitability_score,
                "selling_price_inr": prof.target_selling_price_inr if prof else 0.0,
                "net_margin_pct": prof.net_profit_margin_pct if prof else 0.0,
                "net_profit_inr": prof.net_operating_profit_inr if prof else 0.0,
                "roi_pct": prof.roi_pct if prof else 0.0,
                "confidence": s.confidence_level
            })

        # 3. Pending approvals requiring urgent user attention
        pending_approvals = db.query(ApprovalRequest).filter(
            ApprovalRequest.status == "PENDING"
        ).order_by(ApprovalRequest.financial_impact_inr.desc()).all()

        urgent_actions = [
            {
                "request_id": a.id,
                "action_type": a.action_type,
                "title": a.title,
                "financial_impact_inr": a.financial_impact_inr,
                "requested_by": a.requested_by,
                "created_at": a.created_at.strftime("%H:%M IST")
            }
            for a in pending_approvals
        ]

        # 4. Inventory Replenishment Alerts
        low_stock_items = db.query(InventoryItem).filter(
            InventoryItem.current_stock_units <= InventoryItem.reorder_point_units
        ).all()

        replenishment_alerts = [
            {
                "product_id": item.product_id,
                "sku": item.sku,
                "title": item.product.title if item.product else item.sku,
                "current_stock": item.current_stock_units,
                "reorder_point": item.reorder_point_units,
                "days_of_supply": item.days_of_supply_remaining,
                "recommended_order_qty": item.recommended_reorder_qty,
                "stockout_risk_score": item.stockout_risk_score
            }
            for item in low_stock_items
        ]

        # 5. Format Summary Briefing
        summary = (
            f"DAILY E-COMMERCE BRIEFING ({report_date_str})\n"
            f"• Portfolio Overview: {total_products} tracked candidates ({approved_count} active/approved, {awaiting_approval_count} awaiting review, {rejected_count} rejected)\n"
            f"• Top Opportunity: {top_opportunities[0]['title'][:50]} (Score: {top_opportunities[0]['score']}/100, Margin: {top_opportunities[0]['net_margin_pct']}%)" if top_opportunities else "• No active opportunity"
            f"\n• Pending Human Approvals: {len(pending_approvals)} critical action items requiring review"
            f"\n• Inventory Alerts: {len(replenishment_alerts)} SKUs below Reorder Point (ROP)"
        )

        # Persist report
        existing = db.query(DailyReportRecord).filter(DailyReportRecord.report_date == report_date_str).first()
        if not existing:
            existing = DailyReportRecord(report_date=report_date_str)
            db.add(existing)

        existing.summary_text = summary
        existing.metrics_json = json.dumps({
            "total_products": total_products,
            "discovered": discovered_count,
            "awaiting_approval": awaiting_approval_count,
            "approved": approved_count,
            "rejected": rejected_count
        })
        existing.top_opportunities_json = json.dumps(top_opportunities)
        existing.urgent_actions_json = json.dumps(urgent_actions)
        existing.replenishment_alerts_json = json.dumps(replenishment_alerts)

        db.commit()
        db.refresh(existing)

        # Dispatch external alerts if configured
        if pending_approvals or replenishment_alerts:
            notification_hub.send_telegram_alert(
                f"📊 *Amazon India Daily Briefing ({report_date_str})*\n\n"
                f"• *Pending Approvals*: {len(pending_approvals)}\n"
                f"• *Restock Alerts*: {len(replenishment_alerts)}\n"
                f"• *Top Candidate*: {top_opportunities[0]['title'][:40] if top_opportunities else 'None'}\n\n"
                f"Open Dashboard to review and take action."
            )

        self.log_action(
            db,
            action="GENERATE_DAILY_REPORT",
            resource_type="DAILY_REPORT",
            resource_id=report_date_str,
            details={"urgent_actions_count": len(urgent_actions), "replenishment_alerts_count": len(replenishment_alerts)}
        )

        return existing

    def run(self, db: Session, **kwargs) -> Dict[str, Any]:
        report = self.generate_daily_report(db, kwargs.get("report_date"))
        return {
            "report_date": report.report_date,
            "summary": report.summary_text,
            "urgent_actions": json.loads(report.urgent_actions_json),
            "replenishment_alerts": json.loads(report.replenishment_alerts_json)
        }


reporting_agent = DailyReportingAgent()
