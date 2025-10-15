from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, String, Text, DateTime, Enum as SAEnum, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


# 공지사항 상태 Enum 값.
class NoticeStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"

# 공지사항 엔티티
class Notice(Base):
    __tablename__ = "notices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[NoticeStatus] = mapped_column(SAEnum(NoticeStatus), default=NoticeStatus.DRAFT)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(),  onupdate=func.now(),nullable=False)