from typing import Optional

from sqlalchemy import update, func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.prompt import Prompt, PromptStatus
from src.repository.base_repository import BaseRepository


class PromptRepository(BaseRepository):
    def __init__(self, session: Optional[AsyncSession] = None):
        super().__init__(Prompt, session)

    async def count_latest_prompts(
        self,
        keyword: str,
        ai_provider: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> int:
        async def query(session: AsyncSession):
            # Use select_from for better query optimization
            stmt = select(func.count()).select_from(Prompt).where(Prompt.is_latest == True)
            if keyword:
                stmt = stmt.where(
                    Prompt.name.like(f"%{keyword}%")  # noqa
                    | Prompt.title.like(f"%{keyword}%")  # noqa
                )
            if ai_provider:
                stmt = stmt.where(Prompt.ai_provider == ai_provider)
            if enabled is not None:
                stmt = stmt.where(Prompt.enabled == enabled)
            result = await session.exec(stmt)  # noqa
            return result.one()

        return await self._execute_func(query)

    async def search_latest_prompts(
        self,
        keyword: str,
        ai_provider: Optional[str] = None,
        enabled: Optional[bool] = None,
        page: int = 1,
        size: int = 10,
    ) -> list[Prompt]:
        async def query(session: AsyncSession):
            stmt = select(Prompt).where(Prompt.is_latest == True)
            if keyword:
                stmt = stmt.where(
                    Prompt.name.like(f"%{keyword}%")  # noqa
                    | Prompt.title.like(f"%{keyword}%")  # noqa
                )
            if ai_provider:
                stmt = stmt.where(Prompt.ai_provider == ai_provider)
            if enabled is not None:
                stmt = stmt.where(Prompt.enabled == enabled)
            stmt = stmt.order_by(Prompt.updated_at.desc())  # noqa
            stmt = stmt.offset((page - 1) * size).limit(size)
            result = await session.exec(stmt)  # noqa
            return result.all()

        return await self._execute_func(query)

    async def update_latest_flag_by_root_id(self, root_id: int, is_latest: bool):
        async def persist(session: AsyncSession):
            await session.exec(
                update(Prompt)  # noqa
                .where(Prompt.root_id == root_id)  # noqa
                .values(is_latest=is_latest)
                .execution_options(synchronize_session="fetch")
            )
            await session.commit()

        await self._execute_func(persist)

    async def get_max_version_by_root_id(self, root_id: int) -> Optional[int]:
        async def query(session: AsyncSession):
            result = await session.exec(
                select(Prompt.version)  # noqa
                .where(Prompt.root_id == root_id)  # noqa
                .order_by(Prompt.version.desc())  # noqa
                .limit(1)
            )
            max_version = result.first()
            return max_version

        return await self._execute_func(query)

    async def update_published_prompts_by_root_id(self, root_id: int):
        async def persist(session: AsyncSession):
            await session.exec(
                update(Prompt)  # noqa
                .where(Prompt.root_id == root_id)  # noqa
                .where(Prompt.status == PromptStatus.published)
                .values(status=PromptStatus.archived, is_latest=False)
                .execution_options(synchronize_session="fetch")
            )
            await session.commit()

        await self._execute_func(persist)

    async def get_enabled_by_name(self, name: str) -> list[Prompt]:
        async def query(session: AsyncSession):
            result = await session.exec(
                select(Prompt)  # noqa
                .where(Prompt.name == name)
                .where(Prompt.status == PromptStatus.published)
                .where(Prompt.enabled == True)
            )
            return result.all()

        return await self._execute_func(query)
