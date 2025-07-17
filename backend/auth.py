from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from database import db
from security.jwt_utils import create_access_token, verify_token

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
    return jwt.encode(data, "your-secret-key", algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload