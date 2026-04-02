from pydantic import BaseModel, field_validator
from typing import Optional

class FuelPass(BaseModel):
    pass_id: Optional[str] = None
    vehicle_id: str
    fuel_type: str
    pass_code: str
    status: str

class FuelPassCreate(BaseModel):
    vehicle_id: str
    fuel_type: str

class FuelPassUpdate(BaseModel):
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value:
            value = value.upper()
            if value not in ["ACTIVE", "INACTIVE", "BLOCKED"]:
                raise ValueError("Invalid status")
        return value