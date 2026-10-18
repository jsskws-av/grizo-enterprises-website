"""
Relational Database Models for AI E-Commerce Management System
Built using SQLAlchemy 2.0 Declarative Base.
Strictly separates actual market data from estimates and AI hypotheses.
"""

from datetime import datetime
from typing import Optional, List
import json

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, Index, Enum
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(32), default="admin", nullable=False)  # admin, operator, viewer
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asin = Column(String(32), index=True, nullable=True)  # Target or competitor ASIN
    sku = Column(String(64), unique=True, nullable=True, index=True)
    title = Column(String(500), nullable=False)
    brand = Column(String(100), nullable=True)
    category = Column(String(100), nullable=False, default="Home & Kitchen")
    hsn_code = Column(String(16), nullable=True)
    package_weight_grams = Column(Float, default=350.0)
    fulfilment_channel = Column(String(32), default="EASY_SHIP")  # EASY_SHIP, FBA, SELF_SHIP
    
    # Lifecycle Workflow Status:
    # DISCOVERED -> ANALYSED -> RISK_CHECKED -> AWAITING_APPROVAL -> APPROVED -> ACTION_EXECUTED -> REJECTED
    status = Column(String(32), default="DISCOVERED", index=True, nullable=False)
    rejection_reason = Column(Text, nullable=True)
    is_synthetic = Column(Boolean, default=False, nullable=False)  # Explicit synthetic test flag
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    observations = relationship("MarketObservation", back_populates="product", cascade="all, delete-orphan")
    supplier_quotes = relationship("SupplierQuote", back_populates="product", cascade="all, delete-orphan")
    profitability = relationship("ProfitabilityAnalysis", back_populates="product", uselist=False, cascade="all, delete-orphan")
    score = relationship("ProductScore", back_populates="product", uselist=False, cascade="all, delete-orphan")
    compliance = relationship("ComplianceCheck", back_populates="product", uselist=False, cascade="all, delete-orphan")
    keywords = relationship("KeywordRecord", back_populates="product", cascade="all, delete-orphan")
    listing_draft = relationship("ListingDraft", back_populates="product", uselist=False, cascade="all, delete-orphan")
    inventory = relationship("InventoryItem", back_populates="product", uselist=False, cascade="all, delete-orphan")


class MarketObservation(Base):
    __tablename__ = "market_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    source = Column(String(64), nullable=False)  # SP_API, AMAZON_IN_PUBLIC, KEEPA, GOOGLE_TRENDS, MANUAL
    
    # Rigorous Data Classification: ACTUAL vs REPORTED_ESTIMATE vs AI_HYPOTHESIS
    data_type = Column(String(32), default="REPORTED_ESTIMATE", nullable=False)
    confidence_level = Column(String(16), default="MEDIUM")  # HIGH, MEDIUM, LOW
    
    selling_price_inr = Column(Float, nullable=False)
    mrp_inr = Column(Float, nullable=True)
    bsr_rank = Column(Integer, nullable=True)
    bsr_category = Column(String(100), nullable=True)
    
    estimated_monthly_sales = Column(Integer, nullable=True)
    sales_estimation_method = Column(String(100), nullable=True)  # e.g. "BSR Power Law Curve (IN)", "SP-API Reports"
    sales_confidence_pct = Column(Float, default=70.0)
    
    review_count = Column(Integer, default=0)
    rating_avg = Column(Float, default=0.0)
    num_sellers = Column(Integer, default=1)
    buy_box_winner = Column(String(100), nullable=True)
    is_amazon_sold = Column(Boolean, default=False)
    
    top_complaints_json = Column(Text, default="[]")
    raw_payload_json = Column(Text, default="{}")
    
    observed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    product = relationship("Product", back_populates="observations")


class SupplierQuote(Base):
    __tablename__ = "supplier_quotes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    supplier_name = Column(String(150), nullable=False)
    supplier_contact = Column(String(200), nullable=True)
    platform = Column(String(64), default="IndiaMART")  # IndiaMART, TradeIndia, Direct_Factory
    
    quoted_price_inr = Column(Float, nullable=False)
    input_gst_pct = Column(Float, default=18.0)  # GST rate paid to supplier
    moq = Column(Integer, default=50)  # Minimum order quantity
    
    shipping_cost_to_warehouse = Column(Float, default=0.0)
    lead_time_days = Column(Integer, default=7)
    
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_method = Column(String(100), default="Pending manual phone/invoice confirmation")
    verification_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="supplier_quotes")


class ProfitabilityAnalysis(Base):
    __tablename__ = "profitability_analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True, index=True)
    
    target_selling_price_inr = Column(Float, nullable=False)
    supplier_cost_inr = Column(Float, nullable=False)
    inbound_shipping_per_unit = Column(Float, default=15.0)
    packaging_labelling_cost = Column(Float, default=12.0)
    
    # Amazon Fees
    referral_fee_inr = Column(Float, nullable=False)
    closing_fee_inr = Column(Float, nullable=False)
    weight_handling_fee_inr = Column(Float, nullable=False)
    fba_storage_fee_inr = Column(Float, default=0.0)
    
    # Taxes
    amazon_fee_gst_inr = Column(Float, nullable=False)  # 18% on Amazon fees
    product_gst_rate_pct = Column(Float, default=18.0)
    product_output_gst_inr = Column(Float, nullable=False)
    product_input_gst_credit_inr = Column(Float, nullable=False)
    net_gst_payable_inr = Column(Float, nullable=False)
    
    # Operating & Risk Reserves
    estimated_ad_cost_per_unit = Column(Float, default=40.0)
    return_refund_cost_per_unit = Column(Float, default=25.0)
    damaged_inventory_reserve_per_unit = Column(Float, default=10.0)
    
    # Financial Output Metrics (Base Case)
    contribution_per_unit_inr = Column(Float, nullable=False)
    net_operating_profit_inr = Column(Float, nullable=False)
    net_profit_margin_pct = Column(Float, nullable=False)
    roi_pct = Column(Float, nullable=False)
    
    # Scenario Modeling
    optimistic_profit_inr = Column(Float, nullable=False)
    pessimistic_profit_inr = Column(Float, nullable=False)
    
    breakeven_selling_price_inr = Column(Float, nullable=False)
    max_affordable_ad_cost_inr = Column(Float, nullable=False)
    breakeven_units_volume = Column(Integer, default=10)
    
    # Working Capital
    cash_required_initial_batch = Column(Float, nullable=False)
    holding_period_days_estimated = Column(Integer, default=30)
    
    is_provisional = Column(Boolean, default=False)
    missing_cost_items_json = Column(Text, default="[]")
    assumptions_json = Column(Text, default="{}")
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="profitability")


class ProductScore(Base):
    __tablename__ = "product_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True, index=True)
    
    overall_score = Column(Float, nullable=False)  # 0 to 100
    
    demand_score = Column(Float, default=0.0)
    profitability_score = Column(Float, default=0.0)
    competition_score = Column(Float, default=0.0)
    supplier_score = Column(Float, default=0.0)
    stability_score = Column(Float, default=0.0)
    keyword_score = Column(Float, default=0.0)
    simplicity_score = Column(Float, default=0.0)
    risk_score = Column(Float, default=0.0)
    
    rejection_gate_passed = Column(Boolean, default=True, nullable=False)
    gate_failures_json = Column(Text, default="[]")
    evidence_summary_json = Column(Text, default="{}")
    
    confidence_level = Column(String(16), default="MEDIUM")
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="score")


class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True, index=True)
    
    category_restricted = Column(Boolean, default=False)
    trademark_risk_score = Column(Float, default=0.0)  # 0.0 (Safe) to 1.0 (Infringement risk)
    counterfeit_risk_score = Column(Float, default=0.0)
    special_handling = Column(String(32), default="STANDARD")  # STANDARD, HAZMAT, BATTERY, LIQUID, FRAGILE
    
    fragility_tier = Column(Integer, default=1)  # 1=Low, 2=Medium, 3=High
    mandatory_licences_json = Column(Text, default="[]")  # e.g. BIS, FSSAI, CDSCO
    rejection_flags_json = Column(Text, default="[]")
    
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="compliance")


class KeywordRecord(Base):
    __tablename__ = "keyword_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    keyword_phrase = Column(String(200), nullable=False)
    search_volume_monthly = Column(Integer, nullable=True)
    search_volume_type = Column(String(32), default="ESTIMATED")  # EXACT, ESTIMATED, AI_GENERATED
    relevance_score = Column(Float, default=0.8)
    competition_index = Column(Float, default=0.5)  # 0.0 low to 1.0 high
    estimated_cpc_inr = Column(Float, default=12.0)
    is_primary = Column(Boolean, default=False)
    
    discovered_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="keywords")


class ListingDraft(Base):
    __tablename__ = "listing_drafts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True, index=True)
    
    status = Column(String(32), default="DRAFT", index=True, nullable=False)  # DRAFT, AWAITING_APPROVAL, APPROVED, PUBLISHED
    title = Column(String(250), nullable=False)
    brand_name = Column(String(100), default="Generic")
    
    bullet_point_1 = Column(String(500), nullable=True)
    bullet_point_2 = Column(String(500), nullable=True)
    bullet_point_3 = Column(String(500), nullable=True)
    bullet_point_4 = Column(String(500), nullable=True)
    bullet_point_5 = Column(String(500), nullable=True)
    
    description = Column(Text, nullable=True)
    search_terms = Column(String(250), nullable=True)  # Amazon 249 byte limit
    
    recommended_price_inr = Column(Float, nullable=False)
    gtin_or_asin = Column(String(64), nullable=True)
    
    images_json = Column(Text, default="[]")
    checklist_passed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="listing_draft")


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Action types requiring human approval:
    # PURCHASE_INVENTORY, PAY_SUPPLIER, PUBLISH_LISTING, CREATE_AD_CAMPAIGN, INCREASE_AD_BUDGET, CHANGE_PRICE, DELETE_PRODUCT
    action_type = Column(String(64), nullable=False, index=True)
    entity_type = Column(String(32), default="PRODUCT")  # PRODUCT, INVENTORY, PRICING, CAMPAIGN
    entity_id = Column(Integer, nullable=False)
    title = Column(String(250), nullable=False)
    
    details_json = Column(Text, nullable=False)  # JSON payload with costs, quantities, proposed changes
    financial_impact_inr = Column(Float, default=0.0)
    
    status = Column(String(32), default="PENDING", index=True, nullable=False)  # PENDING, APPROVED, REJECTED, EXECUTED, CANCELLED
    requested_by = Column(String(64), default="AGENT:ListingCreation")
    
    decision_notes = Column(Text, nullable=True)
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True, index=True)
    sku = Column(String(64), unique=True, nullable=False)
    
    current_stock_units = Column(Integer, default=0, nullable=False)
    reserved_stock_units = Column(Integer, default=0, nullable=False)
    
    average_daily_sales = Column(Float, default=0.0)
    sales_velocity_7d = Column(Float, default=0.0)
    sales_velocity_30d = Column(Float, default=0.0)
    
    days_of_supply_remaining = Column(Float, default=0.0)
    supplier_lead_time_days = Column(Integer, default=7)
    safety_stock_units = Column(Integer, default=15)
    
    # Reorder Point = (Demand during Lead Time) + Safety Stock
    reorder_point_units = Column(Integer, default=25)
    recommended_reorder_qty = Column(Integer, default=50)
    
    stockout_risk_score = Column(Float, default=0.0)  # 0 to 1
    excess_stock_risk_score = Column(Float, default=0.0)
    
    last_replenished_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="inventory")


class DailyReportRecord(Base):
    __tablename__ = "daily_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_date = Column(String(16), unique=True, nullable=False, index=True)  # YYYY-MM-DD
    summary_text = Column(Text, nullable=False)
    metrics_json = Column(Text, default="{}")
    top_opportunities_json = Column(Text, default="[]")
    urgent_actions_json = Column(Text, default="[]")
    replenishment_alerts_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    actor = Column(String(64), nullable=False)  # USER, AGENT:Discovery, SCHEDULER, SYSTEM
    action = Column(String(64), nullable=False, index=True)
    resource_type = Column(String(32), nullable=False)
    resource_id = Column(String(64), nullable=True)
    details_json = Column(Text, default="{}")
    ip_address = Column(String(45), default="127.0.0.1")


class IntegrationCredential(Base):
    __tablename__ = "integration_credentials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(64), unique=True, nullable=False, index=True)  # AMAZON_SP_API, GEMINI_API, TELEGRAM_BOT, KEEPA
    is_active = Column(Boolean, default=False, nullable=False)
    is_sandbox = Column(Boolean, default=True, nullable=False)
    
    encrypted_credentials = Column(Text, nullable=False)
    granted_roles_json = Column(Text, default="[]")
    
    last_synced_at = Column(DateTime, nullable=True)
    last_status = Column(String(32), default="NOT_CONFIGURED")  # NOT_CONFIGURED, CONNECTED, ERROR, RATE_LIMITED
    error_message = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
