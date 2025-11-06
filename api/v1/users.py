import random
import uuid

from core.security import get_password_hash
from db.redis_connection import redis_client as r
from db.session import get_db
from fastapi import APIRouter, Depends
from models.users import Users
from schemas.users import UserCreate, UserUpdate, generateOtp
from sqlalchemy.orm import Session

router = APIRouter()

# router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register",response_model=generateOtp)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print("Registering user:", user)
    hashed_pw=get_password_hash(user.password)
    new_user=Users(uuid=str(uuid.uuid4()),
                    email=user.email,
                    password_hash=hashed_pw,
                    date_of_birth=user.date_of_birth,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    role_id=user.role_id,
                    phone_number=user.phone_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("new_user:", new_user)
    otp = str(random.randint(100000, 999999))
    otp_key = f"otp:{user.email}"
    r.setex(otp_key, 300, otp)
    print("Generated OTP:", otp)
    return {"email":new_user.id,"otp":otp}


@router.get("/")
def get_users():
    return [{"id": 1, "name": "Alice"}]