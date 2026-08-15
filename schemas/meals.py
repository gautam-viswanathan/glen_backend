from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time

class MealConsumptionResponse(BaseModel):
    id: int
    meal_id: int
    item_name: str
    meal_date: date
    meal_time: time
    user_id: int
    quantity: Optional[float] = None
    calories_per_item: Optional[int] = None
    quantity_count: Optional[int] = None
    
    class Config:
        from_attributes = True
