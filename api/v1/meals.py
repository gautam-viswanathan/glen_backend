import random
from datetime import date, datetime
from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from db.session import get_db
from models.meal_consumption import MealConsumption
from schemas.meals import MealConsumptionResponse

router = APIRouter()

@router.post("/upload", response_model=MealConsumptionResponse)
def upload_meal_image(
    user_id: int = Form(...),
    meal_id: int = Form(1),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # TODO: In a real implementation, send the image (file.file.read()) to an ML platform 
    # like OpenAI Vision API or a locally hosted CoreML model on the backend.
    
    # Mocking ML Response for nutritional info based on the image upload
    mock_detected_item = random.choice(["Chicken Salad", "Avocado Toast", "Protein Shake"])
    mock_calories = random.randint(250, 700)
    
    now = datetime.now()
    
    meal_record = MealConsumption(
        user_id=user_id,
        meal_id=meal_id,
        item_name=mock_detected_item,
        meal_date=now.date(),
        meal_time=now.time(),
        quantity=1.0,
        calories_per_item=mock_calories,
        quantity_count=1
    )
    
    db.add(meal_record)
    db.commit()
    db.refresh(meal_record)
    
    return meal_record
