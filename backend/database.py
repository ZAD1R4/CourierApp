from pymongo import MongoClient
import redis.asyncio as redis
from datetime import datetime

# MongoDB
MONGO_URI = "mongodb://mongo:27017"
client = MongoClient(MONGO_URI)
db = client["courier_db"]

# Redis
REDIS_URI = "redis://redis:6379"
redis_client = redis.Redis.from_url(REDIS_URI)