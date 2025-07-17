from fastapi import Request, HTTPException
from collections import defaultdict
from datetime import datetime, timedelta

# Простой рейт-лимитер
class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    def is_allowed(self, identifier: str) -> bool:
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=1)
        self.requests[identifier] = [t for t in self.requests[identifier] if t > window_start]
        if len(self.requests[identifier]) >= self.requests_per_minute:
            return False
        self.requests[identifier].append(now)
        return True

rate_limiter = RateLimiter(requests_per_minute=100)

def rate_limit_middleware(app):
    @app.middleware("http")
    async def middleware(request: Request, call_next):
        client_ip = request.client.host
        if not rate_limiter.is_allowed(client_ip):
            raise HTTPException(status_code=429, detail="Too Many Requests")
        return await call_next(request)