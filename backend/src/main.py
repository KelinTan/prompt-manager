import os
import time
from contextlib import asynccontextmanager
from typing import Annotated

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id import correlation_id
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.apis.login_admin_api import router as admin_login_router
from src.apis.prompt_admin_api import router as admin_prompt_router
from src.core.config import Settings, get_settings
from src.core.logger import setup_logger, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App starting up...")
    setup_logger()
    yield
    logger.info("App shutting down...")


openapi_url = get_settings().app_env.is_not_prod() and "/openapi.json" or None
app = FastAPI(openapi_url=openapi_url, lifespan=lifespan)


ADMIN_API = f"/admin/api"

#  Admin service endpoints
ADMIN_PROMPT_API = f"{ADMIN_API}/prompts"
ADMIN_LOGIN_API = f"{ADMIN_API}/login"

app.include_router(admin_prompt_router, prefix=ADMIN_PROMPT_API, tags=["admin"])
app.include_router(admin_login_router, prefix=ADMIN_LOGIN_API, tags=["admin"])


@app.middleware("http")
async def log_process_time(request: Request, call_next):
    if request.url.path in ("/ping",) or request.url.path.startswith("/actuator"):
        return await call_next(request)

    start_time = time.time()
    logger.info(f"API Start: {request.method} {request.url.path}")
    status = 200
    try:
        response = await call_next(request)
        status = response.status_code
    except HTTPException as e:
        status = e.status_code
        logger.warning(
            f"API HTTPException: uri={request.url.path}, status={status}, detail={e.detail}"
        )
        raise
    except Exception as e:
        status = 500
        logger.exception(f"API Exception: uri={request.url.path}, error={e}")
        raise
    finally:
        process_time = int((time.time() - start_time) * 1000)
        if status >= 500:
            logger.error(
                f"API failed: uri={request.url.path}, status={status}, time={process_time}ms",
            )
        elif status >= 400:
            logger.warning(
                f"API failed: uri={request.url.path}, status={status}, time={process_time}ms",
            )
        else:
            logger.info(
                f"API success: uri={request.url.path}, status={status}, time={process_time}ms",
            )

    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error at {request.url.path}: {exc.errors()}")
    return build_error_response(
        request,
        message="请求参数错误",
        status_code=422,
        details=str(exc.errors()),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP exception: {exc.status_code} {exc.detail}")
    return build_error_response(
        request,
        message=exc.detail,
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return build_error_response(
        request,
        message="服务器内部错误，请稍后再试",
        status_code=500,
    )


def build_error_response(
        request: Request,
        message: str,
        status_code: int = 500,
        error_code: str | None = None,
        details: dict | list | str | None = None,
):
    request_id = correlation_id.get() or "unknown"
    content = {
        "status": "error",
        "path": request.url.path,
        "message": message,
        "request_id": request_id,
    }
    if error_code:
        content["error_code"] = error_code
    if details:
        content["details"] = details
    return JSONResponse(status_code=status_code, content=content)


app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIdMiddleware, validator=None)  # type: ignore


@app.get("/ping")
def hello():
    return {"Hello": "World"}


@app.get("/actuator/health")
def health():
    return {"status": "UP"}


@app.get("/settings")
def settings(config: Annotated[Settings, Depends(get_settings)]):
    if get_settings().app_env.is_not_prod():
        return config.model_dump()
    else:
        raise HTTPException(status_code=404, detail="Not Found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
