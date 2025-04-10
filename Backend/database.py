from motor.motor_asyncio import AsyncIOMotorClient
import certifi
import os
from dotenv import load_dotenv
from google.cloud import storage

# Load environment variables from .env
load_dotenv()

# Get the credentials path for Google Cloud Storage from .env
gcs_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if gcs_credentials_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcs_credentials_path

# Initialize Google Cloud Storage Client
try:
    storage_client = storage.Client()
    bucket_name = os.getenv("GCS_BUCKET_NAME", "online_food")  # Default bucket name
    bucket = storage_client.bucket(bucket_name)
    print(f"Connected to GCS bucket: {bucket_name}")
except Exception as e:
    print(f"Error initializing Google Cloud Storage: {e}")
    bucket = None

# Fetch MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the environment variables.")

# Initialize MongoDB Client
try:
    client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client["food_delivery"]

    # Define collections
    foods_collection = db["foods"]
    orders_collection = db["orders"]
    users_collection = db["users"]
    deliveries_collection = db["deliveries"]

    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None

# Utility function to get the database instance
async def get_db():
    """Returns the database instance."""
    if not db:
        raise Exception("Database connection is not initialized.")
    return db

# Utility function to connect to MongoDB
async def connect_to_mongo():
    """Establish connection to MongoDB."""
    try:
        # Ensure the connection is established
        await client.admin.command("ping")
        print("Connected to MongoDB successfully.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

# Utility function to close MongoDB connection
async def close_mongo_connection():
    """Close MongoDB connection on shutdown."""
    try:
        await client.close()
        print("MongoDB connection closed.")
    except Exception as e:
        print(f"Error closing MongoDB connection: {e}")

# Utility function to upload an image to Google Cloud Storage
async def upload_image_to_gcs(file, file_name, content_type):
    """Asynchronously uploads an image to Google Cloud Storage and returns the public URL."""
    if not bucket:
        raise Exception("GCS bucket is not initialized.")
    try:
        blob = bucket.blob(file_name)

        # Read file asynchronously
        file_data = await file.read()

        # Upload file to GCS
        blob.upload_from_string(file_data, content_type=content_type)

        # Make file public
        blob.make_public()

        # Return public URL
        return blob.public_url
    except Exception as e:
        print(f"Error uploading image to GCS: {e}")
        return None
