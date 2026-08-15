from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.activity_tracker import ActivityTracker
from schemas.health import HealthSyncRequest

router = APIRouter()

@router.post("/sync")
def sync_health_data(payload: HealthSyncRequest, db: Session = Depends(get_db)):
    for item in payload.data:
        record = ActivityTracker(
            user_id=payload.user_id,
            activity_type=item.activity_type,
            activity_date=item.activity_date,
            calories_burnt=item.calories_burnt,
            activity_name=item.activity_name,
            activity_time=item.activity_time,
            activity_duration=item.activity_duration
        )
        db.add(record)
    db.commit()
    return {"status": "success", "synced_records": len(payload.data)}
