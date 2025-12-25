from enum import Enum
from typing import TypeVar, Type, Optional, Callable, Any, List, Tuple

from sqlalchemy import func
from sqlmodel import select, asc, desc
from sqlmodel.ext.asyncio.session import AsyncSession

T = TypeVar("T")


class FilterOp(str, Enum):
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    IN = "in"
    LIKE = "like"


class OrderDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


ConditionType = Tuple[str, FilterOp, Any | None]
OrderByType = List[Tuple[str, OrderDirection]]


class BaseRepository:
    def __init__(self, model: Type[T], session: Optional[AsyncSession] = None):
        self.model = model
        self.session = session

    async def _get_session(self) -> AsyncSession:
        """Get the session to use for the query."""
        if self.session is not None:
            return self.session
        else:
            from src.core.db import async_engine

            return AsyncSession(async_engine)

    async def _execute_func(self, callable_func: Callable[[AsyncSession], Any]) -> Any:
        """
        Execute a query function with the session.
        """
        if self.session:
            return await callable_func(self.session)
        else:
            from src.core.db import async_engine

            async with AsyncSession(async_engine) as session:
                return await callable_func(session)

    async def get_by_uuids(self, uuids: List[str]) -> List[T]:
        """Get objects by UUIDs."""

        if not uuids:
            return []

        async def query(session: AsyncSession):
            result = await session.exec(
                select(self.model).where(self.model.uuid.in_(uuids))  # noqa
            )
            return result.all()

        return await self._execute_func(query)

    async def get_by_uuid(self, uuid: str) -> Optional[T]:
        """Get an object by UUID."""

        async def query(session: AsyncSession):
            result = await session.exec(
                select(self.model).where(self.model.uuid == uuid)  # noqa
            )
            return result.first()

        return await self._execute_func(query)

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        """Get an object by ID."""

        async def query(session: AsyncSession):
            result = await session.exec(
                select(self.model).where(self.model.id == obj_id)  # noqa
            )
            return result.first()

        return await self._execute_func(query)

    async def get_by_ids(self, ids: List[int]) -> List[T]:
        """Get objects by IDs."""

        if not ids:
            return []

        async def query(session: AsyncSession):
            result = await session.exec(
                select(self.model).where(self.model.id.in_(ids))  # noqa
            )
            return result.all()

        return await self._execute_func(query)

    async def batch_save(self, objs: List[T]) -> List[T]:
        """Save a list of objects."""

        async def persist(session: AsyncSession):
            session.add_all(objs)
            await session.commit()
            return objs

        return await self._execute_func(persist)

    async def save(self, obj: T) -> T:
        """Save an object."""

        async def persist(session: AsyncSession):
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

        return await self._execute_func(persist)

    async def get_by_page(
        self,
        page: int = 1,
        size: int = 10,
        filters: Optional[List[ConditionType]] = None,
        order_by: Optional[List[Tuple[str, str]]] = None,
    ) -> List[T]:
        async def query(session: AsyncSession):
            stmt = select(self.model)
            stmt = await self._apply_filters(stmt, filters)
            stmt = await self._apply_order_by(stmt, order_by)
            stmt = stmt.offset((page - 1) * size).limit(size)
            result = await session.exec(stmt)
            return result.all()

        return await self._execute_func(query)

    async def get_list(
        self,
        filters: Optional[List[ConditionType]] = None,
        order_by: Optional[List[Tuple[str, str]]] = None,
    ) -> List[T]:
        async def query(session: AsyncSession):
            stmt = select(self.model)
            stmt = await self._apply_filters(stmt, filters)
            stmt = await self._apply_order_by(stmt, order_by)
            result = await session.exec(stmt)
            return result.all()

        return await self._execute_func(query)

    async def count(self, filters: Optional[List[ConditionType]] = None) -> int:
        async def query(session: AsyncSession):
            stmt = select(func.count()).select_from(self.model)
            stmt = await self._apply_filters(stmt, filters)
            result = await session.exec(stmt)
            return result.one()

        return await self._execute_func(query)

    async def delete(self, obj: T) -> None:
        """Delete an object."""

        async def persist(session: AsyncSession):
            await session.delete(obj)
            await session.commit()

        await self._execute_func(persist)

    async def _apply_filters(
        self,
        stmt,
        filters: Optional[List[ConditionType]] = None,
    ):
        """通用条件处理，返回 stmt"""
        if filters:
            for field, op, value in filters:
                if value is None:
                    continue
                col = getattr(self.model, field)
                if op == FilterOp.EQ:
                    stmt = stmt.where(col == value)
                elif op == FilterOp.NE:
                    stmt = stmt.where(col != value)
                elif op == FilterOp.LT:
                    stmt = stmt.where(col < value)
                elif op == FilterOp.LE:
                    stmt = stmt.where(col <= value)
                elif op == FilterOp.GT:
                    stmt = stmt.where(col > value)
                elif op == FilterOp.GE:
                    stmt = stmt.where(col >= value)
                elif op == FilterOp.IN:
                    stmt = stmt.where(col.in_(value))
                elif op == FilterOp.LIKE:
                    stmt = stmt.where(col.like(f"%{value}%"))
        return stmt

    async def _apply_order_by(
        self, stmt, order_by: Optional[List[Tuple[str, OrderDirection]]] = None
    ):
        if order_by:
            order_clauses = []
            for field, direction in order_by:
                col = getattr(self.model, field)
                order_clauses.append(
                    asc(col) if direction == OrderDirection.ASC else desc(col)
                )
            stmt = stmt.order_by(*order_clauses)
        return stmt
