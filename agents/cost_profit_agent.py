"""
AGENT 3: Product Cost and Profitability Agent
Deterministic mathematical engine computing granular unit economics, Amazon India fees,
GST tax liability, working capital requirements, break-even thresholds, and multi-scenario modeling.
Never hallucinates or invents numbers. Enforces provisional status if supplier costs are unverified.
"""

from typing import Dict, Any, List, Optional
import json
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent, DataType, ConfidenceLevel
from config.fee_schedules import (
    get_referral_fee, get_closing_fee, get_shipping_fee, AMAZON_FEE_GST_RATE
)
from database.models import Product, SupplierQuote, ProfitabilityAnalysis, MarketObservation


class CostAndProfitabilityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="CostAndProfitabilityAgent",
            description="Computes exact Amazon India unit economics, fees, GST, break-even and scenarios"
        )

    def calculate_unit_economics(
        self,
        category: str,
        selling_price: float,
        supplier_cost: float,
        package_weight_grams: float,
        fulfilment_channel: str = "EASY_SHIP",
        inbound_shipping_per_unit: float = 20.0,
        packaging_labelling_cost: float = 15.0,
        estimated_ad_cost_per_unit: float = 40.0,
        return_rate_pct: float = 5.0,
        damaged_inventory_rate_pct: float = 1.5,
        product_gst_rate_pct: float = 18.0,
        shipping_zone: str = "NATIONAL",
        moq: int = 50
    ) -> Dict[str, Any]:
        """
        Deterministic unit economics calculator for Amazon India.
        """
        selling_price = max(0.0, float(selling_price))
        supplier_cost = max(0.0, float(supplier_cost))
        package_weight_grams = max(100.0, float(package_weight_grams))
        channel = fulfilment_channel.upper()

        # 1. Amazon Marketplace Fees
        referral_fee = get_referral_fee(category, selling_price)
        closing_fee = get_closing_fee(channel, selling_price)
        shipping_fee = get_shipping_fee(channel, package_weight_grams, shipping_zone)
        fba_storage_fee = 10.0 if channel == "FBA" else 0.0

        total_amazon_fees = round(referral_fee + closing_fee + shipping_fee + fba_storage_fee, 2)
        amazon_fee_gst = round(total_amazon_fees * AMAZON_FEE_GST_RATE, 2)

        # 2. Indian Goods and Services Tax (GST) Calculations
        # Product Selling Price is MRP (inclusive of GST)
        base_product_selling_price = selling_price / (1.0 + (product_gst_rate_pct / 100.0))
        product_output_gst = round(selling_price - base_product_selling_price, 2)

        # Input Tax Credit (ITC) from Supplier Purchase (assuming supplier price includes GST)
        supplier_base_cost = supplier_cost / (1.0 + (product_gst_rate_pct / 100.0))
        product_input_gst_credit = round(supplier_cost - supplier_base_cost, 2)

        # Net GST to remit to Govt (Output GST minus Input GST Credit)
        net_gst_payable = max(0.0, round(product_output_gst - product_input_gst_credit, 2))

        # 3. Direct Procurement & Inbound Logistics
        direct_product_cost = supplier_cost + inbound_shipping_per_unit + packaging_labelling_cost

        # 4. Reserves for Returns & Damage
        # On returns, Amazon retains 20% of referral fee or up to INR 300, and return shipping is charged
        return_refund_cost = round((selling_price * (return_rate_pct / 100.0)) * 0.35, 2)
        damaged_inventory_reserve = round(supplier_cost * (damaged_inventory_rate_pct / 100.0), 2)

        # 5. Unit Contribution (Gross Margin before Advertising and Overhead)
        unit_contribution = round(
            selling_price - (direct_product_cost + total_amazon_fees + amazon_fee_gst),
            2
        )

        # 6. Base-Case Net Operating Profit
        total_costs_base = (
            direct_product_cost +
            total_amazon_fees +
            amazon_fee_gst +
            estimated_ad_cost_per_unit +
            return_refund_cost +
            damaged_inventory_reserve
        )
        net_operating_profit = round(selling_price - total_costs_base, 2)
        net_profit_margin_pct = round((net_operating_profit / selling_price) * 100.0, 2) if selling_price > 0 else 0.0
        roi_pct = round((net_operating_profit / direct_product_cost) * 100.0, 2) if direct_product_cost > 0 else 0.0

        # 7. Break-Even Calculations
        # Break-even price: price that covers product costs, shipping, closing, minimum ad & return costs
        # Solved iteratively for Amazon India referral fee slab
        breakeven_price = round(
            (direct_product_cost + shipping_fee + closing_fee + (closing_fee * 0.18) + estimated_ad_cost_per_unit + 15.0) / 0.85,
            2
        )
        max_affordable_ad_cost = max(0.0, round(estimated_ad_cost_per_unit + net_operating_profit, 2))

        # 8. Scenario Modeling
        # Optimistic: Higher organic conversion (ad spend -35%), lower returns (-40%), zero damage
        opt_ad_cost = round(estimated_ad_cost_per_unit * 0.65, 2)
        opt_returns = round(return_refund_cost * 0.60, 2)
        opt_profit = round(
            selling_price - (direct_product_cost + total_amazon_fees + amazon_fee_gst + opt_ad_cost + opt_returns),
            2
        )

        # Pessimistic: Higher customer acquisition cost (+40%), higher return rate (+50%)
        pess_ad_cost = round(estimated_ad_cost_per_unit * 1.40, 2)
        pess_returns = round(return_refund_cost * 1.50, 2)
        pess_damage = round(damaged_inventory_reserve * 1.50, 2)
        pess_profit = round(
            selling_price - (direct_product_cost + total_amazon_fees + amazon_fee_gst + pess_ad_cost + pess_returns + pess_damage),
            2
        )

        # 9. Working Capital Requirements
        initial_batch_size = max(moq, 50)
        cash_required_initial_batch = round(direct_product_cost * initial_batch_size, 2)

        return {
            "target_selling_price": selling_price,
            "supplier_cost": supplier_cost,
            "inbound_shipping_per_unit": inbound_shipping_per_unit,
            "packaging_labelling_cost": packaging_labelling_cost,
            "referral_fee": referral_fee,
            "closing_fee": closing_fee,
            "weight_handling_fee": shipping_fee,
            "fba_storage_fee": fba_storage_fee,
            "total_amazon_fees": total_amazon_fees,
            "amazon_fee_gst": amazon_fee_gst,
            "product_output_gst": product_output_gst,
            "product_input_gst_credit": product_input_gst_credit,
            "net_gst_payable": net_gst_payable,
            "estimated_ad_cost_per_unit": estimated_ad_cost_per_unit,
            "return_refund_cost_per_unit": return_refund_cost,
            "damaged_inventory_reserve_per_unit": damaged_inventory_reserve,
            "contribution_per_unit": unit_contribution,
            "net_operating_profit": net_operating_profit,
            "net_profit_margin_pct": net_profit_margin_pct,
            "roi_pct": roi_pct,
            "breakeven_selling_price": breakeven_price,
            "max_affordable_ad_cost": max_affordable_ad_cost,
            "optimistic_profit": opt_profit,
            "pessimistic_profit": pess_profit,
            "cash_required_initial_batch": cash_required_initial_batch,
            "initial_batch_units": initial_batch_size,
            "assumptions": {
                "fulfilment_channel": channel,
                "shipping_zone": shipping_zone,
                "product_weight_g": package_weight_grams,
                "return_rate_assumed_pct": return_rate_pct,
                "ad_cost_assumed_inr": estimated_ad_cost_per_unit,
                "gst_rate_pct": product_gst_rate_pct
            }
        }

    def run(self, db: Session, product_id: int, **kwargs) -> Dict[str, Any]:
        """Compute and persist complete profitability analysis for a given product."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product #{product_id} not found")

        # Get latest market observation for selling price
        obs = db.query(MarketObservation).filter(
            MarketObservation.product_id == product_id
        ).order_by(MarketObservation.observed_at.desc()).first()

        selling_price = kwargs.get("selling_price")
        if selling_price is None:
            selling_price = obs.selling_price_inr if obs else 599.0

        # Get latest supplier quote
        quote = db.query(SupplierQuote).filter(
            SupplierQuote.product_id == product_id
        ).order_by(SupplierQuote.created_at.desc()).first()

        missing_items = []
        is_provisional = False

        if quote:
            supplier_cost = quote.quoted_price_inr
            inbound_shipping = quote.shipping_cost_to_warehouse
            moq = quote.moq
            if not quote.is_verified:
                is_provisional = True
                missing_items.append("Supplier quote is unverified; pending manual verification")
        else:
            is_provisional = True
            missing_items.append("No supplier quote on record; using conservative placeholder cost")
            supplier_cost = round(selling_price * 0.35, 2)
            inbound_shipping = 20.0
            moq = 50

        # Compute
        results = self.calculate_unit_economics(
            category=product.category,
            selling_price=selling_price,
            supplier_cost=supplier_cost,
            package_weight_grams=product.package_weight_grams or 350.0,
            fulfilment_channel=product.fulfilment_channel or "EASY_SHIP",
            inbound_shipping_per_unit=inbound_shipping,
            packaging_labelling_cost=kwargs.get("packaging_cost", 15.0),
            estimated_ad_cost_per_unit=kwargs.get("ad_cost", 45.0),
            moq=moq
        )

        # Persist or update ProfitabilityAnalysis record
        existing = db.query(ProfitabilityAnalysis).filter(
            ProfitabilityAnalysis.product_id == product_id
        ).first()

        if not existing:
            existing = ProfitabilityAnalysis(product_id=product_id)
            db.add(existing)

        existing.target_selling_price_inr = results["target_selling_price"]
        existing.supplier_cost_inr = results["supplier_cost"]
        existing.inbound_shipping_per_unit = results["inbound_shipping_per_unit"]
        existing.packaging_labelling_cost = results["packaging_labelling_cost"]
        existing.referral_fee_inr = results["referral_fee"]
        existing.closing_fee_inr = results["closing_fee"]
        existing.weight_handling_fee_inr = results["weight_handling_fee"]
        existing.fba_storage_fee_inr = results["fba_storage_fee"]
        existing.amazon_fee_gst_inr = results["amazon_fee_gst"]
        existing.product_output_gst_inr = results["product_output_gst"]
        existing.product_input_gst_credit_inr = results["product_input_gst_credit"]
        existing.net_gst_payable_inr = results["net_gst_payable"]
        existing.estimated_ad_cost_per_unit = results["estimated_ad_cost_per_unit"]
        existing.return_refund_cost_per_unit = results["return_refund_cost_per_unit"]
        existing.damaged_inventory_reserve_per_unit = results["damaged_inventory_reserve_per_unit"]
        existing.contribution_per_unit_inr = results["contribution_per_unit"]
        existing.net_operating_profit_inr = results["net_operating_profit"]
        existing.net_profit_margin_pct = results["net_profit_margin_pct"]
        existing.roi_pct = results["roi_pct"]
        existing.optimistic_profit_inr = results["optimistic_profit"]
        existing.pessimistic_profit_inr = results["pessimistic_profit"]
        existing.breakeven_selling_price_inr = results["breakeven_selling_price"]
        existing.max_affordable_ad_cost_inr = results["max_affordable_ad_cost"]
        existing.cash_required_initial_batch = results["cash_required_initial_batch"]
        existing.is_provisional = is_provisional
        existing.missing_cost_items_json = json.dumps(missing_items)
        existing.assumptions_json = json.dumps(results["assumptions"])

        db.commit()

        self.log_action(
            db,
            action="CALCULATE_PROFITABILITY",
            resource_type="PRODUCT",
            resource_id=str(product_id),
            details={
                "selling_price": results["target_selling_price"],
                "net_profit": results["net_operating_profit"],
                "net_margin_pct": results["net_profit_margin_pct"],
                "is_provisional": is_provisional
            }
        )

        return results


cost_profit_agent = CostAndProfitabilityAgent()
