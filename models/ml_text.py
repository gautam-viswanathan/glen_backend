# import datetime
from typing import Optional

from db.base import Base
from models.target_attribute import TargetAttribute
from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MlText(Base):
    __tablename__ = 'ml_text'
    __table_args__ = (
        Index('text_code', 'text_code', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text_code: Mapped[str] = mapped_column(String(255), nullable=False)
    ENG: Mapped[Optional[str]] = mapped_column(String(255))

    target_attribute: Mapped[list['TargetAttribute']] = relationship('TargetAttribute', back_populates='ml_text')
