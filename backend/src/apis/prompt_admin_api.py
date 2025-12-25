import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.aigc.aigc import (
    AiProvider,
    CompletionChatMessage,
    CompletionChatMessageRole,
    CompletionReturnType,
)
from src.aigc.openai_proxy import OpenAiProxy
from src.core.db import get_async_session
from src.core.depend import verify_aigc_admin_jwt
from src.core.logger import logger
from src.models.api_model import ApiPageResponse
from src.models.prompt import PromptType
from src.aigc.multi_modal import MultiModal
from src.services.prompt_admin_service import (
    PromptAdminService,
    PromptResponse,
    PromptRequest,
)

router = APIRouter()


class PromptDebugRequest(BaseModel):
    message: str
    ai_provider: AiProvider | None = None
    model: str | None = None
    type: PromptType = PromptType.text
    return_type: CompletionReturnType = CompletionReturnType.text
    return_size: int = 1
    urls: list[str] | None = None


class PromptSynthesisResponse(BaseModel):
    urls: list[str]


class PromptRollbackRequest(BaseModel):
    target_id: int


@router.post("")
async def create_prompt(
        request: PromptRequest,
        user_uuid: str = Depends(verify_aigc_admin_jwt),
        session=Depends(get_async_session),
) -> PromptResponse:
    logger.info(f"create_prompt: {request} by user: {user_uuid}")
    return await PromptAdminService(session).create_prompt(request, user_uuid)


@router.put("/{prompt_id}")
async def update_prompt(
        prompt_id: int,
        request: PromptRequest,
        user_uuid: str = Depends(verify_aigc_admin_jwt),
        session=Depends(get_async_session),
) -> PromptResponse:
    logger.info(f"update_prompt: {request} by user: {user_uuid}")
    return await PromptAdminService(session).update(prompt_id, request, user_uuid)


@router.post("/{prompt_id}/enable")
async def enable_prompt(
        prompt_id: int,
        user_uuid: str = Depends(verify_aigc_admin_jwt),
        session=Depends(get_async_session),
) -> PromptResponse:
    logger.info(f"enable_prompt: {prompt_id} by user: {user_uuid}")
    return await PromptAdminService(session).enable(prompt_id, user_uuid)


@router.post("/{prompt_id}/disable")
async def disable_prompt(
        prompt_id: int,
        user_uuid: str = Depends(verify_aigc_admin_jwt),
        session=Depends(get_async_session),
) -> PromptResponse:
    logger.info(f"disable_prompt: {prompt_id} by user: {user_uuid}")
    return await PromptAdminService(session).disable(prompt_id, user_uuid)


@router.post("/{prompt_id}/publish")
async def publish_prompt(
        prompt_id: int,
        user_uuid: str = Depends(verify_aigc_admin_jwt),
        session=Depends(get_async_session),
) -> PromptResponse:
    logger.info(f"publish_prompt: {prompt_id} by user: {user_uuid}")
    return await PromptAdminService(session).publish(prompt_id, user_uuid)


@router.get("/{prompt_id}/history")
async def get_prompt_history(
        prompt_id: int,
        page: int = 1,
        size: int = 10,
        _: str = Depends(verify_aigc_admin_jwt),
        session=Depends(get_async_session),
) -> ApiPageResponse:
    return await PromptAdminService(session).get_history(prompt_id, page, size)


@router.post("/{prompt_id}/rollback")
async def rollback_prompt(
        prompt_id: int,
        request: PromptRollbackRequest,
        user_uuid: str = Depends(verify_aigc_admin_jwt),
        session=Depends(get_async_session),
) -> PromptResponse:
    logger.info(f"rollback_prompt: {prompt_id} to ¬ by user: {user_uuid}")
    return await PromptAdminService(session).rollback(
        prompt_id, request.target_id, user_uuid
    )


@router.delete("/{prompt_id}", status_code=204)
async def delete_prompt(
        prompt_id: int,
        user_uuid: str = Depends(verify_aigc_admin_jwt),
        session=Depends(get_async_session),
):
    logger.info(f"delete_prompt: {prompt_id} by user: {user_uuid}")
    await PromptAdminService(session).delete(prompt_id)


@router.get("/{prompt_id}")
async def get_prompt(
        prompt_id: int,
        _: str = Depends(verify_aigc_admin_jwt),
        session=Depends(get_async_session),
) -> PromptResponse:
    return await PromptAdminService(session).get_by_id(prompt_id)


@router.post("/chat/stream")
async def stream_chat_completion(
        request: PromptDebugRequest,
        _: str = Depends(verify_aigc_admin_jwt),
):
    async def event_gen():
        logger.info(f"stream_chat_completion: {request}")
        if request.type == PromptType.text:
            async for chunk in OpenAiProxy(
                    ai_provider=request.ai_provider
            ).invoke_openai_stream(
                messages=[
                    CompletionChatMessage(
                        role=CompletionChatMessageRole.user, content=request.message
                    )
                ],
                model=request.model,
            ):
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        # 目前仅支持 DashScope 的音视频多模态
        elif (
                request.type in (PromptType.audio, PromptType.video, PromptType.image)
                and request.ai_provider == AiProvider.dashscope
        ):
            async for chunk in MultiModal().stream(
                    message=request.message,
                    model=request.model,
                    prompt_type=request.type,
                    urls=request.urls,
            ):
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        else:
            yield f"data: {json.dumps({'type': 'error', 'data': 'Unsupported prompt type'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")


@router.get("")
async def get_prompts(
        page: int = 1,
        size: int = 10,
        keyword: str | None = None,
        ai_provider: AiProvider | None = None,
        enabled: bool | None = None,
        _: str = Depends(verify_aigc_admin_jwt),
        session=Depends(get_async_session),
) -> ApiPageResponse:
    return await PromptAdminService(session).get_prompts(
        page, size, keyword, ai_provider, enabled
    )
