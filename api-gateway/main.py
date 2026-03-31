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
    "transaction": "http://localhost:8004",
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
                raise HTTPException(status_code=404, detail="Method not allowed")
            
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
        "available_services": list(SERVICES.key())
    }


