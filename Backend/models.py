from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, timezone
from bson import ObjectId

# Helper function to convert ObjectId into a string
def object_id_str(obj_id: ObjectId) -> str:
    return str(obj_id)

# User model
class User(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: object_id_str(ObjectId()), alias="_id")
    email: EmailStr
    password: str

# Food model
class Food(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: object_id_str(ObjectId()), alias="_id")
    name: str
    price: float
    image_url: str
    category: str
    description: Optional[str] = None

# Order Item model (for items inside an order)
class OrderItem(BaseModel):
    food_id: str
    quantity: int

# Order model
class Order(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: object_id_str(ObjectId()), alias="_id")
    user_id: str
    items: List[OrderItem]
    total_price: float
    status: str = "Pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Delivery model
class Delivery(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: object_id_str(ObjectId()), alias="_id")
    order_id: str
    driver_name: str
    status: str = "In Progress"
    estimated_time: Optional[str] = None

# Token Data model for authentication
class TokenData(BaseModel):
    username: Optional[str] = None

# User model for database storage (with hashed password)
class UserInDB(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    hashed_password: str

# Contact Form model
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: str
    subject: str
    message: str

class CartItem(BaseModel):
    food_id: str
    name: str
    price: float
    quantity: int
    image: str
