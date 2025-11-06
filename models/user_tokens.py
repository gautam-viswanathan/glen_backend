import datetime
from typing import Optional

from db.base import Base
from models.users import Users
from sqlalchemy import (DateTime, Enum, ForeignKeyConstraint, Index, String,
                        Text, text)
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship


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
