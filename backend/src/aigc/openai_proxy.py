import asyncio
import json
import logging

from openai import AsyncOpenAI, OpenAI

from src.aigc.aigc import (
    CompletionChatMessage,
    CompletionReturnType,
    AiProvider,
)
from src.core.config import get_settings

OPENAI_PROXY_URL = "https://api.openai.com/v1"
DASHSCOPE_PROXY_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEEPSEEK_PROXY_URL = "https://api.deepseek.com"


class OpenAiProxy:
    def __init__(
            self,
            api_key: str | None = None,
            base_url: str | None = None,
            ai_provider: AiProvider = AiProvider.openai,
    ):
        if not api_key:
            if ai_provider == AiProvider.openai:
                api_key = get_settings().openai_key
            elif ai_provider == AiProvider.dashscope:
                api_key = get_settings().ali_dashscope_api_key
            elif ai_provider == AiProvider.deepseek:
                api_key = get_settings().deepseek_api_key
        self.api_key = api_key
        self.ai_provider = ai_provider
        if not base_url:
            if ai_provider == AiProvider.openai:
                base_url = OPENAI_PROXY_URL
            elif ai_provider == AiProvider.dashscope:
                base_url = DASHSCOPE_PROXY_URL
            elif ai_provider == AiProvider.deepseek:
                base_url = DEEPSEEK_PROXY_URL
        self.base_url = base_url
        self.async_client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    async def invoke_openai_stream(
            self,
            messages: list[CompletionChatMessage],
            response_format: CompletionReturnType = CompletionReturnType.text,
            params: dict | None = None,
            model: str | None = None,
            **kwargs,  # noqa
    ):
        if params is None:
            params = {}
        if model is None:
            model = get_settings().openai_model
        assert model is not None
        openai_messages = await self._build_openai_messages(response_format, messages)
        logging.info(
            f"invoke_openai_stream: ai_provider: {self.ai_provider}, model: {model}, messages: {json.dumps(openai_messages, ensure_ascii=False)}, params: {json.dumps(params, ensure_ascii=False)}"
        )

        try:
            # Use async client directly for better performance
            stream = await self.async_client.chat.completions.create(
                model=model,
                messages=openai_messages,
                stream=True,
                stream_options={"include_usage": True},
                **params,
            )
            
            async for chunk in stream:
                if chunk.choices:
                    content = chunk.choices[0].delta.content or ""
                    if content:
                        yield {"type": "message", "data": content}
                elif chunk.usage:
                    yield {
                        "type": "usage",
                        "data": {
                            "completion_tokens": chunk.usage.completion_tokens,
                            "prompt_tokens": chunk.usage.prompt_tokens,
                            "total_tokens": chunk.usage.total_tokens,
                        },
                    }
                    yield {"type": "done", "data": "done"}
        except Exception as e:
            logging.error(f"invoke_openai_stream error: {e}")
            yield {"type": "error", "data": str(e)}

    async def _build_openai_messages(
            self,
            response_format: CompletionReturnType,
            messages: list[CompletionChatMessage],
    ):
        if (
                response_format == CompletionReturnType.json_object
                and self.ai_provider in (AiProvider.dashscope, AiProvider.deepseek)
        ):
            # dashscope and deepseek may not return correct json result
            if len(messages) == 1:
                messages[
                    0
                ].content += "\n## 注意：除了 json结果以外,禁止输出其他任何信息"
            if len(messages) > 1:
                messages[
                    -1
                ].content += "\n## 上述是用户的文本,请严格按照对话开始要求的json格式返回结果,除了 json结果以外,禁止输出其他任何信息"
        openai_messages = []
        for message in messages:
            if message.image_urls:
                images = [
                    {"type": "image_url", "image_url": {"url": url}}
                    for url in message.image_urls
                ]
                openai_messages.append(
                    {
                        "role": message.role,
                        "content": [
                            {"type": "text", "text": message.content},
                            *images,
                        ],
                    }
                )
            else:
                openai_messages.append(message.model_dump())

        return openai_messages


openai_proxy = OpenAiProxy()
