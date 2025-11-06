
# import datetime
from typing import Optional

from db.base import Base
from sqlalchemy import (Column, ForeignKeyConstraint, Index, Integer, String,
                        Table, text)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    permission = relationship('Permissions', secondary='role_permissions', back_populates='role')
    users = relationship('Users', back_populates='role')


t_role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', Integer, primary_key=True),
    Column('permission_id', Integer, primary_key=True),
    ForeignKeyConstraint(['permission_id'], ['permissions.id'], name='role_permissions_ibfk_2'),
    ForeignKeyConstraint(['role_id'], ['roles.id'], name='role_permissions_ibfk_1'),
    Index('permission_id', 'permission_id')
)

