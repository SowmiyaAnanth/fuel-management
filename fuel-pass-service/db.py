import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not MONGO_URI:
    raise ValueError("MONGO_URI is required in .env or environment")

if not DB_NAME:
    raise ValueError("DB_NAME is missing in .env file")

if not COLLECTION_NAME:
    raise ValueError("COLLECTION_NAME is missing in .env file")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
Fuel_Collection = db[COLLECTION_NAME]

print("MongoDB Connected")
print("Collection:", COLLECTION_NAME)
print("MongoDB URI:", MONGO_URI)