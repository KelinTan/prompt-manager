from pydantic import BaseModel


class ApiDataResponse(BaseModel):
    data: dict | str | None = None


class ApiPageResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list = []
