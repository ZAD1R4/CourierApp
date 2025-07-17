from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    role: str

class UserOut(BaseModel):
    id: str
    email: str
    role: str

class TokenData(BaseModel):
    email: str
    role: str

class OrderCreate(BaseModel):
    client_id: str
    address: str
    status: str = "pending"  # по умолчанию

class LocationUpdate(BaseModel):
    courier_id: str
    latitude: float
    longitude: float