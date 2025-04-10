from fastapi import APIRouter, HTTPException, Depends
from database import db
from schemas import OrderSchema
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
async def place_order(user_id: str):
    """Place an order."""
    try:
        cart_items = await db.cart.find({"user_id": user_id}).to_list(100)
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty.")

        order = {
            "user_id": user_id,
            "items": cart_items,
            "status": "Pending",
            "created_at": datetime.utcnow(),
        }
        result = await db.orders.insert_one(order)
        await db.cart.delete_many({"user_id": user_id})  # Clear the cart after placing the order
        return {"message": "Order placed successfully!", "order_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error placing order: {str(e)}")

@router.get("/")
async def get_orders(user_id: str):
    """Retrieve all orders for a user."""
    try:
        orders = await db.orders.find({"user_id": user_id}).to_list(100)
        for order in orders:
            order["_id"] = str(order["_id"])
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving orders: {str(e)}")

@router.get("/{user_id}")
async def get_orders(user_id: str):
    orders = await db.orders.find({"user_id": user_id}).to_list(100)
    return [{"id": str(order["_id"]), **order} for order in orders]

@router.get("/{order_id}")
async def get_order(order_id: str):
    """Retrieve order details by ID."""
    try:
        order = await db.orders.find_one({"_id": ObjectId(order_id)})
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")
        order["_id"] = str(order["_id"])
        return {"order": order}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving order: {str(e)}")

@router.patch("/{order_id}")
async def update_order_status(order_id: str, status: str):
    """Update the status of an order."""
    try:
        result = await db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": status}})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Order not found.")
        return {"message": "Order status updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating order status: {str(e)}")
