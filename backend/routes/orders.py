from fastapi import APIRouter, Depends, HTTPException
from models import OrderCreate
from database import db
from auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/create")
async def create_order(order: OrderCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "client"]:
        raise HTTPException(status_code=403, detail="Access denied")
    order_data = order.dict()
    order_data["created_at"] = datetime.utcnow()
    order_data["status"] = "pending"
    result = db.orders.insert_one(order_data)
    return {"id": str(result.inserted_id), **order_data}

@router.get("/{order_id}")
async def get_order(order_id: str, current_user: dict = Depends(get_current_user)):
    order = db.orders.find_one({"id": order_id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user["role"] == "courier" and order.get("courier_id") != current_user.get("id"):
        raise HTTPException(status_code=403, detail="Access denied")
    return order