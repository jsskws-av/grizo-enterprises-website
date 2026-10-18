"""
AGENT 2: Market and Competition Analyst
Analyzes competitive landscape, review moats, seller saturation, price war risk,
and customer complaints to identify differentiation opportunities on Amazon India.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent, DataType, ConfidenceLevel, sanitize_untrusted_text
from database.models import Product, MarketObservation
from integrations.ai_client import ai_client


class MarketAndCompetitionAnalyst(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="MarketAndCompetitionAnalyst",
            description="Evaluates market saturation, review barriers, price war risks, and unmet customer needs"
        )

    def analyze_competition_metrics(
        self,
        selling_price: float,
        review_count: int,
        rating_avg: float,
        num_sellers: int,
        is_amazon_sold: bool
    ) -> Dict[str, Any]:
        """
        Deterministic competitive risk analysis:
        - Review Moat: > 1,500 reviews = High Barrier for a new seller
        - Saturation: num_sellers > 8 = High Saturation / Risk of Buy Box splitting
        - Brand Dominance: Amazon Retail sold = High barrier
        """
        review_barrier = "LOW"
        if review_count > 2500:
            review_barrier = "VERY_HIGH"
        elif review_count > 800:
            review_barrier = "HIGH"
        elif review_count > 200:
            review_barrier = "MODERATE"

        saturation_level = "LOW"
        if num_sellers > 10:
            saturation_level = "VERY_HIGH"
        elif num_sellers > 5:
            saturation_level = "HIGH"
        elif num_sellers > 2:
            saturation_level = "MODERATE"

        price_war_risk = "HIGH" if (saturation_level in ["HIGH", "VERY_HIGH"] and not is_amazon_sold) else "LOW"

        # Realistic barrier score (0-100)
        barrier_score = 30.0
        if review_barrier in ["HIGH", "VERY_HIGH"]:
            barrier_score += 35.0
        if is_amazon_sold:
            barrier_score += 25.0
        if saturation_level in ["HIGH", "VERY_HIGH"]:
            barrier_score += 10.0

        can_realistically_compete = barrier_score < 75.0

        return {
            "review_barrier": review_barrier,
            "saturation_level": saturation_level,
            "price_war_risk": price_war_risk,
            "amazon_retail_competing": is_amazon_sold,
            "barrier_score": min(100.0, barrier_score),
            "can_realistically_compete": can_realistically_compete,
            "recommendation": (
                "Market is accessible for a differentiated new entrant"
                if can_realistically_compete else
                "High barriers to entry; established sellers hold strong review moats"
            )
        }

    def extract_differentiation_opportunities(
        self,
        product_title: str,
        category: str,
        reviews_or_complaints: List[str]
    ) -> Dict[str, Any]:
        """
        Synthesizes negative customer reviews and complaints into actionable product improvements.
        Uses AI synthesis when available, with deterministic fallback.
        """
        if not reviews_or_complaints:
            return {
                "differentiation_opportunities": [
                    "Bundle essential accessories (e.g. silicone heat handle, cleaning scraper)",
                    "Include bilingual care instructions in English and Hindi",
                    "Upgrade to premium retail gift packaging"
                ],
                "top_complaints": ["No direct complaints supplied"],
                "source": "DEFAULT_DIFFERENTIATION_PLAYBOOK"
            }

        untrusted_text = "\n".join(reviews_or_complaints)
        ai_res = ai_client.generate_json_response(
            system_instruction=(
                "You are an Amazon India product development specialist. "
                "Analyze the customer complaints for an Indian marketplace listing. "
                "Output JSON: {'top_complaints': [list], 'differentiation_opportunities': [list]}"
            ),
            user_prompt=f"Product: {product_title} in Category: {category}",
            untrusted_context=untrusted_text
        )

        if "differentiation_opportunities" in ai_res:
            return ai_res

        # Fallback
        return {
            "top_complaints": [sanitize_untrusted_text(c, 100) for c in reviews_or_complaints[:3]],
            "differentiation_opportunities": [
                f"Address primary customer friction: {sanitize_untrusted_text(reviews_or_complaints[0], 80)}",
                "Provide superior packaging to eliminate shipping damage",
                "Include clear warranty registration card"
            ],
            "source": "RULE_BASED_SYNTHESIS"
        }

    def run(self, db: Session, product_id: int, **kwargs) -> Dict[str, Any]:
        """Run competition audit for candidate product."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        obs = db.query(MarketObservation).filter(
            MarketObservation.product_id == product_id
        ).order_by(MarketObservation.observed_at.desc()).first()

        selling_price = obs.selling_price_inr if obs else 599.0
        review_count = obs.review_count if obs else 100
        rating_avg = obs.rating_avg if obs else 4.0
        num_sellers = obs.num_sellers if obs else 1
        is_amazon_sold = obs.is_amazon_sold if obs else False

        comp_metrics = self.analyze_competition_metrics(
            selling_price=selling_price,
            review_count=review_count,
            rating_avg=rating_avg,
            num_sellers=num_sellers,
            is_amazon_sold=is_amazon_sold
        )

        complaints = json.loads(obs.top_complaints_json) if obs and obs.top_complaints_json else []
        diff_ops = self.extract_differentiation_opportunities(product.title, product.category, complaints)

        # Transition status
        if product.status == "DISCOVERED":
            product.status = "ANALYSED"
            db.commit()

        self.log_action(
            db,
            action="ANALYZE_COMPETITION",
            resource_type="PRODUCT",
            resource_id=str(product_id),
            details={
                "review_barrier": comp_metrics["review_barrier"],
                "can_compete": comp_metrics["can_realistically_compete"],
                "barrier_score": comp_metrics["barrier_score"]
            }
        )

        return {
            "product_id": product_id,
            "competition_metrics": comp_metrics,
            "differentiation": diff_ops
        }


market_analyst = MarketAndCompetitionAnalyst()
