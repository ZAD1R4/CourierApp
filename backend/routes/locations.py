from fastapi import APIRouter, Depends, HTTPException
from models import LocationUpdate
from database import db
from auth import get_current_user

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.post("/update")
async def update_location(location: LocationUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "courier":
        raise HTTPException(status_code=403, detail="Only couriers can update location")
    db.locations.update_one(
        {"courier_id": location.courier_id},
        {"$set": {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timestamp": datetime.utcnow()
        }},
        upsert=True
    )
    return {"status": "Location updated"}