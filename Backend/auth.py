from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from models import TokenData, UserInDB
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from crud import get_user_by_username


#Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#Oauth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#function to verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#function to access tokens
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    #function to verify access tokens
def verify_token(token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError:
        raise credentials_exception

#dependency to get user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    user = await get_user_by_username(token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not Found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserInDB(**user)