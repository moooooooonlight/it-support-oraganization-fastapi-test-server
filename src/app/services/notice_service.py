from dataclasses import replace
from datetime import datetime, timezone
from typing import Optional, List, Tuple

from ..repositories.notice_repository import (
NoticeRepository, InMemoryNoticeRepository, NoticeRecord
)

class NotFoundError(Exception):
    """리소스를 찾지 못했을 때 서비스 계층에서 던지는 예외"""

class NoticeService:
    def __init__(self, repo: NoticeRepository) -> None:
        self._repo = repo

    def list(
            self,
            q: Optional[str],
            is_published: Optional[bool],
            order: str,
            limit: int,
            offset: int,
    ) -> Tuple[List[NoticeRecord], int]:
        items = self._repo.list_all()

        # 검색(제목/내용 LIKE)
        if q:
            q_lower = q.lower()
            items = [
                n for n in items
                if q_lower in n.title.lower() or q_lower in n.content.lower()
            ]

        # 게시여부 필터
        if is_published is not None:
            items = [n for n in items if n.is_published == is_published]

        if order == "latest":
            items.sort(key=lambda n: n.created_at, reverse=True)
        elif order == "oldest":
            items.sort(key=lambda n: n.created_at)
        else:  # pinned_first (default)
            # 핀(True)인 항목을 먼저, 그 안에서는 최신순
            items.sort(
                key=lambda n: (
                    not n.is_pinned,                 # 핀이면 먼저 (False < True)
                    -int(n.created_at.timestamp()),  # 최신 먼저
                )
            )

        total = len(items)
        sliced = items[offset: offset + limit]
        return sliced, total


    def get(self, notice_id:int) -> NoticeRecord:
        rec = self._repo.get(notice_id)
        if not rec:
            raise NotFoundError()
        return rec

    def create(
            self,
            title: str,
            content: str,
            is_pinned: bool,
            is_published: bool,
            author: Optional[str],
    ) -> NoticeRecord:
        now = datetime.now(timezone.utc)
        rec = NoticeRecord(
            id = 0,
            title=title,
            is_pinned=is_pinned,
            is_published=is_published,
            author=author,
            published_at=now if is_published else None,
        )
        return self._repo.create(rec)

    def update(
        self,
        notice_id: int,
        title: str,
        content: str,
        is_pinned: bool,
        is_published: bool,
        author: Optional[str],
    ) -> NoticeRecord:
        current = self.repo.get(notice_id)
        if not current:
            raise NotFoundError()

        # 게시 상태 변경 규칙
        published_at = current.published_at
        if is_published and not current.is_published:
            published_at = datetime.now(timezone.utc)  # 이제 막 게시됨
        if not is_published:
            published_at = None  # 게시 해제 시 null

        updated = replace(
            current,
            title=title,
            content=content,
            is_pinned=is_pinned,
            is_published=is_published,
            author=author,
            published_at=published_at,
        )
        return self._repo.update(updated)

    def set_pinned(self, notice_id: int, is_pinned: bool) -> NoticeRecord:
        current = self._repo.get(notice_id)
        if not current:
            raise NotFoundError()
        updated = replace(current, is_pinned=is_pinned)
        return self._repo.update(updated)


    def set_published(self, notice_id: int, is_published: bool) -> NoticeRecord:
        current = self._repo.get(notice_id)
        if not current:
            raise NotFoundError()
        published_at = current.is_published
        if is_published and not current.is_published:
            published_at = datetime.now(timezone.utc)
        if not is_published:
            published_at = None
        updated = replace(current, is_published=is_published, published_at=published_at)
        return self._repo.update(updated)

    def delete(self, notice_id: int) -> bool:
        ok = self._repo.delete(notice_id)
        if not ok:
            raise NotFoundError()
        return True

_repo_singleton = InMemoryNoticeRepository()
service_singleton = NoticeService(_repo_singleton)

def get_notice_service() -> NoticeService:
    return service_singleton