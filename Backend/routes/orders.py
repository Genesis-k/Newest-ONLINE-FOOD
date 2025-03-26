from fastapi import APIRouter, HTTPException, Depends
from models import Order, OrderItem
from database import orders_collection, db
from bson import ObjectId

router = APIRouter()

# **Place Order**
@router.post("/api/orders")
async def place_order(order: Order):
    order.id = str(ObjectId())
    await orders_collection.insert_one(order.model_dump(by_alias=True))
    return {"message": "Order placed successfully", "order_id": order.id}

# **Get Orders**
@router.get("/api/orders")
async def get_orders():
    orders = await orders_collection.find().to_list(None)
    
    for order in orders:
        order["_id"] = str(order["_id"])

    return orders
# Fetch cart items
@router.get("/api/cart")
async def get_cart():
    cart_items = await db.cart.find().to_list(None)
    for item in cart_items:
        item["_id"] = str(item["_id"])
    return cart_items

# Add item to cart
@router.post("/api/cart")
async def add_to_cart(item: OrderItem):
    new_cart_item = item.model_dump()
    new_cart_item["_id"] = str(ObjectId())  
    await db.cart.insert_one(new_cart_item)
    return {"message": "Item added to cart"}

# Remove item from cart
@router.delete("/api/cart/{item_id}")
async def remove_from_cart(item_id: str):
    delete_result = await db.cart.delete_one({"_id": ObjectId(item_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item removed from cart"}

# Checkout: Convert cart to an order
@router.post("/api/cart/checkout")
async def checkout(user_id: str):
    cart_items = await db.cart.find().to_list(None)

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    order = {
        "user_id": user_id,
        "items": cart_items,
        "total_price": total_price,
        "status": "Pending"
    }

    order_result = await db.orders.insert_one(order)
    await db.cart.delete_many({})  # Clear the cart after checkout

    return {"message": "Order placed successfully", "order_id": str(order_result.inserted_id)}
