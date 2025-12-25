from enum import Enum, StrEnum

from pydantic import BaseModel, Field


class AiProvider(StrEnum):
    openai = "openai"
    dashscope = "dashscope"
    deepseek = "deepseek"


class CompletionReturnType(str, Enum):
    json_object = "json_object"
    text = "text"
    image = "image"


class CompletionChatMessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class CompletionChatMessage(BaseModel):
    role: CompletionChatMessageRole
    content: str
    image_urls: list[str] | None = None
    additional_kwargs: dict | None = Field(default=None)


class AigcResult(BaseModel):
    content: str
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
