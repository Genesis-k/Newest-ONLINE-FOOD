import os
from dotenv import load_dotenv

from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import auth, users, foods, orders, delivery, cart, contact, category
from database import connect_to_mongo, close_mongo_connection
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# Access API keys and other credentials
MAPS_PLATFORM_API_KEY = os.getenv('MAPS_PLATFORM_API_KEY')
MONGO_URI = os.getenv('MONGO_URI')
SECRET_KEY = os.getenv('SECRET_KEY')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Debugging: Print to verify keys are loaded (remove in production)
print(f"Google Maps API Key: {MAPS_PLATFORM_API_KEY}")
print(f"MongoDB URI: {MONGO_URI}")
print(f"Google Application Credentials: {GOOGLE_APPLICATION_CREDENTIALS}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events"""
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(lifespan=lifespan)

# Enable CORS for frontend access
origins = [
    "http://127.0.0.1:5500",
    "https://vermillion-tiramisu-072c61.netlify.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#  Include Routers here
app.include_router(users.router)
app.include_router(foods.router)  
app.include_router(orders.router)
app.include_router(delivery.router)
app.include_router(auth.router)
app.include_router(cart.router)
app.include_router(contact.router)
app.include_router(category.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Online Food Ordering, Delivery & Tracking System"}
