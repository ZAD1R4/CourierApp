from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, orders, locations
from security.rate_limiter import rate_limit_middleware
from security.jwt_utils import jwt_middleware

app = FastAPI()

# Подключение middleware
app.middleware("http")(jwt_middleware)
app.middleware("http")(rate_limit_middleware)

# Подключение маршрутов
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(locations.router, prefix="/locations", tags=["Locations"])

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Courier Delivery Platform API"}