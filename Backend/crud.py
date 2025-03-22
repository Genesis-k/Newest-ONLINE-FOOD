from schemas import UserCreate
from models import UserModel, MenuItemModel, OrderModel
from database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

async def create_user(db: AsyncIOMotorDatabase, user: UserCreate):
    user_data = user.model_dump()
    result = await db.users.insert_one(user_data)  
    return result.inserted_id  

async def get_user_by_username(db: AsyncIOMotorDatabase, username: str):
    return await db.users.find_one({"username": username})  

async def create_menu_item(db: AsyncIOMotorDatabase, item_data: dict):
    item = await db.menu.insert_one(item_data) 
    return item.inserted_id

async def create_order(db: AsyncIOMotorDatabase, order_data: dict):
    order = await db.orders.insert_one(order_data)
    return order.inserted_id

