from fastapi import APIRouter, HTTPException, Depends
from database import db

router = APIRouter()

@router.post("/api/users/register")
async def register_user(user: dict):
    existing_user = await db.users.find_one({"email": user["email"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = await db.users.insert_one(user)
    return {"message": "User registered successfully", "user_id": str(new_user.inserted_id)}

@router.get("/api/users")
async def get_users():
    users = await db.users.find({}, {"_id": 1, "name": 1, "email": 1}).to_list(None)

    for user in users:
        user["_id"] = str(user["_id"])

    return users
