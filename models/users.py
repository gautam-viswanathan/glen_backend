import datetime
from typing import Optional

from db.base import Base
from sqlalchemy import (CHAR, Date, DateTime, Enum, ForeignKey,
                        ForeignKeyConstraint, Index, Integer, String, text)
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['roles.id'], name='users_ibfk_1'),
        Index('email', 'email', unique=True),
        Index('phone_number', 'phone_number', unique=True),
        Index('role_id', 'role_id'),
        Index('username', 'username', unique=True),
        Index('uuid', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(100))
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    phone_number: Mapped[Optional[str]] = mapped_column(String(15))
    role_id: Mapped[Optional[int]] = mapped_column(Integer,ForeignKey("roles.id"))
    status: Mapped[Optional[str]] = mapped_column(Enum('active', 'inactive', 'banned'), server_default=text("'inactive'"))
    last_login: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    # role: Mapped[Optional['Roles']] = relationship('Roles', back_populates='users')
    # activity_tracker: Mapped[Optional['ActivityTracker']] = relationship('ActivityTracker', back_populates='user')
    # meal_consumption: Mapped[Optional['MealConsumption']] = relationship('MealConsumption', back_populates='user')
    # sessions: Mapped[Optional['Sessions']] = relationship('Sessions', back_populates='user')
    # user_tokens: Mapped[Optional['UserTokens']] = relationship('UserTokens', back_populates='user')
    role = relationship('Roles', back_populates='users')
    activity_tracker = relationship('ActivityTracker', back_populates='user')
    meal_consumption = relationship('MealConsumption', back_populates='user')
    sessions = relationship('Sessions', back_populates='user')
    user_tokens = relationship('UserTokens', back_populates='user')