from fastapi import APIRouter, HTTPException, Depends
from auth import hash_password, verify_password, create_access_token
from schemas import UserCreate
from crud import create_user, get_user_by_username
from pymongo. database import Database
from database import get_db
from datetime import timedelta

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate, db: Database = Depends(get_db)):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user.password = hash_password(user.password)
    new_user = create_user(db, user)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(email : str, password: str, db: Database = Depends(get_db)):
    user = await get_user_by_username(db, email)

    if not user or not verify_password(password, user["password"]):
      raise HTTPException(status_code=400, detail="Invalid Credentials")  
    
    access_token = create_access_token({"sub": user["email"]}, timedelta(minutes=30))
    return {"access_token": access_token}
