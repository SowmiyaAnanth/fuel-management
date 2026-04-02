import os
import httpx
from dotenv import load_dotenv
from bson import ObjectId
from bson.errors import InvalidId
from db import vehicle_collection

load_dotenv()

OWNER_SERVICE_URL = os.getenv("OWNER_SERVICE_URL", "http://localhost:8001/api/owners")


class VehicleService:
    def __init__(self):
        pass

    def _format_vehicle(self, vehicle):
        if not vehicle:
            return None

        return {
            "vehicle_id": str(vehicle["_id"]),
            "owner_id": vehicle.get("owner_id"),
            "vehicle_number": vehicle.get("vehicle_number"),
            "vehicle_type": vehicle.get("vehicle_type"),
            "brand": vehicle.get("brand"),
            "model": vehicle.get("model"),
            "fuel_type": vehicle.get("fuel_type"),
        }

    def _is_valid_object_id(self, value: str):
        try:
            ObjectId(value)
            return True
        except InvalidId:
            return False

    def verify_owner_exists(self, owner_id: str) -> bool:
        try:
            response = httpx.get(f"{OWNER_SERVICE_URL}/{owner_id}", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False

    def get_all(self):
        vehicles = vehicle_collection.find()
        return [self._format_vehicle(v) for v in vehicles]

    def get_by_id(self, vehicle_id: str):
        if not self._is_valid_object_id(vehicle_id):
            return None

        vehicle = vehicle_collection.find_one({"_id": ObjectId(vehicle_id)})
        return self._format_vehicle(vehicle)

    def  get_by_owner(self, owner_id: str):
        vehicles = vehicle_collection.find({"owner_id": owner_id})
        return [self._format_vehicle(v) for v in vehicles]

    def create (self, vehicle_data):
        if not self.verify_owner_exists(vehicle_data.owner_id):
            return None, "Owner not found"

        data_dict = vehicle_data.model_dump()

        existing = vehicle_collection.find_one({
            "vehicle_number": data_dict["vehicle_number"]
        })
        if existing:
            return None, "Vehicle number already registered"

        result = vehicle_collection.insert_one(data_dict)
        new_vehicle = vehicle_collection.find_one({"_id": result.inserted_id})
        return self._format_vehicle(new_vehicle), None

    def update(self, vehicle_id: str, vehicle_data):
        if not self._is_valid_object_id(vehicle_id):
            return None

        update_dict = vehicle_data.model_dump(exclude_unset=True)

        if not update_dict:
            return "NO_FIELDS"

        if "owner_id" in update_dict:
            if not self.verify_owner_exists(update_dict["owner_id"]):
                return "OWNER_NOT_FOUND"
        
        if "vehicle_number" in update_dict:
            existing = vehicle_collection.find_one({
                "vehicle_number": update_dict["vehicle_number"],
                "_id": {"$ne": ObjectId(vehicle_id)}
            })
            if existing:
                return "VEHICLE_NUMBER_EXISTS"

            result = vehicle_collection.update_one(
                {"_id": ObjectId(vehicle_id)},
                {"$set": update_dict}
            )

            if result.matched_count == 0:
                return None

            updated = vehicle_collection.find_one({"_id": ObjectId(vehicle_id)})
            return self._format_vehicle(updated)

    def delete (self, vehicle_id: str):
        if not self._is_valid_object_id(vehicle_id):
            return False

        result = vehicle_collection.delete_one({"_id": ObjectId(vehicle_id)})
        return result.deleted_count > 0