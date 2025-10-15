from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from ....core.pagination import PageMeta
from ....schemas.notice import (
    Notice, NoticeCreate, NoticeUpdate, PinUpdate, PublishUpdate, Order
)
from ....services.notice_service import (
    NoticeService, get_notice_service, NotFoundError
)


router = APIRouter(prefix="/notice", tags=["notice"])

@router.get("",response_model=dict)
def list_notices(
        q: Optional[str] = None,
        is_pusblished: Optional[bool] = None,
        order: Order = Query("pinned_first"),
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0),
        svc: NoticeService = Depends(get_notice_service),
):
    items, total = svc.list(q, is_pusblished, order, limit, offset)
    data = [Notice.model_valiate(i) for i in items]
    meta = PageMeta(total=total, limit=limit, offset=offset)
    return {"items":data, "meta":meta}

@router.post("", response_model=Notice, status_code=status.HTTP_201_CREATED)
def create_notice(
        body: NoticeCreate,
        svc: NoticeService = Depends(get_notice_service),
):
    rec = svc.create(
        title=body.title,
        content=body.content,
        is_pinned=body.is_pinned,
        is_published=body.is_published,
        author=body.author,
    )
    return Notice.model_validate(rec)

@router.put("/{notice_id}", response_model=Notice)
def update_notice(
        notice_id: int,
        body: NoticeUpdate,
        svc: NoticeService = Depends(get_notice_service),
):
    try:
        rec = svc.update(
            notice_id=notice_id,
            title=body.title,
            content=body.content,
            is_pinned=body.is_pinned,
            is_published=body.is_published,
            author=body.author,
        )
        return Notice.model_validate(rec)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found")

@router.get("/{notice_id}/pin", response_model=Notice)
def set_pin(
        notice_id: int,
        body: PinUpdate,
        svc: NoticeService = Depends(get_notice_service),
):
    try:
        rec = svc.set_pinned(notice_id, body.is_pinned)
        return Notice.model_validate(rec)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found")

@router.patch("/{notice_id}/publish", response_model=Notice)
def set_publish(
    notice_id: int,
    body: PublishUpdate,
    svc: NoticeService = Depends(get_notice_service),
):
    try:
        rec = svc.set_published(notice_id, body.is_published)
        return Notice.model_validate(rec)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Notice not found")


@router.delete("/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notice(
    notice_id: int,
    svc: NoticeService = Depends(get_notice_service),
):
    try:
        svc.delete(notice_id)
        return None
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Notice not found")