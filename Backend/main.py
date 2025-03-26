from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import users, foods, orders, delivery
from database import connect_to_mongo, close_mongo_connection
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return {"message": "Welcome to the Online Food Ordering, Delivery & Tracking System"}
