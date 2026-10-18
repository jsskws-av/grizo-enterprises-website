"""
Product Research, Candidate Ingestion, Pipeline Trigger and Comparison Routes
"""

from typing import List, Optional, Dict, Any
import json
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from database.connection import get_sync_db
from database.models import (
    Product, MarketObservation, SupplierQuote, ProfitabilityAnalysis,
    ProductScore, ComplianceCheck, KeywordRecord, ListingDraft, InventoryItem
)
from orchestrator.engine import orchestrator
from agents.discovery_agent import discovery_agent
from agents.supplier_agent import supplier_agent

router = APIRouter(prefix="/api/products", tags=["Products"])


class CreateProductRequest(BaseModel):
    title: str
    category: str = "Home & Kitchen"
    selling_price: float
    mrp_inr: Optional[float] = None
    brand: Optional[str] = "Generic"
    asin: Optional[str] = None
    hsn_code: Optional[str] = None
    package_weight_grams: float = 350.0
    fulfilment_channel: str = "EASY_SHIP"
    bsr_rank: Optional[int] = None
    review_count: int = 0
    rating_avg: float = 0.0
    num_sellers: int = 1
    supplier_name: Optional[str] = None
    supplier_quoted_price: Optional[float] = None
    supplier_moq: int = 50
    supplier_is_verified: bool = False


@router.get("")
def list_products(
    status: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "score"  # score, margin, created_at, price
):
    db = get_sync_db()
    try:
        query = db.query(Product)
        if status:
            query = query.filter(Product.status == status)
        if category:
            query = query.filter(Product.category == category)
        if search:
            query = query.filter(Product.title.ilike(f"%{search}%"))

        products = query.all()
        results = []
        for p in products:
            score_val = p.score.overall_score if p.score else 0.0
            margin_val = p.profitability.net_profit_margin_pct if p.profitability else 0.0
            selling_price = p.profitability.target_selling_price_inr if p.profitability else (
                p.observations[0].selling_price_inr if p.observations else 0.0
            )

            results.append({
                "id": p.id,
                "asin": p.asin,
                "sku": p.sku,
                "title": p.title,
                "category": p.category,
                "status": p.status,
                "rejection_reason": p.rejection_reason,
                "overall_score": score_val,
                "gate_passed": p.score.rejection_gate_passed if p.score else True,
                "net_margin_pct": margin_val,
                "selling_price_inr": selling_price,
                "created_at": p.created_at.strftime("%Y-%m-%d %H:%M")
            })

        # Sorting
        if sort_by == "score":
            results.sort(key=lambda x: x["overall_score"], reverse=True)
        elif sort_by == "margin":
            results.sort(key=lambda x: x["net_margin_pct"], reverse=True)
        elif sort_by == "price":
            results.sort(key=lambda x: x["selling_price_inr"], reverse=True)
        else:
            results.sort(key=lambda x: x["id"], reverse=True)

        return results
    finally:
        db.close()


@router.get("/{product_id}")
def get_product_details(product_id: int):
    db = get_sync_db()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        obs = product.observations[-1] if product.observations else None
        prof = product.profitability
        score = product.score
        comp = product.compliance
        quote = product.supplier_quotes[-1] if product.supplier_quotes else None
        draft = product.listing_draft
        inv = product.inventory

        return {
            "id": product.id,
            "asin": product.asin,
            "sku": product.sku,
            "title": product.title,
            "brand": product.brand,
            "category": product.category,
            "hsn_code": product.hsn_code,
            "weight_grams": product.package_weight_grams,
            "fulfilment_channel": product.fulfilment_channel,
            "status": product.status,
            "rejection_reason": product.rejection_reason,
            "is_synthetic": product.is_synthetic,
            "observation": {
                "source": obs.source if obs else "NONE",
                "data_type": obs.data_type if obs else "NONE",
                "confidence": obs.confidence_level if obs else "LOW",
                "selling_price_inr": obs.selling_price_inr if obs else 0.0,
                "mrp_inr": obs.mrp_inr if obs else 0.0,
                "bsr_rank": obs.bsr_rank if obs else None,
                "estimated_monthly_sales": obs.estimated_monthly_sales if obs else 0,
                "sales_method": obs.sales_estimation_method if obs else None,
                "review_count": obs.review_count if obs else 0,
                "rating_avg": obs.rating_avg if obs else 0.0,
                "num_sellers": obs.num_sellers if obs else 1,
                "observed_at": obs.observed_at.strftime("%Y-%m-%d %H:%M") if obs else None
            } if obs else None,
            "supplier_quote": {
                "id": quote.id if quote else None,
                "supplier_name": quote.supplier_name if quote else "None",
                "quoted_price_inr": quote.quoted_price_inr if quote else 0.0,
                "moq": quote.moq if quote else 0,
                "is_verified": quote.is_verified if quote else False,
                "verification_method": quote.verification_method if quote else "None",
                "lead_time_days": quote.lead_time_days if quote else 7
            } if quote else None,
            "profitability": {
                "target_price": prof.target_selling_price_inr if prof else 0.0,
                "supplier_cost": prof.supplier_cost_inr if prof else 0.0,
                "referral_fee": prof.referral_fee_inr if prof else 0.0,
                "closing_fee": prof.closing_fee_inr if prof else 0.0,
                "weight_fee": prof.weight_handling_fee_inr if prof else 0.0,
                "amazon_gst": prof.amazon_fee_gst_inr if prof else 0.0,
                "net_profit": prof.net_operating_profit_inr if prof else 0.0,
                "net_margin_pct": prof.net_profit_margin_pct if prof else 0.0,
                "roi_pct": prof.roi_pct if prof else 0.0,
                "breakeven_price": prof.breakeven_selling_price_inr if prof else 0.0,
                "max_ad_cost": prof.max_affordable_ad_cost_inr if prof else 0.0,
                "is_provisional": prof.is_provisional if prof else True,
                "missing_items": json.loads(prof.missing_cost_items_json) if prof and prof.missing_cost_items_json else []
            } if prof else None,
            "score": {
                "overall": score.overall_score if score else 0.0,
                "demand": score.demand_score if score else 0.0,
                "profitability": score.profitability_score if score else 0.0,
                "competition": score.competition_score if score else 0.0,
                "supplier": score.supplier_score if score else 0.0,
                "stability": score.stability_score if score else 0.0,
                "keyword": score.keyword_score if score else 0.0,
                "simplicity": score.simplicity_score if score else 0.0,
                "risk": score.risk_score if score else 0.0,
                "gate_passed": score.rejection_gate_passed if score else True,
                "gate_failures": json.loads(score.gate_failures_json) if score and score.gate_failures_json else []
            } if score else None,
            "compliance": {
                "restricted": comp.category_restricted if comp else False,
                "special_handling": comp.special_handling if comp else "STANDARD",
                "fragility_tier": comp.fragility_tier if comp else 1,
                "mandatory_licences": json.loads(comp.mandatory_licences_json) if comp and comp.mandatory_licences_json else [],
                "flags": json.loads(comp.rejection_flags_json) if comp and comp.rejection_flags_json else []
            } if comp else None,
            "draft": {
                "id": draft.id if draft else None,
                "title": draft.title if draft else None,
                "status": draft.status if draft else "NONE",
                "recommended_price": draft.recommended_price_inr if draft else 0.0
            } if draft else None,
            "inventory": {
                "current_stock": inv.current_stock_units if inv else 0,
                "days_of_supply": inv.days_of_supply_remaining if inv else 0.0,
                "reorder_point": inv.reorder_point_units if inv else 0,
                "safety_stock": inv.safety_stock_units if inv else 0
            } if inv else None
        }
    finally:
        db.close()


@router.post("")
def create_product(req: CreateProductRequest):
    db = get_sync_db()
    try:
        # Run discovery agent
        disc_res = discovery_agent.run(
            db=db,
            title=req.title,
            category=req.category,
            selling_price=req.selling_price,
            mrp_inr=req.mrp_inr,
            brand=req.brand,
            asin=req.asin,
            hsn_code=req.hsn_code,
            package_weight_grams=req.package_weight_grams,
            fulfilment_channel=req.fulfilment_channel,
            bsr_rank=req.bsr_rank,
            review_count=req.review_count,
            rating_avg=req.rating_avg,
            num_sellers=req.num_sellers
        )
        product_id = disc_res["product_id"]

        # If supplier details provided, record quote
        if req.supplier_name and req.supplier_quoted_price:
            supplier_agent.record_supplier_quote(
                db=db,
                product_id=product_id,
                supplier_name=req.supplier_name,
                quoted_price_inr=req.supplier_quoted_price,
                moq=req.supplier_moq,
                is_verified=req.supplier_is_verified
            )

        # Trigger full evaluation pipeline
        pipeline_res = orchestrator.evaluate_product_pipeline(db, product_id)
        return {
            "product_id": product_id,
            "title": req.title,
            "pipeline": pipeline_res
        }
    finally:
        db.close()


@router.post("/{product_id}/evaluate")
def evaluate_product(product_id: int):
    db = get_sync_db()
    try:
        res = orchestrator.evaluate_product_pipeline(db, product_id)
        return res
    finally:
        db.close()


@router.get("/compare/batch")
def compare_products(ids: str = Query(..., description="Comma separated product IDs")):
    id_list = [int(i.strip()) for i in ids.split(",") if i.strip().isdigit()]
    db = get_sync_db()
    try:
        products = db.query(Product).filter(Product.id.in_(id_list)).all()
        data = []
        for p in products:
            prof = p.profitability
            obs = p.observations[-1] if p.observations else None
            score = p.score
            data.append({
                "id": p.id,
                "title": p.title,
                "category": p.category,
                "status": p.status,
                "overall_score": score.overall_score if score else 0.0,
                "gate_passed": score.rejection_gate_passed if score else True,
                "selling_price": prof.target_selling_price_inr if prof else (obs.selling_price_inr if obs else 0.0),
                "supplier_cost": prof.supplier_cost_inr if prof else 0.0,
                "net_margin_pct": prof.net_profit_margin_pct if prof else 0.0,
                "net_profit_inr": prof.net_operating_profit_inr if prof else 0.0,
                "roi_pct": prof.roi_pct if prof else 0.0,
                "estimated_monthly_sales": obs.estimated_monthly_sales if obs else 0,
                "review_count": obs.review_count if obs else 0,
                "rating": obs.rating_avg if obs else 0.0
            })
        return data
    finally:
        db.close()
