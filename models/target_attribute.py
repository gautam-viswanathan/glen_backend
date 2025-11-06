from db.base import Base
from models.ml_text import MlText
from sqlalchemy import DECIMAL, ForeignKeyConstraint, Index, Integer, decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship


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

