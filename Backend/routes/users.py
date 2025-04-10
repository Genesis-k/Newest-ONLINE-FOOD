from fastapi import APIRouter, Depends, HTTPException
from models import UserSignup, UserLogin
from database import db
from routes.auth import create_jwt_token, get_password_hash, verify_password
from utils import verify_jwt_token, get_password_hash
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Extract user from JWT token."""
    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Protected user profile route"""
    return {"message": "Welcome!", "user": current_user}

@router.post("/signup")
async def signup(user: UserSignup):
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hash_password = get_password_hash(user.password)
    user_data = user.model_dump()
    user_data["password"] = hash_password
    
    await db["users"].insert_one(user_data)
    return {"message": "User created successfully"}


@router.post("/login")
async def login(user: UserLogin):
    db_user = await db["users"].find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_jwt_token({"email": user.email})
    return {"access_token": token, "token_type": "bearer"}
