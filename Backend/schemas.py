from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User Schema
class UserSchema(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    password: str
    role: str = "customer"  # Default role

    class Config:
        from_attributes = True  # Replaces 'orm_mode'
        populate_by_name = True  # Replaces 'allow_population_by_field_name'

# Food Schema
class FoodSchema(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str]
    price: float
    image_url: Optional[str]
    category: str

# Order Schema
class OrderSchema(BaseModel):
    id: Optional[str] = None
    user_id: str
    items: List[dict]  # Each item contains food_id, quantity, name, price, image
    total_price: float
    status: str = "Pending"

# Delivery Schema
class DeliverySchema(BaseModel):
    order_id: str
    status: str
    estimated_delivery_time: Optional[datetime] = None
    delivery_person: Optional[str] = None
    contact_number: Optional[str] = None

    class Config:
        from_attributes = True  # Replaces 'orm_mode'
        populate_by_name = True  # Replaces 'allow_population_by_field_name'

# Cart Schema
class CartItem(BaseModel):
    user_id: str
    food_id: str
    name: str  # Name of the food item
    price: float  # Price of the food item
    image: Optional[str]  # Image URL of the food item
    quantity: int  # Quantity of the food item

# Contact Schema
class ContactForm(BaseModel):
    name: str
    email: str
    message: str