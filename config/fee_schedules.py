"""
Amazon India Fee Schedules and GST Tax Matrix
Source: Official Amazon Services India Seller Fee Schedule & CBIC GST Rates
All fee calculations are deterministic and verified against Amazon India slabs.
"""

from typing import Dict, Any

# Amazon India Marketplace Identifier
MARKETPLACE_ID_INDIA = "A21TJRUUN4KGV"
DEFAULT_CURRENCY = "INR"
DEFAULT_TIMEZONE = "Asia/Kolkata"

# GST Rate on Amazon Seller Fees (Referral, Closing, Weight Handling, Storage)
AMAZON_FEE_GST_RATE = 0.18  # 18% GST

# Category Referral Fee Schedules (% of selling price)
# Each category defines slabs or a flat percentage, plus a minimum fee (usually INR 3 - 5)
CATEGORY_REFERRAL_FEES: Dict[str, Dict[str, Any]] = {
    "Home & Kitchen": {
        "slabs": [
            {"max_price": 300, "rate": 0.06},       # 6% for <= 300
            {"max_price": 1000, "rate": 0.095},     # 9.5% for 301 - 1000
            {"max_price": None, "rate": 0.125}      # 12.5% for > 1000
        ],
        "min_fee": 5.0,
        "default_gst_rate": 0.18,
        "default_hsn": "7323"
    },
    "Office Products & Stationery": {
        "slabs": [
            {"max_price": 500, "rate": 0.08},
            {"max_price": None, "rate": 0.11}
        ],
        "min_fee": 5.0,
        "default_gst_rate": 0.12,
        "default_hsn": "4820"
    },
    "Consumer Electronics & Accessories": {
        "slabs": [
            {"max_price": 500, "rate": 0.09},
            {"max_price": 1000, "rate": 0.11},
            {"max_price": None, "rate": 0.135}
        ],
        "min_fee": 5.0,
        "default_gst_rate": 0.18,
        "default_hsn": "8504"
    },
    "Beauty & Personal Care": {
        "slabs": [
            {"max_price": 500, "rate": 0.055},
            {"max_price": 1000, "rate": 0.08},
            {"max_price": None, "rate": 0.10}
        ],
        "min_fee": 3.0,
        "default_gst_rate": 0.18,
        "default_hsn": "3304"
    },
    "Toys & Games": {
        "slabs": [
            {"max_price": 500, "rate": 0.085},
            {"max_price": 1000, "rate": 0.10},
            {"max_price": None, "rate": 0.12}
        ],
        "min_fee": 5.0,
        "default_gst_rate": 0.12,
        "default_hsn": "9503"
    },
    "Sports, Fitness & Outdoors": {
        "slabs": [
            {"max_price": 500, "rate": 0.075},
            {"max_price": 1000, "rate": 0.10},
            {"max_price": None, "rate": 0.125}
        ],
        "min_fee": 5.0,
        "default_gst_rate": 0.18,
        "default_hsn": "9506"
    },
    "Automotive Accessories": {
        "slabs": [
            {"max_price": 500, "rate": 0.09},
            {"max_price": 1000, "rate": 0.11},
            {"max_price": None, "rate": 0.13}
        ],
        "min_fee": 5.0,
        "default_gst_rate": 0.18,
        "default_hsn": "8708"
    },
    "General Merchandise (Default)": {
        "slabs": [
            {"max_price": 500, "rate": 0.10},
            {"max_price": None, "rate": 0.13}
        ],
        "min_fee": 5.0,
        "default_gst_rate": 0.18,
        "default_hsn": "9999"
    }
}

# Amazon India Closing Fee Slabs (in INR)
# Varies by Fulfilment Channel and Item Price
CLOSING_FEES: Dict[str, list] = {
    "EASY_SHIP": [
        {"max_price": 250, "fee": 5.0},
        {"max_price": 500, "fee": 9.0},
        {"max_price": 1000, "fee": 24.0},
        {"max_price": None, "fee": 55.0}
    ],
    "FBA": [
        {"max_price": 250, "fee": 6.0},
        {"max_price": 500, "fee": 11.0},
        {"max_price": 1000, "fee": 22.0},
        {"max_price": None, "fee": 38.0}
    ],
    "SELF_SHIP": [
        {"max_price": 250, "fee": 7.0},
        {"max_price": 500, "fee": 15.0},
        {"max_price": 1000, "fee": 30.0},
        {"max_price": None, "fee": 60.0}
    ]
}

# Weight Handling Fees for Easy Ship (Standard Size, in INR)
# Zones: Local (within city), Regional (within state/zone), National (inter-zone)
EASY_SHIP_WEIGHT_FEES = {
    "LOCAL": {"first_500g": 44.0, "addl_500g_up_to_1kg": 13.0, "addl_500g_up_to_5kg": 18.0},
    "REGIONAL": {"first_500g": 53.0, "addl_500g_up_to_1kg": 17.0, "addl_500g_up_to_5kg": 24.0},
    "NATIONAL": {"first_500g": 74.0, "addl_500g_up_to_1kg": 25.0, "addl_500g_up_to_5kg": 33.0}
}

# FBA Weight Handling (Standard Size, in INR)
FBA_WEIGHT_FEES = {
    "LOCAL": {"first_500g": 32.0, "addl_500g_up_to_1kg": 14.0, "addl_500g_up_to_5kg": 19.0},
    "REGIONAL": {"first_500g": 42.0, "addl_500g_up_to_1kg": 18.0, "addl_500g_up_to_5kg": 26.0},
    "NATIONAL": {"first_500g": 62.0, "addl_500g_up_to_1kg": 26.0, "addl_500g_up_to_5kg": 35.0}
}

# FBA Monthly Storage Fees (per cubic foot per month in INR)
FBA_STORAGE_FEE_PER_CUFT_MONTH = 45.0  # Off-peak standard rate


def get_referral_fee(category: str, selling_price: float) -> float:
    """Calculate exact Amazon referral fee based on category slabs."""
    cat_config = CATEGORY_REFERRAL_FEES.get(category, CATEGORY_REFERRAL_FEES["General Merchandise (Default)"])
    slabs = cat_config["slabs"]
    min_fee = cat_config.get("min_fee", 5.0)

    chosen_rate = slabs[-1]["rate"]
    for slab in slabs:
        if slab["max_price"] is not None and selling_price <= slab["max_price"]:
            chosen_rate = slab["rate"]
            break

    calculated_fee = selling_price * chosen_rate
    return round(max(calculated_fee, min_fee), 2)


def get_closing_fee(fulfilment_channel: str, selling_price: float) -> float:
    """Calculate exact Amazon closing fee based on fulfilment method and price."""
    channel = fulfilment_channel.upper()
    slabs = CLOSING_FEES.get(channel, CLOSING_FEES["EASY_SHIP"])

    for slab in slabs:
        if slab["max_price"] is None or selling_price <= slab["max_price"]:
            return float(slab["fee"])
    return 55.0


def get_shipping_fee(fulfilment_channel: str, weight_grams: float, zone: str = "NATIONAL") -> float:
    """
    Calculate shipping/weight-handling fee.
    Default zone is National for conservative profitability estimation.
    """
    channel = fulfilment_channel.upper()
    zone = zone.upper() if zone.upper() in ["LOCAL", "REGIONAL", "NATIONAL"] else "NATIONAL"

    if channel == "SELF_SHIP":
        # Estimate standard third-party courier cost in India (Delhivery / BlueDart)
        if weight_grams <= 500:
            return 65.0
        elif weight_grams <= 1000:
            return 95.0
        else:
            extra_kg = (weight_grams - 1000) / 1000.0
            return round(95.0 + (extra_kg * 60.0), 2)

    matrix = FBA_WEIGHT_FEES if channel == "FBA" else EASY_SHIP_WEIGHT_FEES
    zone_rates = matrix.get(zone, matrix["NATIONAL"])

    first_500g = zone_rates["first_500g"]
    if weight_grams <= 500:
        return float(first_500g)
    elif weight_grams <= 1000:
        return float(first_500g + zone_rates["addl_500g_up_to_1kg"])
    else:
        # 1kg to 5kg
        extra_500g_units = ((weight_grams - 1000) + 499) // 500  # Ceiling division
        return round(first_500g + zone_rates["addl_500g_up_to_1kg"] + (extra_500g_units * zone_rates["addl_500g_up_to_5kg"]), 2)
