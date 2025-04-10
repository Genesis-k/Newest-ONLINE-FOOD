from fastapi import APIRouter, HTTPException
from database import db
from schemas import DeliverySchema

router = APIRouter(prefix="/delivery", tags=["Delivery"])

@router.get("/{order_id}", response_model=DeliverySchema)
async def track_delivery(order_id: str):
    """Track the delivery status of an order."""
    try:
        # Find the delivery record by order_id
        delivery = await db.delivery.find_one({"order_id": order_id})
        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")
        
        # Convert MongoDB ObjectId to string and return the delivery details
        delivery["id"] = str(delivery["_id"])
        del delivery["_id"]  # Remove the ObjectId field for compatibility
        return delivery
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking delivery: {str(e)}")

@router.patch("/{order_id}")
async def update_delivery_status(order_id: str, status: str):
    """Update the delivery status of an order."""
    try:
        result = await db.delivery.update_one({"order_id": order_id}, {"$set": {"status": status}})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Delivery not found.")
        return {"message": "Delivery status updated successfully!"}
    except Exception as e:
        raise HTTPException (status_code=500, detail=f"Error updating delivery status: {str(e)}")