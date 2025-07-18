import pytest
import jwt
from fastapi import FastAPI, Request, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.auth import (
    JWT_SECRET,
    JWT_ALGORITHM,
    create_access_token,
    authenticate_user,
    pwd_context
)

# Мокаем зависимости
@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('backend.database.db'), \
         patch('backend.auth.db'):
        yield

app = FastAPI()
client = TestClient(app)

# 1. Тест успешной аутентификации
def test_authenticate_user_success():
    mock_user = {
        "email": "test@example.com",
        "password": pwd_context.hash("password123")
    }
    
    with patch('backend.auth.db.users.find_one', return_value=mock_user):
        user = authenticate_user("test@example.com", "password123")
        assert user == mock_user

# 2. Тест неудачной аутентификации
def test_authenticate_user_failure():    
    with patch('backend.auth.db.users.find_one', return_value=None):
        user = authenticate_user("wrong@example.com", "password123")
        assert user is False

# 3. Тест создания токена
def test_create_access_token():
    token = create_access_token({"sub": "test@example.com"})
    decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    assert decoded["sub"] == "test@example.com"

# 4. Тест middleware с валидным токеном
def test_jwt_middleware_valid_token():
    app = FastAPI()
    
    @app.middleware("http")
    async def test_middleware(request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401)
        token = auth_header.split(" ")[1]
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.PyJWTError:
            raise HTTPException(status_code=401)
        return await call_next(request)
    
    @app.get("/protected")
    async def protected():
        return {"status": "ok"}
    
    client = TestClient(app)
    token = create_access_token({"sub": "test@example.com"})
    
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

# 5. Тест middleware без токена
def test_jwt_middleware_missing_token():
    app = FastAPI()

    @app.middleware("http")
    async def test_middleware(request: Request, call_next):
        if request.url.path == "/protected":
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                from fastapi.responses import JSONResponse
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Missing token"},
                )
        return await call_next(request)

    @app.get("/protected")
    async def protected():
        return {"status": "ok"}

    client = TestClient(app)
    response = client.get("/protected")
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Missing token"