from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.core.config import get_settings
from src.core.jwt_verify import jwt_verify
from src.core.logger import logger

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("")
async def login(request: LoginRequest) -> dict:
    logger.info(f"Admin login request: {request}")
    aigc_admins = get_settings().aigc_admins
    if request.username not in aigc_admins:
        logger.warning(f"User {request.username} is not allowed to login as admin")
        raise HTTPException(
            status_code=403, detail="User is not allowed to login as admin"
        )
    token = jwt_verify.create_access_token({"user": request.username, "role": "aigc-admin"})
    return {
        "meta": {
            "accessToken": token
        }
    }
