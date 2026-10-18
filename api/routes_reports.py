"""
Daily Reports, Historical Executive Briefings, and CSV/Excel Export API
"""

from typing import List, Optional, Dict, Any
import json
import csv
import io
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse

from database.connection import get_sync_db
from database.models import DailyReportRecord, Product, ProductScore, ProfitabilityAnalysis
from agents.reporting_agent import reporting_agent

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("")
def list_reports():
    db = get_sync_db()
    try:
        reps = db.query(DailyReportRecord).order_by(DailyReportRecord.created_at.desc()).all()
        return [
            {
                "id": r.id,
                "report_date": r.report_date,
                "summary": r.summary_text,
                "metrics": json.loads(r.metrics_json) if r.metrics_json else {},
                "top_opportunities": json.loads(r.top_opportunities_json) if r.top_opportunities_json else [],
                "urgent_actions": json.loads(r.urgent_actions_json) if r.urgent_actions_json else [],
                "replenishment_alerts": json.loads(r.replenishment_alerts_json) if r.replenishment_alerts_json else [],
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M")
            }
            for r in reps
        ]
    finally:
        db.close()


@router.get("/latest")
def get_latest_report():
    db = get_sync_db()
    try:
        rep = db.query(DailyReportRecord).order_by(DailyReportRecord.created_at.desc()).first()
        if not rep:
            # Generate one on the fly
            rep = reporting_agent.generate_daily_report(db)

        return {
            "id": rep.id,
            "report_date": rep.report_date,
            "summary": rep.summary_text,
            "metrics": json.loads(rep.metrics_json) if rep.metrics_json else {},
            "top_opportunities": json.loads(rep.top_opportunities_json) if rep.top_opportunities_json else [],
            "urgent_actions": json.loads(rep.urgent_actions_json) if rep.urgent_actions_json else [],
            "replenishment_alerts": json.loads(rep.replenishment_alerts_json) if rep.replenishment_alerts_json else [],
            "created_at": rep.created_at.strftime("%Y-%m-%d %H:%M")
        }
    finally:
        db.close()


@router.post("/generate")
def trigger_daily_report():
    db = get_sync_db()
    try:
        rep = reporting_agent.generate_daily_report(db)
        return {"status": "SUCCESS", "report_date": rep.report_date}
    finally:
        db.close()


@router.get("/export/csv")
def export_products_csv():
    """Export complete product portfolio, unit economics, and scores to CSV."""
    db = get_sync_db()
    try:
        products = db.query(Product).all()
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow([
            "ID", "Title", "Category", "Status", "Overall Score", "Rejection Gate Passed",
            "Target Price (INR)", "Supplier Cost (INR)", "Net Margin (%)", "Net Profit (INR)",
            "ROI (%)", "Estimated Monthly Sales", "Review Count", "Rating", "Current Stock",
            "Days of Supply Remaining", "Rejection Reason"
        ])

        for p in products:
            prof = p.profitability
            obs = p.observations[-1] if p.observations else None
            score = p.score
            inv = p.inventory

            writer.writerow([
                p.id,
                p.title,
                p.category,
                p.status,
                score.overall_score if score else 0.0,
                "YES" if (score and score.rejection_gate_passed) else "NO",
                prof.target_selling_price_inr if prof else (obs.selling_price_inr if obs else 0.0),
                prof.supplier_cost_inr if prof else 0.0,
                prof.net_profit_margin_pct if prof else 0.0,
                prof.net_operating_profit_inr if prof else 0.0,
                prof.roi_pct if prof else 0.0,
                obs.estimated_monthly_sales if obs else 0,
                obs.review_count if obs else 0,
                obs.rating_avg if obs else 0.0,
                inv.current_stock_units if inv else 0,
                inv.days_of_supply_remaining if inv else 0.0,
                p.rejection_reason or ""
            ])

        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode("utf-8")),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=amazon_in_product_portfolio.csv"}
        )
    finally:
        db.close()
