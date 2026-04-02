from fastapi import FastAPI, HTTPException, status
from models import TransactionCreate, TransactionUpdate
from service import TransactionService

app = FastAPI(title="Refueling Transaction Service", version="1.0.0")

#Initialize service
transaction_service = TransactionService()

@app.get("/")
def read_root():
    return {
        "success": True,
        "message": "Refueling Transaction Service is running"
    }


# GET ALL
@app.get("/api/transactions")
async def get_all_transactions():
    data = await transaction_service.get_all()
    return {
        "success": True,
        "message": "Transactions retrieved successfully",
        "data": data
    }

# GET BY ID
@app.get("/api/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    transaction = await transaction_service.get_by_id(transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {
        "success": True,
        "message": "Transaction retrieved successfully",
        "data": transaction
    }

# CREATE Transaction
@app.post("/api/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction: TransactionCreate):
    created = await transaction_service.create(transaction)

    if not created:
        raise HTTPException(status_code=400, detail="Transaction ID already exists")
    
    if isinstance(created, dict) and "error" in created:
        raise HTTPException(status_code=400, detail=created["error"])
    
    return {
        "success": True,
        "message": "Transaction created successfully",
        "data": created
    }


# UPDATE
@app.put("/api/transactions/{transaction_id}")
async def update_transaction(transaction_id: str, transaction: TransactionUpdate):
    updated = await transaction_service.update(transaction_id, transaction)

    if not updated:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if isinstance(updated, dict) and "error" in updated:
        raise HTTPException(status_code=400, detail=updated["error"])

    return {
        "success": True,
        "message": "Transaction updated successfully",
        "data": updated
    }


# DELETE
@app.delete("/api/transactions/{transaction_id}")
async def delete_transaction(transaction_id: str):
    success = await transaction_service.delete(transaction_id)

    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return {
        "success": True,
        "message": "Transaction deleted successfully"
    }
    