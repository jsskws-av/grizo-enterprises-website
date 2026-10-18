"""
AGENT 4: Supplier Research Agent
Identifies potential wholesale suppliers in India (IndiaMART, TradeIndia, direct manufacturers).
Tracks verified supplier quotations, MOQs, lead times, and verification checklists.
PROHIBITION: Never claims a supplier is verified without proof; never places purchase orders automatically.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent, DataType, ConfidenceLevel, sanitize_untrusted_text
from database.models import Product, SupplierQuote


class SupplierResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="SupplierResearchAgent",
            description="Manages supplier discovery, quotation intake, verification status, and procurement terms"
        )

    def record_supplier_quote(
        self,
        db: Session,
        product_id: int,
        supplier_name: str,
        quoted_price_inr: float,
        moq: int = 50,
        supplier_contact: Optional[str] = None,
        platform: str = "IndiaMART",
        shipping_cost_to_warehouse: float = 20.0,
        lead_time_days: int = 7,
        input_gst_pct: float = 18.0,
        is_verified: bool = False,
        verification_method: str = "Pending manual phone/invoice confirmation",
        verification_notes: Optional[str] = None
    ) -> SupplierQuote:
        """
        Record a supplier quote with honest verification status.
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        quote = SupplierQuote(
            product_id=product_id,
            supplier_name=sanitize_untrusted_text(supplier_name, 120),
            supplier_contact=sanitize_untrusted_text(supplier_contact or "", 150),
            platform=platform,
            quoted_price_inr=max(1.0, float(quoted_price_inr)),
            input_gst_pct=input_gst_pct,
            moq=max(1, int(moq)),
            shipping_cost_to_warehouse=max(0.0, float(shipping_cost_to_warehouse)),
            lead_time_days=max(1, int(lead_time_days)),
            is_verified=bool(is_verified),
            verification_method=verification_method,
            verification_notes=verification_notes,
            created_at=datetime.utcnow()
        )
        db.add(quote)
        db.commit()
        db.refresh(quote)

        self.log_action(
            db,
            action="RECORD_SUPPLIER_QUOTE",
            resource_type="SUPPLIER_QUOTE",
            resource_id=str(quote.id),
            details={
                "product_id": product_id,
                "supplier": quote.supplier_name,
                "quoted_price_inr": quote.quoted_price_inr,
                "is_verified": quote.is_verified,
                "moq": quote.moq
            }
        )
        return quote

    def run(self, db: Session, product_id: int, **kwargs) -> Dict[str, Any]:
        """Audit supplier options for candidate product and list missing verification requirements."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        quotes = db.query(SupplierQuote).filter(
            SupplierQuote.product_id == product_id
        ).order_by(SupplierQuote.is_verified.desc(), SupplierQuote.quoted_price_inr.asc()).all()

        if not quotes:
            return {
                "product_id": product_id,
                "quotes_count": 0,
                "best_quote": None,
                "has_verified_supplier": False,
                "verification_checklist": [
                    "Search IndiaMART / TradeIndia for domestic manufacturers",
                    "Request sample unit to inspect physical build quality",
                    "Verify active GSTIN on CBIC portal",
                    "Negotiate MOQ and payment terms (e.g., 30% advance, 70% against dispatch)"
                ]
            }

        best = quotes[0]
        missing_verifications = []
        if not best.is_verified:
            missing_verifications.extend([
                "Confirm active GSTIN matches supplier business name",
                "Receive physical sample before placing initial inventory order",
                "Verify bank account name matches supplier invoice"
            ])

        return {
            "product_id": product_id,
            "quotes_count": len(quotes),
            "best_quote": {
                "id": best.id,
                "supplier_name": best.supplier_name,
                "quoted_price_inr": best.quoted_price_inr,
                "moq": best.moq,
                "is_verified": best.is_verified,
                "verification_method": best.verification_method,
                "lead_time_days": best.lead_time_days
            },
            "has_verified_supplier": best.is_verified,
            "manual_verification_required": missing_verifications
        }


supplier_agent = SupplierResearchAgent()
