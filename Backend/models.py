from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from bson import ObjectId

# Helper function for MongoDB ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        schema.update(type="string")
        return schema

# Base model with ObjectId support
class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        from_attributes = True

# User model
class User(MongoBaseModel):
    username: str
    email: EmailStr  # Use EmailStr for email validation
    password: str
    role: str = "customer"  # Default role: customer

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Food Item model
class Food(MongoBaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category: str

# Order Item model
class OrderItem(BaseModel):
    food_id: PyObjectId
    name: str
    price: float
    quantity: int
    image_url: Optional[str] = None

# Order model
class Order(MongoBaseModel):
    user_id: PyObjectId
    items: List[OrderItem]  # List of items in the order
    total_price: float
    status: str = "Pending"  # Default status: Pending

# Delivery model
class Delivery(MongoBaseModel):
    order_id: PyObjectId
    status: str = "Preparing"  # Default status: Preparing
    estimated_time: Optional[int] = None  # Estimated time in minutes
    delivery_person: Optional[str] = None
    contact_number: Optional[str] = None
