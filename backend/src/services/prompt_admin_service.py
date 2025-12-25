from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.aigc.aigc import CompletionReturnType, AiProvider
from src.models.api_model import ApiPageResponse
from src.models.prompt import Prompt, PromptType, FormatType, PromptStatus
from src.repository.base_repository import FilterOp
from src.repository.prompt_repository import PromptRepository
from src.utils.date import format_cst_datetime


class PromptResponse(BaseModel):
    id: int
    title: str | None
    name: str
    template: str
    type: PromptType = PromptType.text
    model: str | None = None
    mock: bool
    mock_data: str | None = None
    return_type: CompletionReturnType = CompletionReturnType.text
    format_type: FormatType = FormatType.braces
    remark: str | None = None
    ai_provider: AiProvider | None = None
    is_latest: bool
    version: int
    enabled: bool
    status: PromptStatus
    created_at: datetime
    updated_at: datetime


class PromptRequest(BaseModel):
    title: str | None = None
    name: str
    template: str
    type: PromptType = PromptType.text
    model: str | None = None
    mock: bool = True
    mock_data: str | None = None
    return_type: CompletionReturnType = CompletionReturnType.text
    format_type: FormatType = FormatType.braces
    remark: str | None = None
    ai_provider: AiProvider | None = None


class PromptAdminService:
    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session
        self.prompt_repository = PromptRepository(session)

    async def create_prompt(
            self, request: PromptRequest, user_uuid: str
    ) -> PromptResponse:
        prompt = Prompt(**request.model_dump())
        prompt.status = PromptStatus.draft
        prompt.is_latest = True
        prompt.version = 1
        prompt.created_by = user_uuid
        prompt.updated_by = user_uuid
        await self.prompt_repository.save(prompt)
        prompt.root_id = prompt.id
        await self.prompt_repository.save(prompt)
        return await self._build_prompt_response(prompt)

    async def enable(self, prompt_id: int, user_uuid: str) -> PromptResponse:
        prompt = await self.prompt_repository.get_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with id {prompt_id} not found")
        prompt.enabled = True
        prompt.updated_by = user_uuid
        await self.prompt_repository.save(prompt)
        return await self._build_prompt_response(prompt)

    async def disable(self, prompt_id: int, user_uuid: str) -> PromptResponse:
        prompt = await self.prompt_repository.get_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with id {prompt_id} not found")
        prompt.enabled = False
        prompt.updated_by = user_uuid
        await self.prompt_repository.save(prompt)
        return await self._build_prompt_response(prompt)

    async def update(
            self, prompt_id: int, request: PromptRequest, user_uuid: str
    ) -> PromptResponse:
        prompt = await self.prompt_repository.get_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with id {prompt_id} not found")
        latest_draft_prompt = await self.prompt_repository.get_list(
            filters=[
                ("status", FilterOp.EQ, PromptStatus.draft),
                ("is_latest", FilterOp.EQ, True),
                ("root_id", FilterOp.EQ, prompt.root_id or prompt.id),
            ]
        )
        if latest_draft_prompt:
            # 已有草稿，更新草稿
            latest_draft = latest_draft_prompt[0]
            for key, value in request.model_dump().items():
                setattr(latest_draft, key, value)
            latest_draft.updated_by = user_uuid
            await self.prompt_repository.save(latest_draft)
            return await self._build_prompt_response(latest_draft)
        elif prompt.status == PromptStatus.published:
            # 已发布，创建新草稿
            new_prompt = Prompt(**request.model_dump())
            new_prompt.status = PromptStatus.draft
            new_prompt.is_latest = True
            new_prompt.version = (
                                         await self.prompt_repository.get_max_version_by_root_id(
                                             prompt.root_id or prompt.id
                                         )
                                         or 1
                                 ) + 1
            new_prompt.root_id = prompt.root_id or prompt.id
            new_prompt.created_by = user_uuid
            new_prompt.updated_by = user_uuid
            await self.prompt_repository.save(new_prompt)
            # 更新当前最新草稿标记
            prompt.is_latest = False
            await self.prompt_repository.save(prompt)
            return await self._build_prompt_response(new_prompt)
        else:
            # 草稿，更新草稿
            for key, value in request.model_dump().items():
                setattr(prompt, key, value)
            prompt.updated_by = user_uuid
            await self.prompt_repository.save(prompt)
            return await self._build_prompt_response(prompt)

    async def rollback(
            self, prompt_id: int, target_id: int, user_uuid: str
    ) -> PromptResponse:
        current_prompt = await self.prompt_repository.get_by_id(prompt_id)
        if not current_prompt:
            raise ValueError(f"Prompt with id {prompt_id} not found")
        target_prompt = await self.prompt_repository.get_by_id(target_id)
        if not target_prompt:
            raise ValueError(f"Target prompt with id {target_id} not found")
        root_id = current_prompt.root_id or current_prompt.id
        max_version = await self.prompt_repository.get_max_version_by_root_id(root_id)
        # 创建新的草稿，内容复制自目标版本
        rollback_prompt = Prompt(
            title=target_prompt.title,
            name=target_prompt.name,
            template=target_prompt.template,
            type=target_prompt.type,
            model=target_prompt.model,
            mock=target_prompt.mock,
            mock_data=target_prompt.mock_data,
            return_type=target_prompt.return_type,
            format_type=target_prompt.format_type,
            remark=f"[Rollback from v{target_prompt.version}] {target_prompt.remark or ''}",
            ai_provider=target_prompt.ai_provider,
            status=PromptStatus.draft,
            is_latest=True,
            version=max_version + 1,  # 新版本号
            root_id=root_id,
            created_by=user_uuid,
            updated_by=user_uuid,
        )

        await self.prompt_repository.update_latest_flag_by_root_id(root_id, False)
        await self.prompt_repository.save(rollback_prompt)
        return await self._build_prompt_response(rollback_prompt)

    async def get_history(
            self, prompt_id: int, page: int = 1, size: int = 10
    ) -> ApiPageResponse:
        prompt = await self.prompt_repository.get_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with id {prompt_id} not found")
        root_id = prompt.root_id or prompt.id
        prompts = await self.prompt_repository.get_by_page(
            page=page,
            size=size,
            filters=[
                ("root_id", FilterOp.EQ, root_id),
            ],
            order_by=[("version", "desc")],
        )
        prompts_count = await self.prompt_repository.count(
            filters=[("root_id", FilterOp.EQ, root_id)]
        )
        return ApiPageResponse(
            total=prompts_count,
            page=page,
            size=size,
            items=await self._build_prompt_responses(prompts),
        )

    async def publish(self, prompt_id: int, user_uuid: str) -> PromptResponse:
        prompt: Prompt = await self.prompt_repository.get_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with id {prompt_id} not found")
        draft_prompts = await self.prompt_repository.get_list(
            filters=[
                ("status", FilterOp.EQ, PromptStatus.draft),
                ("is_latest", FilterOp.EQ, True),
                ("root_id", FilterOp.EQ, prompt.root_id or prompt.id),
            ]
        )
        if draft_prompts:
            prompt = draft_prompts[0]
        if prompt.status == PromptStatus.published:
            return await self._build_prompt_response(prompt)
        # mark all other prompts with the same root_id as archived
        await self.prompt_repository.update_published_prompts_by_root_id(
            prompt.root_id or prompt.id
        )
        prompt.status = PromptStatus.published
        prompt.is_latest = True
        prompt.updated_by = user_uuid
        await self.prompt_repository.save(prompt)
        return await self._build_prompt_response(prompt)

    async def delete(self, prompt_id: int) -> None:
        existing_prompt = await self.prompt_repository.get_by_id(prompt_id)
        if not existing_prompt:
            raise ValueError(f"Prompt with id {prompt_id} not found")
        await self.prompt_repository.delete(existing_prompt)

    async def get_by_id(self, prompt_id: int) -> PromptResponse:
        prompt = await self.prompt_repository.get_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with id {prompt_id} not found")
        return await self._build_prompt_response(prompt)

    async def get_prompts(
            self,
            page: int = 1,
            size: int = 10,
            keyword: str | None = None,
            ai_provider: AiProvider | None = None,
            enabled: bool | None = None,
    ) -> ApiPageResponse:
        prompts = await self.prompt_repository.search_latest_prompts(
            page=page,
            size=size,
            keyword=keyword or "",
            ai_provider=ai_provider,
            enabled=enabled,
        )
        prompts_count = await self.prompt_repository.count_latest_prompts(
            keyword or "", ai_provider, enabled
        )
        return ApiPageResponse(
            total=prompts_count,
            page=page,
            size=size,
            items=await self._build_prompt_responses(prompts),
        )

    async def _build_prompt_response(self, prompt: Prompt) -> PromptResponse:
        return PromptResponse(
            id=prompt.id,
            title=prompt.title,
            name=prompt.name,
            template=prompt.template,
            type=prompt.type,
            model=prompt.model,
            mock=prompt.mock,
            mock_data=prompt.mock_data,
            return_type=prompt.return_type,
            format_type=prompt.format_type,
            remark=prompt.remark,
            ai_provider=prompt.ai_provider,
            created_at=format_cst_datetime(prompt.created_at),
            updated_at=format_cst_datetime(prompt.updated_at),
            is_latest=prompt.is_latest,
            version=prompt.version,
            enabled=prompt.enabled,
            status=prompt.status,
        )

    async def _build_prompt_responses(
            self, prompts: list[Prompt]
    ) -> list[PromptResponse]:
        # Use list comprehension directly for better performance
        # This is not N+1 as each prompt object already has all needed data
        responses = []
        for prompt in prompts:
            responses.append(PromptResponse(
                id=prompt.id,
                title=prompt.title,
                name=prompt.name,
                template=prompt.template,
                type=prompt.type,
                model=prompt.model,
                mock=prompt.mock,
                mock_data=prompt.mock_data,
                return_type=prompt.return_type,
                format_type=prompt.format_type,
                remark=prompt.remark,
                ai_provider=prompt.ai_provider,
                created_at=format_cst_datetime(prompt.created_at),
                updated_at=format_cst_datetime(prompt.updated_at),
                is_latest=prompt.is_latest,
                version=prompt.version,
                enabled=prompt.enabled,
                status=prompt.status,
            ))
        return responses
