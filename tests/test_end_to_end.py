"""
End-to-End System Verification Test Suite
Simulates the entire workflow from product ingestion to 12-agent pipeline evaluation,
approval decisions, daily reports, and CSV export.
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from orchestrator.emergency_stop import emergency_stop

client = TestClient(app)


def test_api_health_and_dashboard_serving():
    """Verify dashboard loads and returns HTML."""
    res = client.get("/")
    assert res.status_code == 200
    assert "Amazon India AI E-Commerce Automation Platform" in res.text


def test_product_ingestion_and_pipeline_execution():
    """Verify end-to-end product creation and agent pipeline."""
    payload = {
        "title": "Ergonomic Memory Foam Footrest Cushion for Office Desk",
        "category": "Office Products & Stationery",
        "selling_price": 799.0,
        "asin": "B09ABC1234",
        "bsr_rank": 950,
        "package_weight_grams": 450.0,
        "fulfilment_channel": "EASY_SHIP",
        "supplier_name": "Comfort Foams Pvt Ltd (Noida)",
        "supplier_quoted_price": 240.0,
        "supplier_moq": 100,
        "supplier_is_verified": True
    }
    res = client.post("/api/products", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "product_id" in data
    assert data["pipeline"]["pipeline_status"] in ["AWAITING_APPROVAL", "APPROVED"]
    assert data["pipeline"]["overall_score"] > 50


def test_calculator_api_accuracy():
    """Verify calculator endpoint returns exact Amazon India fees and net profit."""
    res = client.post("/api/calculator", json={
        "category": "Home & Kitchen",
        "selling_price": 999.0,
        "supplier_cost": 320.0,
        "package_weight_grams": 2100.0,
        "fulfilment_channel": "EASY_SHIP",
        "shipping_zone": "NATIONAL"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["referral_fee"] == 94.91
    assert data["closing_fee"] == 24.0
    assert data["weight_handling_fee"] == 198.0
    assert data["net_profit_margin_pct"] > 0.0


def test_approval_centre_workflow():
    """Verify listing and executing approval requests."""
    res = client.get("/api/approvals?status=PENDING")
    assert res.status_code == 200
    approvals = res.json()
    assert isinstance(approvals, list)

    if approvals:
        req_id = approvals[0]["id"]
        # Approve
        app_res = client.post(f"/api/approvals/{req_id}/approve", json={
            "user_name": "Test Runner",
            "notes": "E2E automated approval verification"
        })
        assert app_res.status_code == 200
        assert app_res.json()["status"] == "SUCCESS"

        # Execute
        exec_res = client.post(f"/api/approvals/{req_id}/execute")
        assert exec_res.status_code == 200
        assert exec_res.json()["status"] in ["SIMULATED_EXECUTION", "LIVE_EXECUTED", "EXECUTED"]


def test_daily_report_generation_and_csv_export():
    """Verify daily report generation and portfolio CSV export."""
    # Generate report
    rep_res = client.post("/api/reports/generate")
    assert rep_res.status_code == 200
    assert rep_res.json()["status"] == "SUCCESS"

    # Export CSV
    csv_res = client.get("/api/reports/export/csv")
    assert csv_res.status_code == 200
    assert "text/csv" in csv_res.headers["content-type"]
    assert "Target Price (INR)" in csv_res.text
