from fastapi import APIRouter
from crud import create_menu_item
from models import MenuItemModel

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.post("/add")
async def add_item(item: MenuItemModel):
    return await create_menu_item(item_data=item.model_dump())
