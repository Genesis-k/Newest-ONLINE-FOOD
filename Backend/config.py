import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

SECRET_KEY = os.getenv("JWT_SECRET", "4cc57978155b0e006c5ecdcc08e83c9a20cfa426019a4c46772c0c633a465a8")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
