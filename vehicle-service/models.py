from pydantic import BaseModel, field_validator
from typing import Optional, List, Any
import read_root


ALLOWED_FUEL_TYPES = ["petrol", "diesel", "electric", "hybrid"]


class Vehicle(BaseModel):
    vehicle_id: str
    owner_id: str
    vehicle_number: str
    vehicle_type: str
    brand: str
    model: str
    fuel_type: str


class VehicleCreate(BaseModel):
    owner_id: str
    vehicle_number: str
    vehicle_type: str
    brand: str
    model: str
    fuel_type: str


    @field_validator("vehicle_number")
    @classmethod
    def validate_vehicle_number(cls, value: str):
        value = value.strip().upper()
        if not re.match(r"^[A-Z0-9\- ]+$", value):
            raise ValueError("Invalid vehicle number format")
        return value


    @field_validator("fuel_type")
    @classmethod
    def validate_fuel_type(cls, value: str):
        value = value.strip().lower()
        if value not in ALLOWED_FUEL_TYPES:
            raise ValueError(f"fuel_type must be one of {ALLOWED_FUEL_TYPES}")
        return value


class VehicleUpdate(BaseModel):
    owner_id: Optional[str] = None
    vehicle_number: Optional[str] = None
    vehicle_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    fuel_type: Optional[str] = None


    @field_validator("vehicle_number")
    @classmethod
    def validate_vehicle_number(cls, value: Optional[str]):
        if value is None:
            return value
        value = value.strip().upper()
        if not re.match(r"^[A-Z0-9\-]+$", value):
            raise ValueError("Invalid vehicle number format")
        return value

    @field_validator("fuel_type")
    @classmethod
    def validate_fuel_type(cls, value: Optional[str]):
        if value is None:
            return value
        value = value.strip().lower()
        if value not in ALLOWED_FUEL_TYPES:
            raise ValueError(f"fuel_type must be one of {ALLOWED_FUEL_TYPES}")
        return value


class VehicleResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Vehicle] = None


class VehicleListResponse(BaseModel):
    success: bool
    message: str
    data: List[Vehicle]

class GenericResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None