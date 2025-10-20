from enum import Enum


class ProcessingType(str, Enum):
    """
    Enum for different data processing types
    Each type has different MongoDB collections and join logic
    """
    TYPE5 = "type5"              # Sales data processing
    # INVENTORY = "inventory"      # Inventory management
    # CUSTOMER = "customer"        # Customer data processing
    # PRODUCT = "product"          # Product catalog processing
    # FINANCIAL = "financial"      # Financial reports


class ProcessingConfig:
    """Configuration for each processing type"""

    CONFIGS = {
        ProcessingType.TYPE5: {
            "collections": ["T24_T24CORE_ACCOUNT", "T24_T24CORE_CUSTOMER", "BIZ_CORP_ACCT", "BIZ_CORP"], 
        },
        # ProcessingType.INVENTORY: {
        #     "collection": "inventory_reference",
        #     "join_key": "warehouse_id",
        #     "description": "Process inventory data with warehouse information"
        # },
        # ProcessingType.CUSTOMER: {
        #     "collection": "customer_reference",
        #     "join_key": "customer_id",
        #     "description": "Process customer data with profile information"
        # },
        # ProcessingType.PRODUCT: {
        #     "collection": "product_reference",
        #     "join_key": "category_id",
        #     "description": "Process product data with category information"
        # },
        # ProcessingType.FINANCIAL: {
        #     "collection": "financial_reference",
        #     "join_key": "account_id",
        #     "description": "Process financial data with account information"
        # }
    }

    @classmethod
    def get_config(cls, processing_type: ProcessingType) -> dict:
        """Get configuration for a processing type"""
        return cls.CONFIGS.get(processing_type, {})

    @classmethod
    def get_collection(cls, processing_type: ProcessingType) -> str:
        """Get MongoDB collection name for a processing type"""
        return cls.CONFIGS.get(processing_type, {}).get("collections", "reference_data")
