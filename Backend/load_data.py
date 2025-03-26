import asyncio
from database import db

categories_collection = db["categories"]
foods_collection = db["foods"]

async def load_data():
    categories = [
        {"_id": 1, "name": "Main Dishes", "image": "images/category/main dishes/BBQ chicken.jpg"},
        {"_id": 2, "name": "Breakfast & Brunch", "image": "images/category/breakfast & brunch/omelette.jpg"},
        {"_id": 3, "name": "Appetizers", "image": "images/category/appetizers & starters/chicken nuggets.jpg"},
        {"_id": 4, "name": "Healthy & Vegetarian", "image": "images/category/healthy food/greek salad.jpg"},
        {"_id": 5, "name": "Desserts", "image": "images/category/dessert/chocolate cake.jpg"},
        {"_id": 6, "name": "Beverages", "image": "images/category/beverages/cappuccino.jpg"},
    ]

    foods = [
        {"_id": 1, "name": "Beef Burger", "category": 1, "price": 500, "image": "images/category/main dishes/burger.jpg", "description": "Juicy grilledbeef patty with lettuce, tomato and cheese."},
         {"_id": 2, "name": "Fresh Juice", "category": 6, "price": 350, "image": "images/category/beverages/strawberry smoothie.jpg", "description": "Choice of Strawberry with some milk."},
    ]

    #insert data into MOngoDB
    await categories_collection. delete_many({})
    await categories_collection.insert_many(categories)

    await foods_collection.delete_many({})
    await foods_collection.insert_many(foods)

    print("Data loaded successfully.")

    asyncio.run(load_data())