from fastapi import APIRouter, Depends, HTTPException
from models import UserCreate, UserOut
from database import db
from passlib.context import CryptContext
from auth import create_access_token, get_current_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_pw
    result = db.users.insert_one(user_data)
    return {**user.dict(), "id": str(result.inserted_id)}

@router.post("/login")
async def login(email: str, password: str):
    user = db.users.find_one({"email": email})
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"email": user["email"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}