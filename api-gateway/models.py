from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class OwnerCreate(BaseModel):
    full_name: str
    nic: str
    mobile_no: str
    email: EmailStr
    address: str
    district: str

class OwnerUpdate(BaseModel):
    full_name: Optional[str] = None
    nic: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    district: Optional[str] = None

class VehicleCreate(BaseModel):
    owner_id: str
    vehicle_number: str
    vehicle_type: str
    brand: str
    model: str
    fuel_type: str

class VehicleUpdate(BaseModel):
    owner_id: Optional[str] = None
    vehicle_number: Optional[str] = None
    vehicle_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    fuel_type: Optional[str] = None

class FuelPassCreate(BaseModel):
    vehicle_id: str
    fuel_type: str

class FuelPassUpdate(BaseModel):
    status: Optional[str] = None

class TransactionCreate(BaseModel):
    pass_id: str
    vehicle_id: str
    litres_issued: float
    issued_datetime: datetime
    operator_name: str
    status: str

class TransactionUpdate(BaseModel):
    pass_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    litres_issued: Optional[float] = None
    issued_datetime: Optional[datetime] = None
    operator_name: Optional[str] = None
    status: Optional[str] = None