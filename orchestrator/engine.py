"""
Central Multi-Agent Orchestration Engine
Coordinates the execution pipeline across all 12 specialized agents:
Discovery -> Market Analysis -> Supplier Vetting -> Profitability -> Compliance -> Scoring -> Keywords -> Images -> Listing -> Approval -> Inventory -> Reporting.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from agents.discovery_agent import discovery_agent
from agents.market_analyst import market_analyst
from agents.cost_profit_agent import cost_profit_agent
from agents.supplier_agent import supplier_agent
from agents.risk_agent import risk_agent
from agents.keyword_agent import keyword_agent
from agents.image_agent import image_agent
from agents.listing_agent import listing_agent
from agents.inventory_agent import inventory_agent
from agents.price_agent import price_agent
from agents.health_agent import health_agent
from agents.reporting_agent import reporting_agent
from orchestrator.scoring_engine import scoring_engine
from orchestrator.emergency_stop import emergency_stop
from database.models import Product, AuditLog


class MultiAgentOrchestrator:
    def __init__(self):
        self.emergency_stop = emergency_stop

    def evaluate_product_pipeline(self, db: Session, product_id: int) -> Dict[str, Any]:
        """
        Execute full end-to-end evaluation pipeline for a candidate product:
        1. Market & Competition Analysis
        2. Supplier Research Audit
        3. Cost & Profitability Calculation (Deterministic)
        4. Regulatory Compliance & Hazmat Screening
        5. Weighted Scoring & Rejection Gate Check
        6. Keyword Harvesting
        7. Product Image Asset Planning
        8. Listing Draft Preparation & Approval Request Creation
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        pipeline_log = []

        # 1. Market & Competition Analysis
        comp_res = market_analyst.run(db, product_id)
        pipeline_log.append({"step": "MarketAnalysis", "status": "COMPLETED", "summary": comp_res["competition_metrics"]["recommendation"]})

        # 2. Supplier Audit
        sup_res = supplier_agent.run(db, product_id)
        pipeline_log.append({"step": "SupplierAudit", "status": "COMPLETED", "has_verified_supplier": sup_res["has_verified_supplier"]})

        # 3. Cost & Profitability Calculation
        prof_res = cost_profit_agent.run(db, product_id)
        pipeline_log.append({
            "step": "Profitability",
            "status": "COMPLETED",
            "net_margin": f"{prof_res['net_profit_margin_pct']}%",
            "is_provisional": prof_res.get("is_provisional", False)
        })

        # 4. Compliance & Risk Audit
        risk_res = risk_agent.run(db, product_id)
        pipeline_log.append({
            "step": "Compliance",
            "status": "COMPLETED",
            "is_safe": risk_res["is_safe_to_sell"],
            "flags": risk_res["rejection_flags"]
        })

        # 5. Scoring & Mandatory Rejection Gates
        score_rec = scoring_engine.score_product(db, product_id)
        passed_gates = score_rec.rejection_gate_passed
        pipeline_log.append({
            "step": "Scoring",
            "status": "PASSED" if passed_gates else "REJECTED",
            "score": score_rec.overall_score,
            "gate_passed": passed_gates
        })

        # If rejected by mandatory gates, halt pipeline here
        if not passed_gates:
            pipeline_log.append({
                "step": "PipelineHalted",
                "status": "REJECTED_BY_GATE",
                "reason": score_rec.gate_failures_json
            })
            return {
                "product_id": product_id,
                "pipeline_status": "REJECTED",
                "score": score_rec.overall_score,
                "rejection_reasons": json.loads(score_rec.gate_failures_json),
                "steps": pipeline_log
            }

        # 6. Keyword Research
        kw_res = keyword_agent.run(db, product_id)
        pipeline_log.append({"step": "KeywordResearch", "status": "COMPLETED", "keywords_found": len(kw_res["keywords"])})

        # 7. Image Studio Planning
        img_res = image_agent.run(db, product_id)
        pipeline_log.append({"step": "ImageStudio", "status": "COMPLETED", "slots_planned": len(img_res["image_plan"])})

        # 8. Listing Draft Preparation
        listing_res = listing_agent.run(db, product_id)
        pipeline_log.append({
            "step": "ListingDraft",
            "status": "AWAITING_APPROVAL",
            "approval_request_id": listing_res["approval_request_id"]
        })

        # 9. Inventory Audit
        inv_res = inventory_agent.run(db, product_id)
        pipeline_log.append({
            "step": "InventoryAudit",
            "status": "COMPLETED",
            "days_of_supply": inv_res["metrics"]["days_of_supply"]
        })

        db.commit()

        return {
            "product_id": product_id,
            "pipeline_status": "AWAITING_APPROVAL",
            "overall_score": score_rec.overall_score,
            "net_profit_margin_pct": prof_res["net_profit_margin_pct"],
            "approval_request_id": listing_res["approval_request_id"],
            "steps": pipeline_log
        }


orchestrator = MultiAgentOrchestrator()
