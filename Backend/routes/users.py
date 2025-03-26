from fastapi import APIRouter, Depends
from database import get_db
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"message": "User authenticated", "token": token}
