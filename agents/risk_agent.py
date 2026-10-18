"""
AGENT 5: Product Risk and Compliance Agent
Screens candidate products against Indian regulations and Amazon listing restrictions:
1. Indian Legal Metrology (Packaged Commodities) Rules, 2011 (Mandatory declarations)
2. Bureau of Indian Standards (BIS) Mandatory Certification Order
3. Trademark & Brand Infringement risk
4. Hazardous / Dangerous Goods (Hazmat) classification
5. Breakage fragility tiers (Glass/Ceramic)
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent, DataType, ConfidenceLevel, sanitize_untrusted_text
from database.models import Product, ComplianceCheck

# High-Risk / Restricted keywords on Amazon India
HAZMAT_KEYWORDS = ["battery", "lithium", "flammable", "aerosol", "solvent", "corrosive", "laser", "chemical"]
RESTRICTED_CATEGORIES = ["Grocery & Gourmet Foods", "Health & Personal Care", "Jewellery", "Fine Art"]
BIS_MANDATORY_CATEGORIES = ["Electronics", "Power Adapters", "Toys", "Steel Products", "Chemicals"]


class ProductRiskAndComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="ProductRiskAndComplianceAgent",
            description="Screens products for Amazon India category gating, BIS standards, trademark risks, and Metrology rules"
        )

    def evaluate_compliance(
        self,
        title: str,
        category: str,
        brand: str,
        fragility_tier: int = 1
    ) -> Dict[str, Any]:
        """Audit regulatory and platform safety."""
        title_lower = title.lower()
        rejection_flags = []
        mandatory_licences = [
            "Active GSTIN",
            "Legal Metrology Declaration (MRP, Net Qty, Month/Year of Pkg, Consumer Care Contact)"
        ]

        # 1. Hazmat check
        is_hazmat = any(kw in title_lower for kw in HAZMAT_KEYWORDS)
        if is_hazmat:
            rejection_flags.append("Contains Hazmat / Dangerous Goods keywords (batteries, chemicals, aerosols)")
            special_handling = "HAZMAT"
        elif fragility_tier >= 3:
            special_handling = "FRAGILE"
        else:
            special_handling = "STANDARD"

        # 2. BIS Certification Requirement
        needs_bis = any(cat.lower() in category.lower() for cat in BIS_MANDATORY_CATEGORIES) or "electric" in title_lower or "charger" in title_lower
        if needs_bis:
            mandatory_licences.append("BIS Registration (CRS / ISI Mark under Quality Control Orders)")

        # 3. Category Restriction / Gating
        is_restricted = category in RESTRICTED_CATEGORIES
        if is_restricted:
            mandatory_licences.append(f"Amazon Category Ungating Approval for '{category}' (Brand Authorisation or Purchase Invoices)")

        # 4. Trademark / Counterfeit Risk
        famous_brands = ["apple", "samsung", "nike", "adidas", "sony", "philips", "boat", "prestige", "milton", "pigeon"]
        trademark_risk_score = 0.0
        for b in famous_brands:
            if b in title_lower and (not brand or b not in brand.lower()):
                trademark_risk_score = 0.85
                rejection_flags.append(f"Potential trademark infringement of protected brand: '{b.title()}'")
                break

        # 5. Fragility check
        if fragility_tier >= 3:
            rejection_flags.append("High breakage fragility tier (Tier 3 Glass/Ceramic) requires drop-test certified thermocol packaging")

        is_safe = len(rejection_flags) == 0

        return {
            "is_safe_to_sell": is_safe,
            "category_restricted": is_restricted,
            "special_handling": special_handling,
            "trademark_risk_score": trademark_risk_score,
            "counterfeit_risk_score": 0.0,
            "fragility_tier": fragility_tier,
            "mandatory_licences": mandatory_licences,
            "rejection_flags": rejection_flags
        }

    def run(self, db: Session, product_id: int, **kwargs) -> Dict[str, Any]:
        """Perform compliance audit on product and update ComplianceCheck record."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        fragility_tier = int(kwargs.get("fragility_tier", 1))
        # Default fragility based on material keywords
        title_lower = product.title.lower()
        if "glass" in title_lower or "ceramic" in title_lower or "porcelain" in title_lower:
            fragility_tier = 3
        elif "plastic" in title_lower or "acrylic" in title_lower:
            fragility_tier = 2

        results = self.evaluate_compliance(
            title=product.title,
            category=product.category,
            brand=product.brand or "",
            fragility_tier=fragility_tier
        )

        existing = db.query(ComplianceCheck).filter(ComplianceCheck.product_id == product_id).first()
        if not existing:
            existing = ComplianceCheck(product_id=product_id)
            db.add(existing)

        existing.category_restricted = results["category_restricted"]
        existing.trademark_risk_score = results["trademark_risk_score"]
        existing.counterfeit_risk_score = results["counterfeit_risk_score"]
        existing.special_handling = results["special_handling"]
        existing.fragility_tier = results["fragility_tier"]
        existing.mandatory_licences_json = json.dumps(results["mandatory_licences"])
        existing.rejection_flags_json = json.dumps(results["rejection_flags"])
        existing.checked_at = datetime.utcnow()

        # Update product status if risk checked
        if product.status == "ANALYSED":
            product.status = "RISK_CHECKED"

        db.commit()

        self.log_action(
            db,
            action="COMPLIANCE_AUDIT",
            resource_type="PRODUCT",
            resource_id=str(product_id),
            details={
                "is_safe": results["is_safe_to_sell"],
                "special_handling": results["special_handling"],
                "flags": results["rejection_flags"]
            }
        )

        return results


risk_agent = ProductRiskAndComplianceAgent()
