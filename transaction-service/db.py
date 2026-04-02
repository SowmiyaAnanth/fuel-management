from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing in .env file")

if not DB_NAME:
    raise ValueError("DATABASE_NAME is missing in .env file")


# Create MongoDB client 
client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]


# Get Collection
def get_collection():
    return database[COLLECTION_NAME]

