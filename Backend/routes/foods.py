from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from models import Food
from database import foods_collection
from google.cloud import storage
import os

router = APIRouter()

# **Google Cloud Storage Configuration**
BUCKET_NAME = "your-google-cloud-bucket-name"
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# **Upload Image to Google Cloud**
async def upload_image_to_gcs(file: UploadFile):
    blob = bucket.blob(f"food_images/{file.filename}")
    blob.upload_from_file(file.file, content_type=file.content_type)
    return blob.public_url

# **Add Food**
@router.post("/api/foods")
async def add_food(name: str, price: float, category: str, description: str, file: UploadFile = File(...)):
    image_url = await upload_image_to_gcs(file)
    food_data = Food(name=name, price=price, category=category, image_url=image_url, description=description)
    await foods_collection.insert_one(food_data.dict(by_alias=True))
    return {"message": "Food item added successfully"}

# **Get Foods**
@router.get("/api/foods")
async def get_foods(category: str = None):
    query = {"category": category} if category else {}
    foods = await foods_collection.find(query).to_list(None)
    
    for food in foods:
        food["_id"] = str(food["_id"])

    return foods
