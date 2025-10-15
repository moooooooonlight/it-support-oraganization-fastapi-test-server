from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.models.notice import Notice
from app.db.session import get_db
from app.schemas.notice import NoticeRead, NoticeCreate, NoticeUpdate

router = APIRouter(prefix="/notices", tags=["notices"])

@router.post("/", response_model=NoticeRead, status_code= status.HTTP_201_CREATED,)
def create_notice(body: NoticeCreate, db: Session = Depends(get_db)):
    notice = Notice(
        title = body.title,
        content = body.content,
        status = body.status,
    )

    db.add(notice)
    db.commit()
    db.refresh(notice)
    return NoticeRead.model_validate(notice)

@router.get("/{notice_id}", response_model=NoticeRead)
def get_notice(notice_id: int, db: Session = Depends(get_db)):
    notice = db.get(Notice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return NoticeRead.model_validate(notice)

@router.get("", response_model=list[NoticeRead])
def list_notices(db: Session = Depends(get_db)):
    rows = db.query(Notice).order_by(Notice.id.desc()).all()
    return [NoticeRead.model_validate(n) for n in rows]

@router.patch("/{notice_id}", response_model=NoticeRead)
def update_notice(notice_id: int, body: NoticeUpdate, db: Session = Depends(get_db)):
    notice = db.get(Notice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    notice.title = body.title
    notice.content = body.content
    notice.status = body.status

    db.commit()
    db.refresh(notice)
    return NoticeRead.model_validate(notice)


@router.delete("/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    notice = db.get(Notice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    db.delete(notice)
    db.commit()
    return None