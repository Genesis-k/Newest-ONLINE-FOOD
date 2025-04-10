from fastapi import APIRouter, HTTPException, Depends
from database import db
from typing import List
from schemas import CartItem
from routes.auth import get_current_user  # Corrected the import path for the auth module

router = APIRouter(prefix="/api/cart", tags=["Cart"])

@router.post("/")
async def add_to_cart(cart: CartItem, user_id: str = Depends(get_current_user)):
    """Add an item to the user's cart."""
    try:
        # Check if the item already exists in the user's cart
        existing_item = await db.cart.find_one({"user_id": user_id, "food_id": cart.food_id})
        
        if existing_item:
            # Update quantity if the item already exists in the cart
            await db.cart.update_one(
                {"_id": existing_item["_id"]},
                {"$inc": {"quantity": cart.quantity}}
            )
        else:
            # Insert a new item into the cart
            await db.cart.insert_one({**cart.dict(), "user_id": user_id})
        
        return {"message": "Item added to cart successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding item to cart: {str(e)}")

@router.get("/{user_id}")
async def get_cart(user_id: str) -> List[dict]:
    """Retrieve all items in the user's cart."""
    try:
        cart_items = await db.cart.find({"user_id": user_id}).to_list(100)
        return [{"id": str(item["_id"]), **item} for item in cart_items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving cart: {str(e)}")

@router.delete("/{user_id}")
async def clear_cart(user_id: str):
    """Clear the user's cart."""
    try:
        result = await db.cart.delete_many({"user_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="No items found in the cart to delete.")
        return {"message": "Cart cleared successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cart: {str(e)}")
