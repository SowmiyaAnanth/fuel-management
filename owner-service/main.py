from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from models import OwnerCreate, OwnerUpdate, OwnerResponse, OwnerListResponse, GenericResponse
from service import OwnerService

app = FastAPI(title="Owner Management Service", version="1.0.0")
owner_service = OwnerService()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Invalid request data",
            "data": exc.errors()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Unexpected error occurred in Owner Management Service",
            "data": None
        }
    )

@app.get("/", response_model=GenericResponse)
def read_root():
    return {
        "success": True,
        "message": "Owner Management Service is running",
        "data": None 
    }

@app.get("/api/owners", response_model=OwnerListResponse)
def get_all_owners():
    owners = owner_service.get_all()
    return {
        "success": True,
        "message": "Owners fetched successfully",
        "data": owners
    }

@app.get("/api/owners/{owner_id}", response_model=OwnerResponse)
def get_owner(owner_id: str):
    owner = owner_service.get_by_id(owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    return {
        "success": True,
        "message": "Owner fetched successfully",
        "data": owner
    }

@app.post("/api/owners", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
def create_owner(owner: OwnerCreate):
    created_owner = owner_service.create(owner)

    if not created_owner:
        raise HTTPException(status_code=400, detail="Owner with this NIC already exists")
    
    return {
        "success": True,
        "message": "Owner created successfully",
        "data": created_owner
    }

@app.put("/api/owners/{owner_id}", response_model=OwnerResponse)
def update_owner(owner_id: str, owner: OwnerUpdate):
    updated_owner = owner_service.update(owner_id, owner)

    if updated_owner == "NO_FIELDS":
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    if updated_owner == "NIC_EXISTS":
        raise HTTPException(status_code=400, detail="Another owner with this NIC already exists")

    if not updated_owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    return {
        "success": True,
        "message": "Owner updated successfully",
        "data": updated_owner
    }

@app.delete("/api/owners/{owner_id}", response_model=GenericResponse)
def delete_owner(owner_id: str):
    deleted = owner_service.delete(owner_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    return {
        "success": True,
        "message": "Owner deleted successfully",
        "data": None
    }