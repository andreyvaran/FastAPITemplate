import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from starlette import status
from app.config import Settings
from lib.db_accessor import DatabaseAccessor
from models.db import init_db, Base
from models.client import *
from endpoints.client import router as cl_router
from endpoints.tag import router as tg_router

# from app.endpoints import router_list, bind_routes


def bind_exceptions(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_error(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )


def bind_events(app: FastAPI, db_settings: dict) -> None:
    @app.on_event("startup")
    async def set_engine():
        db = DatabaseAccessor(db_settings=db_settings)
        await db.run()
        await db.init_db(Base)
        app.state.db = db

    @app.on_event("shutdown")
    async def close_engine():
        await app.state.db.stop()


def get_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(
        title="Menuda",
        description="Сервис уведомлений",
        docs_url="/swagger",
    )
    bind_events(app, settings.db_settings)
    bind_exceptions(app)
    app.include_router(cl_router, prefix="")
    app.include_router(tg_router, prefix="")

    # bind_routes(app, router_list)
    add_pagination(app)
    return app


app = get_app()
if __name__ == '__main__':

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
    )
