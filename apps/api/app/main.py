from fastapi import FastAPI

from app.api.chat import router as chat_router


def create_app() -> FastAPI:
    app = FastAPI(title="Enterprise AI Assistant API", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(chat_router)
    return app


app = create_app()
