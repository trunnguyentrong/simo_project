from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any
import pandas as pd
from loguru import logger
from ..config import settings


class MongoDBService:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        """Connect to MongoDB"""
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB]

    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()

    async def get_reference_data(
        self,
        collection_name: str = "reference_data",
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Get reference data from MongoDB for joining

        Args:
            collection_name: Name of the collection to query
            filters: Optional filters for the query

        Returns:
            List of documents from the collection
        """
        if filters is None:
            filters = {}

        collection = self.db[collection_name]
        cursor = collection.find(filters)
        return await cursor.to_list(length=None)

    async def get_multiple_collections(
        self,
        collection_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        """
        Get data from multiple collections at once

        Args:
            collection_names: List of collection names to query

        Returns:
            Dict with collection names as keys and DataFrames as values

        Example:
            result = {
                "sales": pd.DataFrame(...),
                "products": pd.DataFrame(...)
            }
        """
        results = {}

        for name in collection_names:
            collection = self.db[name]
            cursor = collection.find()
            data = await cursor.to_list(length=None)
            results[name] = pd.DataFrame(data)
        logger.info("Get data from mongodb Successfully !!!")

        return results

    async def save_processed_data(
        self,
        data: List[Dict[str, Any]],
        collection_name: str = "processed_data"
    ):
        """
        Save processed data to MongoDB

        Args:
            data: List of documents to save
            collection_name: Name of the collection to save to
        """
        if not data:
            return

        collection = self.db[collection_name]
        await collection.insert_many(data)


# Singleton instance
mongodb_service = MongoDBService()
