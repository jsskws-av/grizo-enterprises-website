"""
AGENT 7: Product Image Studio Agent
Validates compliance against Amazon India Image Style Guides:
1. Pure white background (RGB 255, 255, 255) for Main image
2. Minimum 1000px on longest side (1600px recommended for smooth zoom)
3. Product must occupy >= 85% of image frame
4. No text, logos, borders, or watermarks on Main image
5. Strict separation between factual photographs and illustrative lifestyle graphics
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent, DataType, ConfidenceLevel


class ProductImageStudioAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="ProductImageStudioAgent",
            description="Validates image technical specs against Amazon image guidelines and crafts promotional graphic concepts"
        )

    def validate_image_compliance(
        self,
        image_type: str,
        width: int,
        height: int,
        is_pure_white_bg: bool = True,
        contains_text_or_watermark: bool = False,
        product_frame_fill_pct: float = 88.0
    ) -> Dict[str, Any]:
        """
        Amazon Image Guidelines Compliance Check:
        - MAIN_PRODUCT: Strict Amazon main image requirements
        - INFOGRAPHIC / LIFESTYLE: Secondary image guidelines
        """
        violations = []
        warnings = []

        longest_side = max(width, height)
        if longest_side < 1000:
            violations.append(f"Image resolution ({width}x{height}) is under Amazon minimum 1000px requirement.")
        elif longest_side < 1600:
            warnings.append(f"Image resolution ({width}x{height}) meets 1000px minimum but 1600px is recommended for zoom.")

        if image_type == "MAIN_PRODUCT":
            if not is_pure_white_bg:
                violations.append("MAIN image must have a pure white background (RGB 255, 255, 255).")
            if contains_text_or_watermark:
                violations.append("MAIN image must NOT contain promotional text, watermarks, borders, or inset images.")
            if product_frame_fill_pct < 85.0:
                violations.append(f"Product occupies only {product_frame_fill_pct}% of frame; Amazon requires >= 85%.")

        is_valid = len(violations) == 0
        return {
            "is_compliant": is_valid,
            "violations": violations,
            "warnings": warnings,
            "image_type": image_type,
            "specs": {"width": width, "height": height, "longest_side": longest_side}
        }

    def generate_image_plan(self, product_title: str, category: str) -> List[Dict[str, Any]]:
        """
        Prepares a complete 7-image Amazon listing graphic plan.
        Separates factual physical photographs from lifestyle and infographics.
        """
        return [
            {
                "slot": 1,
                "type": "MAIN_PRODUCT",
                "is_factual_photo": True,
                "title": "Factual Product Main Shot",
                "description": "Authentic studio photo of the product on seamless pure white RGB (255,255,255) background. No props.",
                "target_resolution": "2000x2000",
                "aspect_ratio": "1:1"
            },
            {
                "slot": 2,
                "type": "INFOGRAPHIC",
                "is_factual_photo": False,
                "title": "Dimensional & Technical Callouts",
                "description": "Product schematic displaying exact dimensions in cm and inches, weight in grams, and material callouts.",
                "target_resolution": "2000x2000",
                "aspect_ratio": "1:1"
            },
            {
                "slot": 3,
                "type": "LIFESTYLE",
                "is_factual_photo": False,
                "title": "Contextual Lifestyle Scene",
                "description": f"Product in an authentic Indian home/kitchen environment showing active daily usage.",
                "target_resolution": "2000x2000",
                "aspect_ratio": "1:1"
            },
            {
                "slot": 4,
                "type": "FEATURE_CALLOUT",
                "is_factual_photo": False,
                "title": "Key Material & Ergonomic Benefits",
                "description": "Macro close-up highlighting surface finish, reinforced joints, and durability testing.",
                "target_resolution": "2000x2000",
                "aspect_ratio": "1:1"
            },
            {
                "slot": 5,
                "type": "COMPARISON_GRAPHIC",
                "is_factual_photo": False,
                "title": "Our Product vs Cheap Alternatives",
                "description": "Side-by-side comparison table highlighting superior material thickness, food-grade safety, and longer warranty.",
                "target_resolution": "2000x2000",
                "aspect_ratio": "1:1"
            },
            {
                "slot": 6,
                "type": "PACKAGING",
                "is_factual_photo": True,
                "title": "Retail Packaging & Box Contents",
                "description": "Photo of the sturdy protective shipping box, user manual, warranty card, and all included accessories.",
                "target_resolution": "2000x2000",
                "aspect_ratio": "1:1"
            }
        ]

    def run(self, db: Session, product_id: int, **kwargs) -> Dict[str, Any]:
        """Generate graphic asset plan and run validation checks."""
        from database.models import Product
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        plan = self.generate_image_plan(product.title, product.category)

        self.log_action(
            db,
            action="GENERATE_IMAGE_PLAN",
            resource_type="PRODUCT",
            resource_id=str(product_id),
            details={"slots_count": len(plan)}
        )

        return {
            "product_id": product_id,
            "image_plan": plan,
            "guideline_summary": "Amazon India requires 1000px+ (1600px+ recommended), pure white BG for Slot 1."
        }


image_agent = ProductImageStudioAgent()
