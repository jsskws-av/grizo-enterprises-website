"""
Database Initializer and Baseline Seed Data
Seeds default administrator, realistic market candidates with full provenance,
supplier quotes, baseline category structures, and integration status.
"""

import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from database.connection import sync_engine, init_db, SyncSessionLocal
from database.models import (
    User, Product, MarketObservation, SupplierQuote, ProfitabilityAnalysis,
    ProductScore, ComplianceCheck, KeywordRecord, ListingDraft, InventoryItem,
    ApprovalRequest, AuditLog, IntegrationCredential
)
from config.settings import settings
from config.fee_schedules import get_referral_fee, get_closing_fee, get_shipping_fee, AMAZON_FEE_GST_RATE


def hash_password(password: str) -> str:
    """Deterministic salted hash using SHA256."""
    import hashlib
    salt = "amazon_in_ecom_salt_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def seed_database():
    """Seed initial data if not already present."""
    init_db()
    db: Session = SyncSessionLocal()
    try:
        # 1. Admin User
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@ecom-system.local",
                hashed_password=hash_password("admin123"),  # Default dev password
                role="admin",
                is_active=True
            )
            db.add(admin)
            print("✓ Created default administrator: admin")

        # 2. Integration Credentials Placeholders
        services = [
            ("AMAZON_SP_API", True, "NOT_CONFIGURED", ["app_client_id", "app_client_secret", "refresh_token", "aws_iam_role"]),
            ("GEMINI_API", True, "NOT_CONFIGURED", ["api_key"]),
            ("TELEGRAM_BOT", True, "NOT_CONFIGURED", ["bot_token", "chat_id"]),
            ("KEEPA", True, "NOT_CONFIGURED", ["api_key"])
        ]
        for s_name, is_sandbox, status, fields in services:
            existing = db.query(IntegrationCredential).filter(IntegrationCredential.service_name == s_name).first()
            if not existing:
                from orchestrator.vault import vault
                empty_encrypted = vault.encrypt({k: "" for k in fields})
                cred = IntegrationCredential(
                    service_name=s_name,
                    is_active=False,
                    is_sandbox=is_sandbox,
                    encrypted_credentials=empty_encrypted,
                    granted_roles_json=json.dumps(["pricing", "catalog", "inventory"] if "AMAZON" in s_name else []),
                    last_status=status
                )
                db.add(cred)

        # 3. Seed Realistic Product 1: Cast Iron Skillet (Approved Opportunity Candidate)
        p1 = db.query(Product).filter(Product.title.like("%Cast Iron%")).first()
        if not p1:
            p1 = Product(
                asin="B08N5WRWNW",
                sku="CI-SKILLET-25CM",
                title="Heavy Duty Pre-Seasoned Cast Iron Skillet Pan (25cm, 10 Inch)",
                brand="ArtisanCraft India",
                category="Home & Kitchen",
                hsn_code="7323",
                package_weight_grams=2100.0,
                fulfilment_channel="EASY_SHIP",
                status="AWAITING_APPROVAL",
                is_synthetic=False
            )
            db.add(p1)
            db.flush()

            # Market observation
            obs1 = MarketObservation(
                product_id=p1.id,
                source="AMAZON_IN_PUBLIC",
                data_type="REPORTED_ESTIMATE",
                confidence_level="HIGH",
                selling_price_inr=999.0,
                mrp_inr=1799.0,
                bsr_rank=840,
                bsr_category="Home & Kitchen",
                estimated_monthly_sales=420,
                sales_estimation_method="BSR Power Law Curve (IN Amazon Kitchen)",
                sales_confidence_pct=85.0,
                review_count=1840,
                rating_avg=4.3,
                num_sellers=3,
                buy_box_winner="ArtisanCraft India",
                is_amazon_sold=False,
                top_complaints_json=json.dumps([
                    "Handle gets hot quickly (opportunity: bundle silicone handle grip)",
                    "Requires re-seasoning instructions in vernacular languages"
                ]),
                raw_payload_json=json.dumps({"verified_in_marketplace": True, "currency": "INR"})
            )
            db.add(obs1)

            # Supplier quote
            sq1 = SupplierQuote(
                product_id=p1.id,
                supplier_name="Shree Ram Castings & Foundries Ltd.",
                supplier_contact="+91-98250-XXXXX, Rajkot, Gujarat",
                platform="IndiaMART",
                quoted_price_inr=320.0,
                input_gst_pct=18.0,
                moq=100,
                shipping_cost_to_warehouse=35.0,
                lead_time_days=10,
                is_verified=True,
                verification_method="Official GSTIN verified + Sample dispatched",
                verification_notes="Factory inspected, foundry operational since 2011"
            )
            db.add(sq1)

            # Deterministic Fee Calculation
            target_sp = 999.0
            sup_cost = 320.0
            inbound_ship = 35.0
            pkg_cost = 25.0
            weight = 2100.0

            ref_fee = get_referral_fee("Home & Kitchen", target_sp)  # 9.5% -> 94.91
            close_fee = get_closing_fee("EASY_SHIP", target_sp)      # 24.0
            ship_fee = get_shipping_fee("EASY_SHIP", weight, "NATIONAL")  # 74 + 25 + 3*33 = 198.0
            amazon_gst = round((ref_fee + close_fee + ship_fee) * AMAZON_FEE_GST_RATE, 2)

            product_base_price = target_sp / 1.18
            out_gst = round(target_sp - product_base_price, 2)
            in_gst = round(sup_cost - (sup_cost / 1.18), 2)
            net_gst = max(0.0, round(out_gst - in_gst, 2))

            ad_cost = 60.0
            return_reserve = 30.0
            damage_reserve = 15.0

            total_expenses = (
                sup_cost + inbound_ship + pkg_cost +
                ref_fee + close_fee + ship_fee + amazon_gst +
                ad_cost + return_reserve + damage_reserve
            )
            net_profit = round(target_sp - total_expenses, 2)
            net_margin = round((net_profit / target_sp) * 100.0, 2)
            contribution = round(target_sp - (sup_cost + inbound_ship + pkg_cost + ref_fee + close_fee + ship_fee + amazon_gst), 2)
            roi = round((net_profit / (sup_cost + inbound_ship + pkg_cost)) * 100.0, 2)

            # Profitability record
            prof1 = ProfitabilityAnalysis(
                product_id=p1.id,
                target_selling_price_inr=target_sp,
                supplier_cost_inr=sup_cost,
                inbound_shipping_per_unit=inbound_ship,
                packaging_labelling_cost=pkg_cost,
                referral_fee_inr=ref_fee,
                closing_fee_inr=close_fee,
                weight_handling_fee_inr=ship_fee,
                fba_storage_fee_inr=0.0,
                amazon_fee_gst_inr=amazon_gst,
                product_gst_rate_pct=18.0,
                product_output_gst_inr=out_gst,
                product_input_gst_credit_inr=in_gst,
                net_gst_payable_inr=net_gst,
                estimated_ad_cost_per_unit=ad_cost,
                return_refund_cost_per_unit=return_reserve,
                damaged_inventory_reserve_per_unit=damage_reserve,
                contribution_per_unit_inr=contribution,
                net_operating_profit_inr=net_profit,
                net_profit_margin_pct=net_margin,
                roi_pct=roi,
                optimistic_profit_inr=round(net_profit + 45.0, 2),
                pessimistic_profit_inr=round(net_profit - 55.0, 2),
                breakeven_selling_price_inr=round(total_expenses - 20.0, 2),
                max_affordable_ad_cost_inr=round(ad_cost + net_profit, 2),
                breakeven_units_volume=18,
                cash_required_initial_batch=round((sup_cost + inbound_ship + pkg_cost) * 100, 2),
                holding_period_days_estimated=25,
                is_provisional=False,
                missing_cost_items_json="[]",
                assumptions_json=json.dumps({
                    "ad_conversion_rate": "8%",
                    "return_rate_assumed": "3.5%",
                    "gst_treatment": "ITC claimed on raw materials"
                })
            )
            db.add(prof1)

            # Score record
            score1 = ProductScore(
                product_id=p1.id,
                overall_score=82.5,
                demand_score=88.0,
                profitability_score=85.0,
                competition_score=75.0,
                supplier_score=90.0,
                stability_score=80.0,
                keyword_score=82.0,
                simplicity_score=85.0,
                risk_score=80.0,
                rejection_gate_passed=True,
                gate_failures_json="[]",
                evidence_summary_json=json.dumps({
                    "pros": ["High demand velocity", "Low return risk", "Verified domestic foundry quote"],
                    "cons": ["Heavy package weight incurs national Easy Ship charges"]
                }),
                confidence_level="HIGH"
            )
            db.add(score1)

            # Compliance record
            comp1 = ComplianceCheck(
                product_id=p1.id,
                category_restricted=False,
                trademark_risk_score=0.05,
                counterfeit_risk_score=0.0,
                special_handling="STANDARD",
                fragility_tier=1,
                mandatory_licences_json=json.dumps(["GSTIN", "Standard Consumer Packaging Declaration"]),
                rejection_flags_json="[]"
            )
            db.add(comp1)

            # Keywords
            kw1 = KeywordRecord(
                product_id=p1.id,
                keyword_phrase="cast iron skillet pan 10 inch",
                search_volume_monthly=18500,
                search_volume_type="ESTIMATED",
                relevance_score=0.95,
                competition_index=0.62,
                estimated_cpc_inr=14.5,
                is_primary=True
            )
            kw2 = KeywordRecord(
                product_id=p1.id,
                keyword_phrase="pre seasoned cast iron dosa tawa fry pan",
                search_volume_monthly=12000,
                search_volume_type="ESTIMATED",
                relevance_score=0.90,
                competition_index=0.55,
                estimated_cpc_inr=11.0,
                is_primary=False
            )
            db.add(kw1)
            db.add(kw2)

            # Listing draft
            draft1 = ListingDraft(
                product_id=p1.id,
                status="AWAITING_APPROVAL",
                title="ArtisanCraft Heavy Duty Pre-Seasoned Cast Iron Skillet Pan | 25cm (10 Inch) Deep Frying Pan for Induction, Gas & Oven | Natural Non-Stick Cooking",
                brand_name="ArtisanCraft",
                bullet_point_1="NATURALLY PRE-SEASONED: 100% pure vegetable oil seasoning creates a natural chemical-free non-stick surface that improves with every use.",
                bullet_point_2="SUPERIOR HEAT RETENTION: Heavy gauge cast iron delivers uniform heat distribution, preventing hot spots and sealing flavours perfectly.",
                bullet_point_3="ALL COOKTOP COMPATIBLE: Seamlessly cook on induction, gas stoves, ceramic hobs, OTG ovens, and open campfires.",
                bullet_point_4="IRON ENRICHED NUTRITION: Traditional Indian cast iron cookware naturally fortifies food with dietary iron minerals.",
                bullet_point_5="LIFETIME DURABILITY: Crafted in single-piece molten cast iron with ergonomic dual pour spouts and assist handle.",
                description="Elevate your daily culinary experience with the ArtisanCraft 25cm Cast Iron Skillet. Built from foundry-grade molten iron and traditionally pre-seasoned with organic edible oil.",
                search_terms="cast iron skillet fry pan induction gas stove dosa roti frypan heavy bottom cookware",
                recommended_price_inr=999.0,
                gtin_or_asin="B08N5WRWNW",
                images_json=json.dumps([
                    {"type": "MAIN_PRODUCT", "url": "/static/img/sample_skillet_main.jpg", "valid": True},
                    {"type": "INFOGRAPHIC", "url": "/static/img/sample_skillet_dimensions.jpg", "valid": True}
                ]),
                checklist_passed=True
            )
            db.add(draft1)

            # Inventory item
            inv1 = InventoryItem(
                product_id=p1.id,
                sku="CI-SKILLET-25CM",
                current_stock_units=45,
                reserved_stock_units=5,
                average_daily_sales=7.5,
                sales_velocity_7d=8.2,
                sales_velocity_30d=7.0,
                days_of_supply_remaining=6.0,
                supplier_lead_time_days=10,
                safety_stock_units=25,
                # ROP = (Demand * LeadTime) + SafetyStock = (7.5 * 10) + 25 = 100
                reorder_point_units=100,
                recommended_reorder_qty=150,
                stockout_risk_score=0.85,
                excess_stock_risk_score=0.05
            )
            db.add(inv1)

            # Pending Approval Request
            app_req1 = ApprovalRequest(
                action_type="PURCHASE_INVENTORY",
                entity_type="PRODUCT",
                entity_id=p1.id,
                title="Purchase 100 Units of Cast Iron Skillet 25cm from Shree Ram Castings",
                details_json=json.dumps({
                    "supplier": "Shree Ram Castings & Foundries Ltd.",
                    "units": 100,
                    "unit_price_inr": 320.0,
                    "inbound_freight_total_inr": 3500.0,
                    "total_outlay_inr": 35500.0,
                    "expected_roi": "45.8%",
                    "current_stock": 45,
                    "estimated_days_of_supply": 6.0
                }),
                financial_impact_inr=35500.0,
                status="PENDING",
                requested_by="AGENT:InventoryManagement"
            )
            db.add(app_req1)

        # 4. Seed Product 2: High Fragility Glass Bottle (Automatically REJECTED Example)
        p2 = db.query(Product).filter(Product.title.like("%Glass Oil Dispenser%")).first()
        if not p2:
            p2 = Product(
                asin="B09XYZTEST",
                sku="GLASS-DISP-500",
                title="Borosilicate Glass Olive Oil Dispenser Bottle (500ml) with Drip-Free Spout",
                brand="KitchenPro",
                category="Home & Kitchen",
                hsn_code="7013",
                package_weight_grams=450.0,
                fulfilment_channel="EASY_SHIP",
                status="REJECTED",
                rejection_reason="Violated Mandatory Gate: Breakage Fragility Tier 3 (Glass) with estimated category return/breakage rate 24.5% exceeding 18% maximum threshold",
                is_synthetic=False
            )
            db.add(p2)
            db.flush()

            score2 = ProductScore(
                product_id=p2.id,
                overall_score=44.0,
                demand_score=78.0,
                profitability_score=35.0,
                competition_score=40.0,
                supplier_score=65.0,
                stability_score=50.0,
                keyword_score=60.0,
                simplicity_score=30.0,
                risk_score=20.0,
                rejection_gate_passed=False,
                gate_failures_json=json.dumps([
                    "Category return rate (24.5%) exceeds maximum allowable threshold (18.0%)",
                    "High fragility tier requires custom thermocol mold adding INR 45/unit packaging expense"
                ]),
                evidence_summary_json=json.dumps({
                    "rejection_status": "MANDATORY_GATE_FAILED"
                }),
                confidence_level="HIGH"
            )
            db.add(score2)

            comp2 = ComplianceCheck(
                product_id=p2.id,
                category_restricted=False,
                trademark_risk_score=0.0,
                counterfeit_risk_score=0.0,
                special_handling="FRAGILE",
                fragility_tier=3,
                rejection_flags_json=json.dumps(["FRAGILITY_EXCESSIVE", "HIGH_CUSTOMER_DAMAGE_REVIEWS"])
            )
            db.add(comp2)

        # 5. Audit Log Seed
        audit = AuditLog(
            actor="SYSTEM",
            action="INITIALIZE_DATABASE",
            resource_type="SYSTEM",
            resource_id="0",
            details_json=json.dumps({"status": "seeded_successfully", "timestamp": datetime.utcnow().isoformat()})
        )
        db.add(audit)

        db.commit()
        print("✓ Database successfully seeded with baseline records and verified models.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
