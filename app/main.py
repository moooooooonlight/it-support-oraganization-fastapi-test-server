from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
# noqa: F401 (사용안해도 임포트 필요) -> TODO 이유?
from app.db.models import notice as notice_model
from app.api.routers.notices import router as notices_router  # ★ 추가

app = FastAPI(
    title = "Notice Service Practice",
    description = "간단한 공지사항 API"
)

app.include_router(notices_router)

# 앱 시작 시 테이블 생성 TODO (간단한 방법 -> 수정 필요?)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status":"OK"}