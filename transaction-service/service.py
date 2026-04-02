from uuid import uuid4
from dotenv import load_dotenv
import os
import httpx
from db import get_collection

# Load .env
load_dotenv()

VEHICLE_SERVICE_URL = os.getenv("VEHICLE_SERVICE_URL")
FUEL_PASS_SERVICE_URL = os.getenv("FUEL_PASS_SERVICE_URL")


class TransactionService:
    def __init__(self):
        pass

    def _format_transaction(self, transaction):
        if not transaction:
            return None

        return {
            "id": str(transaction["_id"]),
            "transaction_id": transaction.get("transaction_id"),
            "pass_id": transaction.get("pass_id"),
            "vehicle_id": transaction.get("vehicle_id"),
            "litres_issued": transaction.get("litres_issued"),
            "issued_datetime": transaction.get("issued_datetime"),
            "operator_name": transaction.get("operator_name"),
            "status": transaction.get("status"),
        }

    # Get all transactions
    async def get_all(self):
        collection = get_collection()
        transactions = []

        async for transaction in collection.find():
            transactions.append(self._format_transaction(transaction))

        return transactions

    # Get transaction by transaction_id
    async def get_by_id(self, transaction_id: str):
        collection = get_collection()
        transaction = await collection.find_one({"transaction_id": transaction_id})
        return self._format_transaction(transaction)

    # Validate vehicle
    async def validate_vehicle(self, vehicle_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{VEHICLE_SERVICE_URL}/api/vehicles/{vehicle_id}"
                )
                return response.status_code == 200
        except Exception:
            return False

    # Validate fuel pass
    async def validate_pass(self, pass_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{FUEL_PASS_SERVICE_URL}/api/fuelpasses/{pass_id}"
                )
                return response.status_code == 200
        except Exception:
            return False

    # Add new transaction
    async def create(self, transaction_data):
        collection = get_collection()
        data = transaction_data.model_dump()

        # Validate vehicle
        if not await self.validate_vehicle(data["vehicle_id"]):
            return {"error": "Invalid vehicle_id"}

        # Validate fuel pass
        if not await self.validate_pass(data["pass_id"]):
            return {"error": "Invalid pass_id"}

        # Generate transaction_id if not provided
        if not data.get("transaction_id"):
            data["transaction_id"] = f"TXN-{uuid4().hex[:8].upper()}"

        # Check if transaction_id already exists
        existing_transaction = await collection.find_one(
            {"transaction_id": data["transaction_id"]}
        )
        if existing_transaction:
            return None

        result = await collection.insert_one(data)
        created_transaction = await collection.find_one({"_id": result.inserted_id})

        return self._format_transaction(created_transaction)

    # Update transaction
    async def update(self, transaction_id: str, transaction_data):
        collection = get_collection()
        update_data = transaction_data.model_dump(exclude_unset=True)

        # Validate vehicle only if updated
        if "vehicle_id" in update_data:
            if not await self.validate_vehicle(update_data["vehicle_id"]):
                return {"error": "Invalid vehicle_id"}

        # Validate pass only if updated
        if "pass_id" in update_data:
            if not await self.validate_pass(update_data["pass_id"]):
                return {"error": "Invalid pass_id"}

        result = await collection.update_one(
            {"transaction_id": transaction_id},
            {"$set": update_data}
        )

        if result.matched_count > 0:
            updated_transaction = await collection.find_one(
                {"transaction_id": transaction_id}
            )
            return self._format_transaction(updated_transaction)

        return None

    # Delete transaction
    async def delete(self, transaction_id: str):
        collection = get_collection()
        result = await collection.delete_one({"transaction_id": transaction_id})
        return result.deleted_count > 0