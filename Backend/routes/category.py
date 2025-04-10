from fastapi import APIRouter, HTTPException
from database import db
from pydantic import BaseModel

router = APIRouter(prefix="/api/category", tags=["Category"])

class Category(BaseModel):
    name: str

@router.get("/")
async def get_categories():
    """Retrieve a list of all unique food categories."""
    try:
        categories = await db.foods.distinct("category")
        return {"message": "Categories retrieved successfully.", "categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")

@router.post("/")
async def add_category(category: Category):
    """Add a new category."""
    try:
        # Check if the category already exists
        existing_category = await db.foods.find_one({"category": category.name})
        if existing_category:
            raise HTTPException(status_code=400, detail="Category already exists.")

        # Insert the new category
        await db.foods.insert_one({"category": category.name})
        return {"message": "Category added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding category: {str(e)}")

@router.delete("/{category_name}")
async def delete_category(category_name: str):
    """Delete a category."""
    try:
        # Delete the category
        result = await db.foods.delete_many({"category": category_name})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Category not found.")
        return {"message": "Category deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting category: {str(e)}")