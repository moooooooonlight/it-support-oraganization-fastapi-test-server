from __future__ import annotations
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Dict, List, Optional, Protocol

# === 도메인 모델(리포지토리 내부 표현) ===
@dataclass
class NoticeRecord:
    id: int
    title: str
    content: str
    is_pinned: bool = False
    is_published: bool = False
    author: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# === 레포지토리 인터페이스 ===
class NoticeRepository(Protocol):
    def list_all(self) -> List[NoticeRecord]: ...
    def get(self, notice_id: int) -> Optional[NoticeRecord]: ...
    def create(self, rec: NoticeRecord) -> NoticeRecord: ...
    def update(self, rec: NoticeRecord) -> NoticeRecord: ...
    def delete(self, notice_id: int) -> bool: ...

class InMemoryNoticeRepository(NoticeRepository):
    """간단한 인메모리 저장소. 나중에 SQLAlchemy 저장소로 교체 가능"""
    def __init__(self) -> None:
        self._db: Dict[int, NoticeRecord] = {}
        self._seq: int = 0

    def _next_id(self) -> int:
        self._seq += 1
        return self._seq

    def list_all(self) -> List[NoticeRecord]:
        return list(self._db.values())

    def get(self, notice_id: int) -> Optional[NoticeRecord]:
        return self._db.get(notice_id)

    def create(self, rec: NoticeRecord) -> NoticeRecord:
        # ID 자동 발급 + 타임스탬프 초기화
        if rec.id == 0:
            rec = replace(rec, id=self._next_id())
        now = datetime.now(timezone.utc)
        rec = replace(rec, created_at=now, updated_at=now)
        self._db[rec.id] = rec
        return rec

    def update(self, rec: NoticeRecord) -> NoticeRecord:
        if rec.id not in self._db:
            raise KeyError("Notice not found")
        rec = replace(rec, updated_at=datetime.now(timezone.utc))
        self._db[rec.id] = rec
        return rec

    def delete(self, notice_id: int) -> bool:
        return self._db.pop(notice_id, None) is not None
