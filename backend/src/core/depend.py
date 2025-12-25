from fastapi import Request, HTTPException
from pydantic import BaseModel

from src.core.config import get_settings
from src.core.jwt_verify import jwt_verify


class JwtUser(BaseModel):
    sub: str
    token: str


def verify_jwt(request: Request) -> JwtUser:
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Authorization header is invalid format"
        )
    authorization_arr = authorization.split(" ")
    if len(authorization_arr) != 2:
        raise HTTPException(
            status_code=401, detail="Authorization header is invalid format"
        )
    token = authorization_arr[1]
    payload = jwt_verify.verify_token(token)
    username = payload.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="sub is missing")
    return JwtUser(token=token, sub=username)


def verify_aigc_admin_jwt(request: Request) -> str:
    jwt_user = verify_jwt(request)
    aigc_admins = get_settings().aigc_admins
    if jwt_user.sub not in aigc_admins:
        raise HTTPException(status_code=403, detail="User is not allowed to access")
    return jwt_user.sub
