from __future__ import annotations
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


# 요청 DTO
class NoticeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    content: str = Field(min_length=1)
    is_pinned: bool = False
    is_published: bool = False
    author: Optional[str] = None

class NoticeUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    content: str = Field(min_length=1)
    is_pinned: bool = False
    is_published: bool = False
    author: Optional[str] = None

class PinUpdate(BaseModel):
    is_pinned: bool

class PublishUpdate(BaseModel):
    is_published: bool

# 조회 파라미터
Order = Literal["latest", "oldest", "pinned_first"]

# 응답 DTO
class Notice(BaseModel):
    id: int
    title: str
    content: str
    is_pinned: bool
    is_published: bool
    author: Optional[str]
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

    class Config:
        from_attributes = True  # pydantic v2: dataclass/obj 매핑에 유용