from fastapi import HTTPException, Request
from functools import wraps
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import timedelta
import jwt
from passlib.context import CryptContext

from backend.database import db

JWT_SECRET = "a1b2c3d4e5f678901234567890abcdef1234567890abcdef1234567890abcdef"
JWT_ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_user(email: str):
    user = db.users.find_one({"email": email})
    return user

def authenticate_user(email: str, password: str):
    user = db.users.find_one({"email": email})
    if not user or not pwd_context.verify(password, user["password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    return jwt.encode(data, "a1b2c3d4e5f678901234567890abcdef1234567890abcdef1234567890abcdef", algorithm="HS256")

def get_current_user(request: Request):
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return request.state.user

def jwt_middleware(app):
    @wraps(app)
    async def middleware(request: Request, call_next):
        excluded_routes = ["/users/login", "/users/register"]
        if request.url.path in excluded_routes:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing token")

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.state.user = payload
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)
    return middleware
