"""
Script to seed MongoDB with sample data
Run: python scripts/seed_mongodb.py
"""

from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGODB_URL = "mongodb://admin:password@localhost:27017"
DB_NAME = "data_processing"

def seed_data():
    client = MongoClient(MONGODB_URL)
    db = client[DB_NAME]

    # Sample reference data
    reference_data = [
        {
            "id": "P001",
            "name": "Laptop Dell XPS 13",
            "category": "Electronics",
            "price": 1299.99,
            "stock": 50,
            "supplier": "Dell Inc."
        },
        {
            "id": "P002",
            "name": "iPhone 15 Pro",
            "category": "Electronics",
            "price": 999.99,
            "stock": 100,
            "supplier": "Apple Inc."
        },
        {
            "id": "P003",
            "name": "Nike Air Max",
            "category": "Clothing",
            "price": 149.99,
            "stock": 200,
            "supplier": "Nike"
        },
        {
            "id": "P004",
            "name": "Samsung Galaxy S24",
            "category": "Electronics",
            "price": 899.99,
            "stock": 75,
            "supplier": "Samsung"
        },
        {
            "id": "P005",
            "name": "Sony WH-1000XM5",
            "category": "Electronics",
            "price": 399.99,
            "stock": 120,
            "supplier": "Sony"
        }
    ]

    # Clear existing data
    db.reference_data.delete_many({})

    # Insert new data
    result = db.reference_data.insert_many(reference_data)

    print(f"✅ Seeded {len(result.inserted_ids)} reference records to MongoDB")

    # Show inserted data
    for doc in db.reference_data.find():
        print(f"  - {doc['id']}: {doc['name']}")

    client.close()

if __name__ == "__main__":
    seed_data()
