from fastapi import APIRouter
 
router = APIRouter()

@router.get("/delivery")
async def delivery():
    return {"message": "Delivery API is working"}