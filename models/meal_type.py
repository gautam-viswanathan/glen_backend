# import datetime
from typing import Optional

from db.base import Base
from models.meal_consumption import MealConsumption
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class FoodTimings(Base):
    __tablename__ = 'food_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    meal_consumption: Mapped[list['MealConsumption']] = relationship('MealConsumption', back_populates='meal')
