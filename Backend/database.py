import os
from motor.motor_asyncio import AsyncIOMotorClient


# Fetch MongoDB URI from Railway environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Initialize MongoDB Client
client = AsyncIOMotorClient(MONGO_URI)
db = client["food_delivery"]

foods_collection = db["foods"]
orders_collection = db["orders"]
users_collection = db["users"]
deliveries_collection = db["deliveries"]


async def get_db():
    """Returns the database instance."""
    return db

async def connect_to_mongo():
    """Establish connection to MongoDB."""
    try:
        # Ensure the connection is established
        await client.admin.command("ping")
        print("Connected to MongoDB successfully.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

async def close_mongo_connection():
    """Close MongoDB connection on shutdown."""
    client.close()
    print(" MongoDB connection closed.")
