from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class NoticeStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISH = "PUBLISH"

class NoticeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    status: NoticeStatus = NoticeStatus.DRAFT

class NoticeUpdate(BaseModel):
    title : str = Field(default=None, min_length=1, max_length=100)
    content: str = Field(min_length=1)
    status: Optional[NoticeStatus] = None

# 단건 응답 DTO (읽기 전용 필드 포함)
class NoticeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # SQLAlchemy 객체 -> Pydantic 변환 허용
    id: int
    title: str
    content: str
    status: NoticeStatus
    created_at: datetime
    updated_at: datetime


# 목록 응답 DTO (페이지네이션용)
class NoticeListResponse(BaseModel):
    items: List[NoticeRead]
    page: int
    size: int
    total: int
