import os
import uuid
import qrcode
import httpx
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError
from db import Fuel_Collection as Collection
from models import FuelPassCreate

VEHICLE_SERVICE_URL = "http://localhost:8002"


class FuelPassService:
    def _format_fuel_pass(self, fuel_pass):
        if not fuel_pass:
            return None

        return {
            "pass_id": str(fuel_pass["_id"]),
            "vehicle_id": fuel_pass.get("vehicle_id"),
            "fuel_type": fuel_pass.get("fuel_type"),
            "pass_code": fuel_pass.get("pass_code"),
            "qr_text": fuel_pass.get("qr_text"),
            "qr_image": fuel_pass.get("qr_image"),
            "status": fuel_pass.get("status")
        }
    #create
    async def create(self, data: FuelPassCreate):
        try:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(
                        f"{VEHICLE_SERVICE_URL}/api/vehicles/{data.vehicle_id}"
                    )
                except httpx.RequestError as e:
                    raise RuntimeError(f"Vehicle service unavailable: {str(e)}")

            if response.status_code == 404:
                raise ValueError("Vehicle not found")

            if response.status_code != 200:
                raise RuntimeError("Failed to fetch vehicle details from vehicle service")

            vehicle_payload = response.json()
            vehicle = vehicle_payload.get("data")

            if not vehicle:
                raise ValueError("Vehicle data not found")

            # validate fuel type with vehicle service record
            vehicle_fuel_type = vehicle.get("fuel_type")
            if not vehicle_fuel_type:
                raise RuntimeError("Vehicle service response missing fuel_type")
            
            vehicle_number = vehicle.get("vehicle_number")
            if not vehicle_number:
                raise RuntimeError("Vehicle service response missing vehicle_number")

            if vehicle_fuel_type != data.fuel_type:
                raise ValueError("Fuel type does not match vehicle record")

            existing = Collection.find_one({"vehicle_id": data.vehicle_id})
            if existing:
                raise ValueError("Fuel pass for vehicle already exists")

            pass_code = str(uuid.uuid4())[:8]
            qr_text = f"FP-{data.vehicle_id}-{pass_code}"

        #  create folder for QR codes if not exists
            if not os.path.exists("qrcodes"):
                os.makedirs("qrcodes")

        #  generate qr image
            safe_vehicle_number = vehicle_number.replace(" ", "_").replace("-", "_")
            qr_filename = f"{safe_vehicle_number}.png"
            img = qrcode.make(qr_text)
            img.save(f"qrcodes/{qr_filename}")

        #  save to db
            new_pass = {
                "vehicle_id": data.vehicle_id,
                "fuel_type": data.fuel_type,
                "pass_code": pass_code,
                "qr_text": qr_text,
                "qr_image": f"qrcodes/{qr_filename}",
                "status": "ACTIVE"
            }

            result =  Collection.insert_one(new_pass)
            created_pass =  Collection.find_one({"_id": result.inserted_id})
            return self._format_fuel_pass(created_pass)
        
        except ValueError:
            raise
        except DuplicateKeyError:
            raise ValueError("Fuel pass already exists for this vehicle")
        except Exception as e:
            raise RuntimeError(f"Failed to create fuel pass: {str(e)}")

    #Get_all
    async def get_all(self):
        try:
            passes = []
            for p in Collection.find():
                passes.append(self._format_fuel_pass(p))
            return passes
        except Exception as e:
            raise RuntimeError(f"Failed to fetch fuel passes: {str(e)}")

    #Get_by_id
    async def get_by_id(self, pass_id: str):
        try:
            fuel_pass =  Collection.find_one({"_id": ObjectId(pass_id)})
            return self._format_fuel_pass(fuel_pass)
        except InvalidId:
            raise ValueError("Invalid fuel pass ID")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch fuel passes: {str(e)}")


    #Update
    async def update_fuel_pass(self, pass_id: str, fuel_pass_data):
        try:
            update_data = fuel_pass_data.dict(exclude_unset=True)

            if not update_data:
                raise ValueError("No fields provided for update")

            result =  Collection.update_one(
                {"_id": ObjectId(pass_id)},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                return None

            updated_fuel_pass = Collection.find_one({"_id": ObjectId(pass_id)})
            return self._format_fuel_pass(updated_fuel_pass)

        except InvalidId:
            raise ValueError("Invalid fuel pass ID")
        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to update fuel pass: {str(e)}")

    # Delete
    async def delete_fuel_pass(self, pass_id: str):
        try:
            result = Collection.delete_one({"_id": ObjectId(pass_id)})
            return result.deleted_count > 0
        except InvalidId:
            raise ValueError("Invalid fuel pass ID")
        except Exception as e:
            raise RuntimeError(f"Failed to delete fuel pass: {str(e)}")

    # Generate_QR
    async def generate_qr(self, data: str, filename: str):
        try:
            os.makedirs("qrcodes", exist_ok=True)
            img = qrcode.make(data)
            img.save(f"qrcodes/{filename}.png")
        except Exception as e:
            raise RuntimeError(f"Failed to generate QR: {str(e)}")



