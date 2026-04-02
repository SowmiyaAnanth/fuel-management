from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any


class TransactionBase(BaseModel):
    pass_id: str
    vehicle_id: str
    litres_issued: float
    issued_datetime: datetime
    operator_name: str
    status: Optional[str] = None


class TransactionCreate(BaseModel):
    pass_id: str
    vehicle_id: str
    litres_issued: float
    issued_datetime: datetime
    operator_name: str


class TransactionUpdate(BaseModel):
    pass_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    litres_issued: Optional[float] = None
    issued_datetime: Optional[datetime] = None
    operator_name: Optional[str] = None
    status: Optional[str] = None


class Transaction(TransactionBase):
    transaction_id: str


class TransactionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class TransactionListResponse(BaseModel):
    success: bool
    message: str
    data: List[Transaction]