from typing import Optional

from db.base import Base
from models.activity_tracker import ActivityTracker
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ActivityTypes(Base):
    __tablename__ = 'activity_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))

    activity_tracker: Mapped[list['ActivityTracker']] = relationship('ActivityTracker', back_populates='activity_types')

