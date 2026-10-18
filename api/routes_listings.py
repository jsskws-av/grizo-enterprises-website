"""
Listing Drafts, Bullet Optimization, and Image Studio API
"""

from typing import List, Optional, Dict, Any
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.connection import get_sync_db
from database.models import ListingDraft, Product
from agents.listing_agent import listing_agent
from agents.image_agent import image_agent

router = APIRouter(prefix="/api/listings", tags=["Listings"])


class UpdateListingDraftRequest(BaseModel):
    title: str
    brand_name: str
    bullet_point_1: str
    bullet_point_2: str
    bullet_point_3: str
    bullet_point_4: str
    bullet_point_5: str
    description: str
    search_terms: str
    recommended_price_inr: float


@router.get("")
def list_drafts():
    db = get_sync_db()
    try:
        drafts = db.query(ListingDraft).all()
        return [
            {
                "id": d.id,
                "product_id": d.product_id,
                "title": d.title,
                "brand": d.brand_name,
                "category": d.product.category if d.product else "General",
                "recommended_price_inr": d.recommended_price_inr,
                "status": d.status,
                "checklist_passed": d.checklist_passed,
                "bullets": [d.bullet_point_1, d.bullet_point_2, d.bullet_point_3, d.bullet_point_4, d.bullet_point_5],
                "search_terms": d.search_terms,
                "search_terms_bytes": len((d.search_terms or "").encode("utf-8")),
                "updated_at": d.updated_at.strftime("%Y-%m-%d %H:%M")
            }
            for d in drafts
        ]
    finally:
        db.close()


@router.get("/{product_id}/images")
def get_image_plan(product_id: int):
    db = get_sync_db()
    try:
        return image_agent.run(db, product_id)
    finally:
        db.close()


@router.post("/{product_id}/regenerate")
def regenerate_listing(product_id: int):
    db = get_sync_db()
    try:
        return listing_agent.run(db, product_id)
    finally:
        db.close()
