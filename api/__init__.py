from api.v1 import users, health, meals
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(meals.router, prefix="/meals", tags=["Meals"])