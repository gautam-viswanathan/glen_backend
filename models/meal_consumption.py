import datetime
import decimal
from typing import Optional

from db.base import Base
from sqlalchemy import (BIGINT, DECIMAL, Date, ForeignKeyConstraint, Index,
                        Integer, String, Time)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MealConsumption(Base):
    __tablename__ = 'meal_consumption'
    __table_args__ = (
        ForeignKeyConstraint(['meal_id'], ['food_timings.id'], name='meal_consumption_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_meal_entries_user'),
        Index('fk_user_meal_entries_user', 'user_id'),
        Index('meal_id', 'meal_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meal_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    meal_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    meal_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(6, 2))
    calories_per_item: Mapped[Optional[int]] = mapped_column(Integer)
    quantity_count: Mapped[Optional[int]] = mapped_column(Integer)

    meal = relationship('FoodTimings', back_populates='meal_consumption')
    user = relationship('Users', back_populates='meal_consumption')

