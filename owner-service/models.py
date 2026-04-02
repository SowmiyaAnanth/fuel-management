from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Any
import re

class Owner(BaseModel):
    owner_id: str
    full_name: str
    nic: str
    mobile_no: str
    email: EmailStr
    address: str
    district: str

class OwnerCreate(BaseModel):
    full_name: str
    nic: str
    mobile_no: str
    email: EmailStr
    address: str
    district: str

    @field_validator("full_name", "address", "district")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value
    
    @field_validator("nic")
    @classmethod
    def validate_nic(cls, value: str) -> str:
        value = value.strip().upper()

        old_pattern = r"^\d{9}[VX]$"
        new_pattern = r"^\d{12}$"

        if not (re.match(old_pattern, value) or re.match(new_pattern, value)):
            raise ValueError("Invalid NIC format")
        
        return value
    
    @field_validator("mobile_no")
    @classmethod
    def validate_mobile(cls, value: str) -> str:
        value = value.strip()

        if not re.match(r"^07\d{8}$", value):
            raise ValueError("Invalid mobile number (07XXXXXXXX)")
        
        return value
    
class OwnerUpdate(BaseModel):
    full_name: Optional[str] = None
    nic: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    district: Optional[str] = None

    @field_validator("full_name", "address", "district")
    @classmethod
    def validate_not_empty(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value
    
    @field_validator("nic")
    @classmethod
    def validate_nic(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        
        value = value.strip().upper()
        old_pattern = r"^\d{9}[VX]$"
        new_pattern = r"^\d{12}$"

        if not (re.match(old_pattern, value) or re.match(new_pattern, value)):
            raise ValueError("Invalid NIC format")
        
        return value
    
    @field_validator("mobile_no")
    @classmethod
    def validate_mobile(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        
        value = value.strip()
        if not re.match(r"^07\d{8}$", value):
            raise ValueError("Invalid mobile number")
        
        return value
    
class OwnerResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Owner] = None

class OwnerListResponse(BaseModel):
    success: bool
    message: str
    data: List[Owner]

class GenericResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


