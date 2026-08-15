from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

class HealthSyncItem(BaseModel):
    activity_type: int
    activity_date: date
    calories_burnt: int
    activity_name: Optional[str] = None
    activity_time: Optional[time] = None
    activity_duration: Optional[time] = None

class HealthSyncRequest(BaseModel):
    user_id: int
    data: List[HealthSyncItem]
