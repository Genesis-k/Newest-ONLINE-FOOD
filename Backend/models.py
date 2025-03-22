from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone

class UserModel(BaseModel):
    username: str
    email: str
    password: str

class MenuItemModel(BaseModel):
        name: str
        description: Optional[str]
        price: float
        available: bool

class OrderModel(BaseModel):
    customer_id: str
    items: List [str]
    total_price: float
    status: str #pending, preparing, out_for_delivery, delivered
    created_at: datetime = datetime.now(timezone.utc)

class TokenData(BaseModel):
    username: Optional[str] = None

class UserInDB(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    hashed_password: str