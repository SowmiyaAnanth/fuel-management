from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import FuelPassCreate, FuelPassUpdate
from service import FuelPassService
from dotenv import load_dotenv
import os


app = FastAPI(title="Fuel Pass Service")
service = FuelPassService()


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    message = str(exc)

    if "already exists" in message:
        return JSONResponse(status_code=409, content={"detail": message})

    return JSONResponse(status_code=400, content={"detail": message})


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError):
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.get("/")
def root():
    return {"message": "Fuel Pass Service running"}


@app.post("/api/fuelpasses", status_code=201)
async def create_fuel_pass(data: FuelPassCreate):
    return await service.create(data)


@app.get("/api/fuelpasses")
async def get_all():
    return await service.get_all()


@app.get("/api/fuelpasses/{pass_id}")
async def get_by_id(pass_id: str):
    fuel_pass = await service.get_by_id(pass_id)
    if not fuel_pass:
        return JSONResponse(status_code=404, content={"detail": "Fuel pass not found"})
    return fuel_pass


@app.put("/api/fuelpasses/{pass_id}")
async def update_fuel_pass(pass_id: str, data: FuelPassUpdate):
    updated = await service.update_fuel_pass(pass_id, data)
    if not updated:
        return JSONResponse(status_code=404, content={"detail": "Fuel pass not found"})
    return updated


@app.delete("/api/fuelpasses/{pass_id}")
async def delete_fuel_pass(pass_id: str):
    deleted = await service.delete_fuel_pass(pass_id)
    if not deleted:
        return JSONResponse(status_code=404, content={"detail": "Fuel pass not found"})
    return {"message": "Fuel pass deleted successfully"}