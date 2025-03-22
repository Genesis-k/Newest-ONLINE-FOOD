from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class TokenData(BaseModel):
        username: Optional[str] = None

class OrderCreate(BaseModel):
            items: List[str]