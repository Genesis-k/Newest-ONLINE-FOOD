from fastapi import APIRouter, Depends
from auth import get_current_user
from crud import create_order

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/")
async def list_orders(current_user: dict = Depends(get_current_user)):
    return await create_order(current_user)
