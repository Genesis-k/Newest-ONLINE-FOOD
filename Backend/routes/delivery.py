from fastapi import APIRouter, HTTPException, Depends
from database import db

router = APIRouter()

@router.get("/api/delivery/{order_id}")
async def get_delivery_status(order_id: str):
    order = await db.orders.find_one({"_id": order_id}, {"_id": 1, "status": 1})
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"order_id": order_id, "status": order["status"]}
