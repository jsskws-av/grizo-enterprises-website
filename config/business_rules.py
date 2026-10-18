"""
Configurable Business Rules, Scoring Weights, and Mandatory Rejection Thresholds
All rules are inspectable, user-customizable, and enforced deterministically.
"""

from typing import Dict, Any, Literal
from pydantic import BaseModel, Field


class ScoringWeights(BaseModel):
    """Configurable weights for product opportunity scoring (sum = 1.0)."""
    demand_evidence: float = Field(default=0.25, ge=0.0, le=1.0)
    profitability: float = Field(default=0.25, ge=0.0, le=1.0)
    competition: float = Field(default=0.15, ge=0.0, le=1.0)
    supplier_reliability: float = Field(default=0.10, ge=0.0, le=1.0)
    sales_pricing_stability: float = Field(default=0.10, ge=0.0, le=1.0)
    keyword_opportunity: float = Field(default=0.05, ge=0.0, le=1.0)
    operational_simplicity: float = Field(default=0.05, ge=0.0, le=1.0)
    return_compliance_risk: float = Field(default=0.05, ge=0.0, le=1.0)


class RejectionThresholds(BaseModel):
    """
    Mandatory gates: Products failing ANY of these thresholds are instantly rejected,
    regardless of how high their numerical score might be.
    """
    min_net_profit_margin_pct: float = Field(default=15.0, description="Minimum base-case net profit margin %")
    min_contribution_per_unit_inr: float = Field(default=50.0, description="Minimum absolute contribution in INR")
    min_roi_pct: float = Field(default=25.0, description="Minimum return on invested capital %")
    max_estimated_return_rate_pct: float = Field(default=18.0, description="Maximum acceptable category return rate %")
    max_fragility_tier: int = Field(default=3, description="1=Low (fabric), 2=Medium (plastic), 3=High (glass/ceramic)")
    require_verified_supplier_quote: bool = Field(default=True, description="Cannot recommend for purchase without verified quote")
    reject_hazmat_and_restricted: bool = Field(default=True, description="Instantly reject Hazmat/Dangerous Goods")
    reject_trademark_infringements: bool = Field(default=True, description="Reject unauthorized branded items")


class OperationalGuardrails(BaseModel):
    """Hard safeguards controlling what the system can do automatically."""
    emergency_stop_active: bool = Field(default=False, description="Global write-freeze circuit breaker")
    automated_pricing_enabled: bool = Field(default=False, description="Whether automated repricing is active")
    max_price_drop_pct: float = Field(default=10.0, description="Maximum permitted price reduction in one step")
    max_price_increase_pct: float = Field(default=15.0, description="Maximum permitted price increase in one step")
    max_daily_ad_spend_inr: float = Field(default=500.0, description="Hard cap on daily advertising spend")
    auto_publish_approved_listings: bool = Field(default=True, description="Publish only once status is APPROVED")
    # HARDCODED PROHIBITION: Never allow automated purchasing
    automated_purchasing_allowed: Literal[False] = Field(default=False, description="STRICTLY FALSE: Orders require human signature")


DEFAULT_SCORING_WEIGHTS = ScoringWeights()
DEFAULT_REJECTION_THRESHOLDS = RejectionThresholds()
DEFAULT_OPERATIONAL_GUARDRAILS = OperationalGuardrails()
