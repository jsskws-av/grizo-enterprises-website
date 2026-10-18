"""
Product Scoring Engine & Mandatory Rejection Gate System
Combines a configurable multi-factor weighted scoring model with non-negotiable rejection gates.
A high numerical score cannot bypass compliance, missing documentation, or margin floors.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from config.business_rules import ScoringWeights, RejectionThresholds, DEFAULT_SCORING_WEIGHTS, DEFAULT_REJECTION_THRESHOLDS
from database.models import (
    Product, MarketObservation, SupplierQuote, ProfitabilityAnalysis,
    ProductScore, ComplianceCheck, KeywordRecord
)


class ScoringEngine:
    def __init__(
        self,
        weights: Optional[ScoringWeights] = None,
        thresholds: Optional[RejectionThresholds] = None
    ):
        self.weights = weights or DEFAULT_SCORING_WEIGHTS
        self.thresholds = thresholds or DEFAULT_REJECTION_THRESHOLDS

    def evaluate_rejection_gates(
        self,
        product: Product,
        profitability: Optional[ProfitabilityAnalysis],
        supplier_quote: Optional[SupplierQuote],
        compliance: Optional[ComplianceCheck]
    ) -> List[str]:
        """
        Evaluate non-negotiable rejection rules.
        Returns a list of failure reasons. If empty, the product passes the gates.
        """
        failures = []

        # Gate 1: Minimum Net Profit Margin %
        if profitability:
            if profitability.net_profit_margin_pct < self.thresholds.min_net_profit_margin_pct:
                failures.append(
                    f"Net profit margin ({profitability.net_profit_margin_pct:.1f}%) "
                    f"is below minimum requirement ({self.thresholds.min_net_profit_margin_pct:.1f}%)"
                )
            if profitability.contribution_per_unit_inr < self.thresholds.min_contribution_per_unit_inr:
                failures.append(
                    f"Unit contribution (₹{profitability.contribution_per_unit_inr:.1f}) "
                    f"is below minimum floor (₹{self.thresholds.min_contribution_per_unit_inr:.1f})"
                )
        else:
            failures.append("Missing profitability analysis; cannot evaluate financial viability")

        # Gate 2: Supplier Quotation & Verification
        if self.thresholds.require_verified_supplier_quote:
            if not supplier_quote:
                failures.append("No supplier quotation on record")
            elif not supplier_quote.is_verified:
                failures.append(f"Supplier quote is unverified ({supplier_quote.verification_method})")

        # Gate 3: Compliance & Legal Restrictions
        if compliance:
            if self.thresholds.reject_hazmat_and_restricted and compliance.special_handling == "HAZMAT":
                failures.append("Product classified as HAZMAT / Dangerous Goods")
            if compliance.category_restricted:
                failures.append("Category requires brand ungating / special documentation not yet on file")
            if self.thresholds.reject_trademark_infringements and compliance.trademark_risk_score > 0.40:
                failures.append(f"High trademark infringement risk detected (Risk: {compliance.trademark_risk_score:.2f})")
            if compliance.fragility_tier > self.thresholds.max_fragility_tier:
                failures.append(f"Fragility tier ({compliance.fragility_tier}) exceeds maximum threshold ({self.thresholds.max_fragility_tier})")
        else:
            failures.append("Compliance audit pending; cannot verify legal safety")

        return failures

    def compute_subscores(
        self,
        product: Product,
        observation: Optional[MarketObservation],
        profitability: Optional[ProfitabilityAnalysis],
        supplier_quote: Optional[SupplierQuote],
        compliance: Optional[ComplianceCheck],
        keywords: List[KeywordRecord]
    ) -> Dict[str, float]:
        """Compute 0-100 sub-scores for each dimension based on observable evidence."""
        # 1. Demand Score (0 - 100)
        demand_score = 50.0
        if observation and observation.estimated_monthly_sales:
            sales = observation.estimated_monthly_sales
            if sales >= 500:
                demand_score = 95.0
            elif sales >= 250:
                demand_score = 85.0
            elif sales >= 100:
                demand_score = 70.0
            else:
                demand_score = max(20.0, sales * 0.5)

        # 2. Profitability Score (0 - 100)
        profit_score = 40.0
        if profitability:
            margin = profitability.net_profit_margin_pct
            if margin >= 30.0:
                profit_score = 95.0
            elif margin >= 20.0:
                profit_score = 80.0
            elif margin >= 15.0:
                profit_score = 65.0
            elif margin >= 10.0:
                profit_score = 45.0
            else:
                profit_score = max(0.0, margin * 2.5)

        # 3. Competition Score (0 - 100, higher = less saturated / easier to compete)
        comp_score = 60.0
        if observation:
            if observation.is_amazon_sold:
                comp_score -= 25.0
            if observation.review_count > 5000:
                comp_score -= 30.0
            elif observation.review_count > 1000:
                comp_score -= 15.0
            elif observation.review_count < 200:
                comp_score += 15.0
            comp_score = max(10.0, min(100.0, comp_score))

        # 4. Supplier Reliability Score (0 - 100)
        supplier_score = 40.0
        if supplier_quote:
            if supplier_quote.is_verified:
                supplier_score = 90.0
            else:
                supplier_score = 60.0
            if supplier_quote.lead_time_days <= 7:
                supplier_score += 5.0

        # 5. Stability Score (0 - 100)
        stability_score = 75.0  # Assumes standard demand curve

        # 6. Keyword Opportunity Score (0 - 100)
        kw_score = 50.0
        if keywords:
            total_vol = sum(k.search_volume_monthly or 0 for k in keywords)
            if total_vol > 20000:
                kw_score = 90.0
            elif total_vol > 5000:
                kw_score = 75.0
            else:
                kw_score = 60.0

        # 7. Operational Simplicity Score (0 - 100)
        simplicity_score = 80.0
        if product.package_weight_grams > 3000:
            simplicity_score -= 30.0
        elif product.package_weight_grams > 1000:
            simplicity_score -= 15.0

        # 8. Return & Compliance Risk Score (0 - 100, higher = lower risk / safer)
        risk_score = 80.0
        if compliance:
            if compliance.fragility_tier >= 3:
                risk_score -= 40.0
            elif compliance.fragility_tier == 2:
                risk_score -= 15.0

        return {
            "demand": round(demand_score, 1),
            "profitability": round(profit_score, 1),
            "competition": round(comp_score, 1),
            "supplier": round(supplier_score, 1),
            "stability": round(stability_score, 1),
            "keyword": round(kw_score, 1),
            "simplicity": round(simplicity_score, 1),
            "risk": round(risk_score, 1)
        }

    def score_product(self, db: Session, product_id: int) -> ProductScore:
        """Evaluate rejection gates, calculate weighted score, and persist."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        observation = db.query(MarketObservation).filter(
            MarketObservation.product_id == product_id
        ).order_by(MarketObservation.observed_at.desc()).first()

        profitability = db.query(ProfitabilityAnalysis).filter(
            ProfitabilityAnalysis.product_id == product_id
        ).first()

        supplier_quote = db.query(SupplierQuote).filter(
            SupplierQuote.product_id == product_id
        ).order_by(SupplierQuote.created_at.desc()).first()

        compliance = db.query(ComplianceCheck).filter(
            ComplianceCheck.product_id == product_id
        ).first()

        keywords = db.query(KeywordRecord).filter(
            KeywordRecord.product_id == product_id
        ).all()

        # Step 1: Evaluate Rejection Gates
        gate_failures = self.evaluate_rejection_gates(
            product=product,
            profitability=profitability,
            supplier_quote=supplier_quote,
            compliance=compliance
        )
        passed_gates = len(gate_failures) == 0

        # Step 2: Compute Dimensional Subscores
        subscores = self.compute_subscores(
            product=product,
            observation=observation,
            profitability=profitability,
            supplier_quote=supplier_quote,
            compliance=compliance,
            keywords=keywords
        )

        # Step 3: Compute Weighted Overall Score
        overall = (
            (subscores["demand"] * self.weights.demand_evidence) +
            (subscores["profitability"] * self.weights.profitability) +
            (subscores["competition"] * self.weights.competition) +
            (subscores["supplier"] * self.weights.supplier_reliability) +
            (subscores["stability"] * self.weights.sales_pricing_stability) +
            (subscores["keyword"] * self.weights.keyword_opportunity) +
            (subscores["simplicity"] * self.weights.operational_simplicity) +
            (subscores["risk"] * self.weights.return_compliance_risk)
        )
        overall = round(overall, 1)

        # Update product status if rejected
        if not passed_gates and product.status not in ["APPROVED", "ACTION_EXECUTED"]:
            product.status = "REJECTED"
            product.rejection_reason = " | ".join(gate_failures)

        # Persist or update ProductScore
        existing = db.query(ProductScore).filter(ProductScore.product_id == product_id).first()
        if not existing:
            existing = ProductScore(product_id=product_id)
            db.add(existing)

        existing.overall_score = overall
        existing.demand_score = subscores["demand"]
        existing.profitability_score = subscores["profitability"]
        existing.competition_score = subscores["competition"]
        existing.supplier_score = subscores["supplier"]
        existing.stability_score = subscores["stability"]
        existing.keyword_score = subscores["keyword"]
        existing.simplicity_score = subscores["simplicity"]
        existing.risk_score = subscores["risk"]
        existing.rejection_gate_passed = passed_gates
        existing.gate_failures_json = json.dumps(gate_failures)
        existing.evidence_summary_json = json.dumps({
            "observation_source": observation.source if observation else "NONE",
            "observation_date": observation.observed_at.isoformat() if observation else None,
            "data_confidence": observation.confidence_level if observation else "LOW",
            "gate_status": "PASSED" if passed_gates else "FAILED"
        })
        existing.calculated_at = datetime.utcnow()

        db.commit()
        db.refresh(existing)
        return existing


scoring_engine = ScoringEngine()
