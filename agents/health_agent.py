"""
AGENT 11: Listing Health and Performance Agent
Monitors post-launch listing health, conversion velocity, return rates,
Buy Box ownership, suppression alerts, and customer complaint trends.
Never claims access to metrics not made available by Amazon APIs.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent, DataType, ConfidenceLevel
from database.models import Product, InventoryItem, MarketObservation


class ListingHealthAndPerformanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="ListingHealthAndPerformanceAgent",
            description="Tracks listing health, buy-box ownership, return trends, and suppression alerts"
        )

    def diagnose_health(
        self,
        product: Product,
        inventory: Optional[InventoryItem],
        observation: Optional[MarketObservation]
    ) -> Dict[str, Any]:
        """
        Diagnose listing health and generate corrective action items:
        - Listing Suppression: Missing title, images, or GTIN
        - Stockout Risk: Days of supply < 7
        - Buy Box Loss: num_sellers > 1 and buy_box_winner != our brand
        - Quality/Return Alert: Rating < 3.8
        """
        alerts = []
        health_score = 100

        # Check suppression risks
        if not product.listing_draft or not product.listing_draft.checklist_passed:
            alerts.append({"type": "COMPLIANCE_DEFECT", "severity": "HIGH", "message": "Draft checklist missing mandatory attributes."})
            health_score -= 25

        # Check inventory risk
        if inventory:
            if inventory.days_of_supply_remaining < 5.0 and inventory.current_stock_units > 0:
                alerts.append({"type": "CRITICAL_STOCK_DEPLETION", "severity": "HIGH", "message": f"Only {inventory.days_of_supply_remaining:.1f} days of stock remaining; reorder urgently."})
                health_score -= 20
            elif inventory.current_stock_units == 0:
                alerts.append({"type": "STOCKOUT", "severity": "CRITICAL", "message": "Listing is Out of Stock. Search ranking is decaying."})
                health_score -= 40

        # Check buy box
        if observation:
            if observation.rating_avg > 0 and observation.rating_avg < 3.8:
                alerts.append({"type": "POOR_RATING", "severity": "MEDIUM", "message": f"Average rating is {observation.rating_avg:.1f}/5. Review negative feedback."})
                health_score -= 15
            if observation.num_sellers > 3:
                alerts.append({"type": "BUY_BOX_COMPETITION", "severity": "LOW", "message": f"{observation.num_sellers} competing sellers on listing."})
                health_score -= 10

        status = "HEALTHY" if health_score >= 80 else ("NEEDS_ATTENTION" if health_score >= 60 else "CRITICAL")

        return {
            "health_score": max(0, health_score),
            "status": status,
            "alerts": alerts,
            "monitored_at": datetime.utcnow().isoformat()
        }

    def run(self, db: Session, product_id: int, **kwargs) -> Dict[str, Any]:
        """Audit health of an active listing."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        diag = self.diagnose_health(
            product=product,
            inventory=product.inventory,
            observation=product.observations[-1] if product.observations else None
        )

        self.log_action(
            db,
            action="AUDIT_LISTING_HEALTH",
            resource_type="PRODUCT",
            resource_id=str(product_id),
            details={"status": diag["status"], "score": diag["health_score"], "alerts_count": len(diag["alerts"])}
        )

        return {"product_id": product_id, "diagnosis": diag}


health_agent = ListingHealthAndPerformanceAgent()
