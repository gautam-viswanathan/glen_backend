import datetime
from typing import Optional

from db.base import Base
from sqlalchemy import (BIGINT, Date, ForeignKeyConstraint, Index, Integer,
                        String, Time, text)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ActivityTracker(Base):
    __tablename__ = 'activity_tracker'
    __table_args__ = (
        ForeignKeyConstraint(['activity_type'], ['activity_types.id'], name='activity_tracker_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_activity_user'),
        Index('activity_type', 'activity_type'),
        Index('fk_activity_user', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    activity_type: Mapped[int] = mapped_column(Integer, nullable=False)
    activity_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    calories_burnt: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False, server_default=text("'1'"))
    activity_name: Mapped[Optional[str]] = mapped_column(String(255))
    activity_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    activity_duration: Mapped[Optional[datetime.time]] = mapped_column(Time)

    # activity_types: Mapped['ActivityTypes'] = relationship('ActivityTypes', back_populates='activity_tracker')
    # user: Mapped['Users'] = relationship('Users', back_populates='activity_tracker')

    activity_types = relationship('ActivityTypes', back_populates='activity_tracker')
    user = relationship('Users', back_populates='activity_tracker')
