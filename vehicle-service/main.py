from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from models import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
    VehicleListResponse,
    GenericResponse
)
from service import VehicleService

app = FastAPI(title="Vehicle Registration Service", version="1.0.0")
vehicle_service = VehicleService()


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
            "message": "Unexpected error occurred in Vehicle Registration Service",
            "data": None
        }
    )    


@app.get("/", response_model=GenericResponse)
def read_root():
    return {
        "success": True,
        "message": "Vehicle Registration Service is running",
        "data": None
    }


@app.get("/api/vehicles", response_model=VehicleListResponse)
def get_all_vehicles():
    vehicles = vehicle_service.get_all()
    return {
        "success": True,
        "message": "Vehicles fetched successfully",
        "data": vehicles
    }


@app.get("/api/vehicles/owner/{owner_id}", response_model=VehicleListResponse)
def get_vehicles_by_owner(owner_id: str):
    vehicles = vehicle_service.get_by_owner(owner_id)
    return {
        "success": True,
        "message": "Vehicles fetched successfully for owner",
        "data": vehicles
    }  


@app.get("/api/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: str):
    vehicle = vehicle_service.get_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return {
        "success": True,
        "message": "Vehicle fetched successfully",
        "data": vehicle
    }  


@app.post("/api/vehicles", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle: VehicleCreate):
    result, error = vehicle_service.create(vehicle)

    if error == "Owner not found":
        raise HTTPException(status_code=400, detail="Owner not found")

    if error:
        raise HTTPException(status_code=400, detail=error)

    return {
        "success": True,
        "message": "Vehicle created successfully",
        "data": result
    }  


@app.put("/api/vehicles/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: str, vehicle: VehicleUpdate):
    updated = vehicle_service.update(vehicle_id, vehicle)

    if updated == "NO_FIELDS":
        raise HTTPException(status_code=400, detail="No fields provided for update")

    if updated == "OWNER_NOT_FOUND":
        raise HTTPException(status_code=400, detail="Owner not found")

    if updated == "VEHICLE_NUMBER_EXISTS":
        raise HTTPException(status_code=400, detail="Vehicle number already registered")

    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return {
        "success": True,
        "message": "Vehicle updated successfully",
        "data": updated
    }  


@app.delete("/api/vehicles/{vehicle_id}", response_model=GenericResponse)
def delete_vehicle(vehicle_id: str):
    success = vehicle_service.delete(vehicle_id)

    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found or invalid vehicle ID")

    return {
        "success": True,
        "message": "Vehicle deleted successfully",
        "data": None
    } 