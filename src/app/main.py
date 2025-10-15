from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.endpoints import notices

def create_app() -> FastAPI:
    app = FastAPI(
        title = "Notice Service",
        version = "0.0.1",
        description = "간단한 공지사항 API - InMemory방식 연습"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(notices.router, prefix="/api/v1")

    @app.get("/", tags=["health"])
    def health_check():
        return {"status": "ok", "service": "notice"}

    return app

app = create_app()

# 개발 환경에서 실행: python -m src.app.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000, reload=True)