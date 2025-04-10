from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from utils import upload_image_to_gcs
from database import foods_collection
from bson import ObjectId

router = APIRouter()

@router.post("/foods", status_code=201)
async def add_food(
    name: str, description: str, price: float, file: UploadFile = File(...)
):
    """Uploads an image to GCS and adds a new food item to MongoDB."""
    try:
        # Upload image to GCS and get the public URL
        image_url = upload_image_to_gcs(file, file.filename, file.content_type)
        if not image_url:
            raise HTTPException(status_code=500, detail="Image upload failed.")

        # Create food item document
        food_item = {
            "name": name,
            "description": description,
            "price": price,
            "image_url": image_url,
        }

        # Insert into MongoDB
        result = await foods_collection.insert_one(food_item)
        food_item["_id"] = str(result.inserted_id)

        return {"message": "Food item added successfully!", "food": food_item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding food: {str(e)}")

@router.get("/foods")
async def get_foods():
    """Fetches all food items from MongoDB."""
    foods = await foods_collection.find().to_list(length=100)
    
    # Convert MongoDB ObjectId to string
    for food in foods:
        food["_id"] = str(food["_id"])

    return {"foods": foods}

@router.get("/foods/{food_id}")
async def get_food(food_id: str):
    """Fetches a single food item by ID."""
    food = await foods_collection.find_one({"_id": ObjectId(food_id)})
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found.")
    
    food["_id"] = str(food["_id"])
    return {"food": food}

@router.put("/foods/{food_id}")
async def update_food(food_id: str, name: str = None, description: str = None, price: float = None):
    """Updates a food item by ID."""
    update_data = {}
    if name:
        update_data["name"] = name
    if description:
        update_data["description"] = description
    if price:
        update_data["price"] = price

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")

    result = await foods_collection.update_one({"_id": ObjectId(food_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Food item not found.")

    return {"message": "Food item updated successfully!"}

@router.delete("/foods/{food_id}")
async def delete_food(food_id: str):
    """Deletes a food item by ID."""
    result = await foods_collection.delete_one({"_id": ObjectId(food_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Food item not found.")

    return {"message": "Food item deleted successfully!"}

@router.get("/search")
async def search_foods(query: str):
    """Search for foods by name or description."""
    try:
        foods = await foods_collection.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        }).to_list(100)

        if not foods:
            return {"message": "No matching foods found.", "foods": []}

        for food in foods:
            food["_id"] = str(food["_id"])
        return {"foods": foods}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching foods: {str(e)}")

@router.get("/foods/paginate")
async def paginate_foods(skip: int = 0, limit: int = 10):
    """Fetches food items with pagination."""
    foods = await foods_collection.find().skip(skip).limit(limit).to_list(length=limit)

    # Convert MongoDB ObjectId to string
    for food in foods:
        food["_id"] = str(food["_id"])

    return {"foods": foods, "skip": skip, "limit": limit}


