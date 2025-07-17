import jwt
from functools import wraps
from fastapi import Request, HTTPException
from datetime import datetime, timedelta

# Настройки
SECRET_KEY = "a1b2c3d4e5f678901234567890abcdef1234567890abcdef1234567890abcdef"
ALGORITHM = "HS256"

# --- Функции для работы с токенами ---

def create_access_token( dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

# --- JWT Middleware ---

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
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)

    return middleware
