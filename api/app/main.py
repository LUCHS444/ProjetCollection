from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from contextlib import asynccontextmanager

from app.routers import auth, items, collection
from app.core.config import settings
from app.db.session import init_db
import app.models
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Ma Collection API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"erreur": {"code": exc.status_code, "message": str(exc.detail)}},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = "; ".join(
        f"{'.'.join(str(p) for p in e['loc'][1:])} : {e['msg']}" for e in exc.errors()
    )
    return JSONResponse(
        status_code=422,
        content={"erreur": {"code": 422, "message": f"Données invalides ({details})"}},
    )


app.include_router(auth.router)
app.include_router(items.router)
app.include_router(collection.router)