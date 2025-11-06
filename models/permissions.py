# import datetime
from typing import Optional

from db.base import Base
from models.roles import Roles
from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Permissions(Base):
    __tablename__ = 'permissions'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    role: Mapped[list['Roles']] = relationship('Roles', secondary='role_permissions', back_populates='permission')
