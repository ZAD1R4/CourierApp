from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from models import LocationUpdate
from database import db 
from auth import get_current_user
from datetime import datetime, timezone
import logging

router = APIRouter()

@router.post("/update")
async def update_location(location: LocationUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "courier":
        raise HTTPException(status_code=403, detail="Only couriers can update location")
    try:
        db.locations.update_one(
            {"courier_id": location.courier_id},
            {"$set": {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "timestamp": datetime.now(timezone.utc)
            }},
            upsert=True
        )
    except Exception as e:
        logging.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return {"status": "Location updated"}