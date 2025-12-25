import asyncio
import json
import logging

import dashscope
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.aigc.aigc import CompletionReturnType
from src.core.config import get_settings
from src.core.logger import logger
from src.models.prompt import PromptType

DEFAULT_VIDEO_FPS = 2


class MultiModalPromptResponse(BaseModel):
    origin_text: str
    data: dict | None = None
    completion_tokens: int | None = None
    prompt_tokens: int | None = None
    total_tokens: int | None = None


class MultiModal:
    def __init__(
            self,
            session: AsyncSession | None = None,
    ):
        self.session = session

    async def stream(
            self,
            message: str,
            model: str,
            prompt_type: PromptType,
            urls: list[str] = None,
    ):
        messages = self._build_messages(prompt_type, urls, message)

        def _sync_stream():
            # noinspection PyTypeChecker
            return dashscope.MultiModalConversation.call(
                model=model,
                api_key=get_settings().ali_dashscope_api_key,
                messages=messages,
                stream=True,
                incremental_output=True,
            )

        try:
            stream = await asyncio.to_thread(_sync_stream)
            for chunk in stream:
                if chunk["output"]["choices"][0]["message"].content:
                    text = chunk["output"]["choices"][0]["message"].content[0]["text"]
                    yield {"type": "message", "data": text}
            yield {"type": "done", "data": "done"}
        except Exception as e:
            logging.error(f"invoke_openai_stream error: {e}")
            yield {"type": "error", "data": str(e)}

    def _build_messages(self, prompt_type: PromptType, urls: list[str], text: str):
        if prompt_type == PromptType.audio:
            return [
                {
                    "role": "user",
                    "content": [*({"audio": u} for u in urls), {"text": text}],
                }
            ]
        elif prompt_type == PromptType.video:
            return [
                {
                    "role": "user",
                    "content": [
                        *({"video": u, "fps": DEFAULT_VIDEO_FPS} for u in urls),
                        {"text": text},
                    ],
                }
            ]
        elif prompt_type == PromptType.image:
            return [
                {
                    "role": "user",
                    "content": [*({"image": u} for u in urls), {"text": text}],
                }
            ]
        else:
            raise ValueError(f"Unsupported prompt_type: {prompt_type}")

    def _handle_response_text(
            self, origin_text: str, return_type: CompletionReturnType
    ) -> MultiModalPromptResponse:
        data = None
        text = origin_text.strip()
        if text.startswith("```json") and text.endswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
        if return_type == CompletionReturnType.json_object:
            try:
                data = json.loads(text)
            except Exception:  # noqa
                logger.error(f"Failed to parse json: {text}")
                data = None
        return MultiModalPromptResponse(origin_text=origin_text, data=data)
