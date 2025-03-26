from fastapi import APIRouter, HTTPException, Depends
from database import db

router = APIRouter()

@router.post("/api/orders")
async def create_order(order: dict):
    new_order = await db.orders.insert_one(order)
    return {"message": "Order placed successfully", "order_id": str(new_order.inserted_id)}

@router.get("/api/orders")
async def get_orders():
    orders = await db.orders.find({}, {"_id": 1, "items": 1, "total": 1, "status": 1}).to_list(None)
    
    for order in orders:
        order["_id"] = str(order["_id"])

    return orders
