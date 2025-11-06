from pydantic import BaseModel


class UserCreate(BaseModel):
    role_id: int
    email: str
    password: str
    date_of_birth: str  # ISO format date string
    username: str
    first_name: str
    last_name: str
    phone_number: str

class generateOtp(BaseModel):
    email: str
    otp:str

    class Config:
        from_attributes  = True

class UserUpdate(BaseModel):
    id: int

    class Config:
        from_attributes  = True