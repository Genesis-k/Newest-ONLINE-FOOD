from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from database import db, foods_collection
from utils import upload_image_to_gcs

router = APIRouter(prefix="/api/foods", tags=["foods"])

# Get all foods or filter by category
@router.get("/")
async def get_foods(category: int = Query(None)):
    query = {"category": category} if category else {}
    foods = await foods_collection.find(query, {"_id": 1, "name": 1, "price": 1, "image": 1, "description": 1}).to_list(None)

    # Convert ObjectId to string
    for food in foods:
        food["_id"] = str(food["_id"])

    return foods

# Search foods by name
@router.get("/search")
async def search_foods(query: str = Query(...)):
    regex_query = {"name": {"$regex": query, "$options": "i"}}
    foods = await foods_collection.find(regex_query, {"_id": 1, "name": 1, "price": 1, "image": 1, "description": 1}).to_list(None)

    # Convert ObjectId to string
    for food in foods:
        food["_id"] = str(food["_id"])

    return foods

# Add a new food item
@router.post("/")
async def add_food (name: str, price: float, category: str, description: str, image: UploadFile = File(...)):
    """Uploads food item with image to GCS and saves it in MongoDB."""
    try:
        image_url = upload_image_to_gcs(image.file, f"foods/image.filename")
        
        food_data = {
            "name": name,
            "price": price,
            "category": category,
            "description": description,
            "image": image_url
        }
        result = await db.foods.insert_one(food_data)

        return {"message": "Food item added", "id": str(result.inserted_id), "image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
