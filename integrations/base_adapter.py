"""
Base Marketplace Adapter Interface
Defines common contract for Amazon India, Flipkart, and Meesho.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime


class BaseMarketplaceAdapter(ABC):
    def __init__(self, marketplace_name: str, marketplace_id: str):
        self.marketplace_name = marketplace_name
        self.marketplace_id = marketplace_id

    @abstractmethod
    def get_connection_status(self) -> Dict[str, Any]:
        """Check whether credentials are valid and return granted roles/permissions."""
        pass

    @abstractmethod
    def fetch_product_pricing(self, item_id: str) -> Dict[str, Any]:
        """Retrieve real-time pricing and buy box status."""
        pass

    @abstractmethod
    def fetch_catalog_item(self, item_id: str) -> Dict[str, Any]:
        """Retrieve catalog details, dimensions, and category."""
        pass

    @abstractmethod
    def fetch_inventory_summaries(self, skus: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Retrieve current inventory levels."""
        pass

    @abstractmethod
    def publish_listing(self, sku: str, listing_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Publish or update a product listing (requires explicit human approval)."""
        pass
