from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from typing import Any

app = FastAPI(title="Fuel Management API Gateway", version="1.0.0")

#Service URLs
SERVICES = {
    "owner": "http://localhost:8001",
    "vehicle": "http://localhost:8002",
    "fuelpass": "http://localhost:8003",
    "transaction": "http://localhost:8004"
}

async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    """Forward request to the appropriate microservice"""
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
    
    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            
            content = None
            if response.text:
                try:
                    content = response.json()
                except Exception:
                    content = {"detail": response.text}
            
            return JSONResponse(
                content=content,
                status_code=response.status_code
            )
        
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
        

@app.get("/")
def read_root():
    return {
        "message": "Fuel Management API Gateway is running",
        "available_services": list(SERVICES.keys())
    }


# Owner Management Service Routes
@app.get("/gateway/owners")
async def get_all_owners():
    return await forward_request("owner", "/api/owners", "GET")

@app.get("/gateway/owners/{owner_id}")
async def get_owner(owner_id: str):
    return await forward_request("owner", f"/api/owners/{owner_id}", "GET")

@app.post("/gateway/owners")
async def create_owner(request: Request):
    body = await request.json()
    return await forward_request("owner", "/api/owners", "POST", json=body)

@app.put("/gateway/owners/{owner_id}")
async def update_owner(owner_id: str, request: Request):
    body = await request.json()
    return await forward_request("owner", f"/api/owners/{owner_id}", "PUT", json=body)

@app.delete("/gateway/owners/{owner_id}")
async def delete_owner(owner_id: str):
    return await forward_request("owner", f"/api/owners/{owner_id}", "DELETE")


# Vehicle Registration Service
@app.get("/gateway/vehicles")
async def get_all_vehicles():
    return await forward_request("vehicle", "/api/vehicles", "GET")

@app.get("/gateway/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: str):
    return await forward_request("vehicle", f"/api/vehicles/{vehicle_id}", "GET")

@app.get("/gateway/vehicles/owner/{owner_id}")
async def get_vehicles_by_owner(owner_id: str):
    return await forward_request("vehicle", f"/api/vehicles/owner/{owner_id}", "GET")

@app.post("/gateway/vehicles")
async def create_vehicle(request: Request):
    body = await request.json()
    return await forward_request("vehicle", "/api/vehicles", "POST", json=body)

@app.put("/gateway/vehicles/{vehicle_id}")
async def update_vehicle(vehicle_id: str, request: Request):
    body = await request.json()
    return await forward_request("vehicle", f"/api/vehicles/{vehicle_id}", "PUT", json=body)

@app.delete("/gateway/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: str):
    return await forward_request("vehicle", f"/api/vehicles/{vehicle_id}", "DELETE")


# Fuel Pass Service Routes
@app.get("/gateway/fuelpasses")
async def get_all_fuelpasses():
    return await forward_request("fuelpass", "/api/fuelpasses", "GET")

@app.get("/gateway/fuelpasses/{pass_id}")
async def get_fuelpass(pass_id: str):
    return await forward_request("fuelpass", f"/api/fuelpasses/{pass_id}", "GET")

@app.post("/gateway/fuelpasses")
async def create_fuelpass(request: Request):
    body = await request.json()
    return await forward_request("fuelpass", "/api/fuelpasses", "POST", json=body)

@app.put("/gateway/fuelpasses/{pass_id}")
async def update_fuelpass(pass_id: str, request: Request):
    body = await request.json()
    return await forward_request("fuelpass", f"/api/fuelpasses/{pass_id}", "PUT", json=body)

@app.delete("/gateway/fuelpasses/{pass_id}")
async def delete_fuelpass(pass_id: str):
    return await forward_request("fuelpass", f"/api/fuelpasses/{pass_id}", "DELETE")


# Transaction Service Routes
@app.get("/gateway/transactions")
async def get_all_transactions():
    return await forward_request("transaction", "/api/transactions", "GET")

@app.get("/gateway/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    return await forward_request("transaction", f"/api/transactions/{transaction_id}", "GET")

@app.post("/gateway/transactions")
async def create_transaction(request: Request):
    body = await request.json()
    return await forward_request("transaction", "/api/transactions", "POST", json=body)

@app.put("/gateway/transactions/{transaction_id}")
async def update_transaction(transaction_id: str, request: Request):
    body = await request.json()
    return await forward_request("transaction", f"/api/transactions/{transaction_id}", "PUT", json=body)

@app.delete("/gateway/transactions/{transaction_id}")
async def delete_transaction(transaction_id: str):
    return await forward_request("transaction", f"/api/transactions/{transaction_id}", "DELETE")

