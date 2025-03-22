from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["food_delivery"]

async def get_db():
    return db

async def connect_to_mongo():
    print("Connected to MongoDB")
 
async def close_mongo_connection():
    client.close()
    print("MongoDB connection closed")