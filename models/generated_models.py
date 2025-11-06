from typing import Optional
import datetime
import decimal

from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Enum, ForeignKeyConstraint, Index, Integer, String, Table, Text, Time, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class ActivityTypes(Base):
    __tablename__ = 'activity_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))

    activity_tracker: Mapped[list['ActivityTracker']] = relationship('ActivityTracker', back_populates='activity_types')


class FoodTimings(Base):
    __tablename__ = 'food_timings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    meal_consumption: Mapped[list['MealConsumption']] = relationship('MealConsumption', back_populates='meal')


class MlText(Base):
    __tablename__ = 'ml_text'
    __table_args__ = (
        Index('text_code', 'text_code', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text_code: Mapped[str] = mapped_column(String(255), nullable=False)
    ENG: Mapped[Optional[str]] = mapped_column(String(255))

    target_attribute: Mapped[list['TargetAttribute']] = relationship('TargetAttribute', back_populates='ml_text')


class Permissions(Base):
    __tablename__ = 'permissions'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    role: Mapped[list['Roles']] = relationship('Roles', secondary='role_permissions', back_populates='permission')


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    permission: Mapped[list['Permissions']] = relationship('Permissions', secondary='role_permissions', back_populates='role')
    users: Mapped[list['Users']] = relationship('Users', back_populates='role')


t_role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', Integer, primary_key=True),
    Column('permission_id', Integer, primary_key=True),
    ForeignKeyConstraint(['permission_id'], ['permissions.id'], name='role_permissions_ibfk_2'),
    ForeignKeyConstraint(['role_id'], ['roles.id'], name='role_permissions_ibfk_1'),
    Index('permission_id', 'permission_id')
)


class TargetAttribute(Base):
    __tablename__ = 'target_attribute'
    __table_args__ = (
        ForeignKeyConstraint(['target_name'], ['ml_text.id'], name='target_attribute_ibfk_1'),
        Index('target_name', 'target_name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_name: Mapped[int] = mapped_column(Integer, nullable=False)
    target: Mapped[decimal.Decimal] = mapped_column(DECIMAL(6, 2), nullable=False)

    ml_text: Mapped['MlText'] = relationship('MlText', back_populates='target_attribute')


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
    role_id: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(Enum('active', 'inactive', 'banned'), server_default=text("'active'"))
    last_login: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    role: Mapped[Optional['Roles']] = relationship('Roles', back_populates='users')
    activity_tracker: Mapped[list['ActivityTracker']] = relationship('ActivityTracker', back_populates='user')
    meal_consumption: Mapped[list['MealConsumption']] = relationship('MealConsumption', back_populates='user')
    sessions: Mapped[list['Sessions']] = relationship('Sessions', back_populates='user')
    user_tokens: Mapped[list['UserTokens']] = relationship('UserTokens', back_populates='user')


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

    activity_types: Mapped['ActivityTypes'] = relationship('ActivityTypes', back_populates='activity_tracker')
    user: Mapped['Users'] = relationship('Users', back_populates='activity_tracker')


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

    meal: Mapped['FoodTimings'] = relationship('FoodTimings', back_populates='meal_consumption')
    user: Mapped['Users'] = relationship('Users', back_populates='meal_consumption')


class Sessions(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='sessions_ibfk_1'),
        Index('user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    user: Mapped['Users'] = relationship('Users', back_populates='sessions')


class UserTokens(Base):
    __tablename__ = 'user_tokens'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='user_tokens_ibfk_1'),
        Index('user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    token: Mapped[str] = mapped_column(Text, nullable=False)
    token_type: Mapped[Optional[str]] = mapped_column(Enum('access', 'refresh', 'reset'), server_default=text("'access'"))
    is_revoked: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='user_tokens')
