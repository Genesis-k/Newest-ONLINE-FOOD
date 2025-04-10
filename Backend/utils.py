from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from google.cloud import storage
import os

# SECRET_KEY: Use a strong, random key
SECRET_KEY = "4cc57978155b0e006c5ecdcc08e83c9a20cfa426019a4c46772c0c633a465a8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expires in 30 minutes

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def  get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, expires_delta: timedelta = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str):
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# Initialize the GCS client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
storage_client = storage.Client()

def upload_image_to_gcs(file, filename, content_type):
    """Uploads an image to Google Cloud Storage and returns the public URL."""
    try:
        bucket_name = os.getenv("GOOGLE_CLOUD_BUCKET")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)

        # Upload the file to GCS
        blob.upload_from_file(file.file, content_type=content_type)

        # Make the file publicly accessible
        blob.make_public()

        # Return the public URL
        return blob.public_url
    except Exception as e:
        raise Exception(f"Failed to upload image to GCS: {str(e)}")
