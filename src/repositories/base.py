from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

ModelT = TypeVar("ModelT", bound=DeclarativeBase)


class BaseRepository(Generic[ModelT]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def model(self) -> type[ModelT]:
        raise NotImplementedError

    async def save(self, instance: ModelT) -> ModelT:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def get(self, id: str) -> ModelT | None:
        stmt = select(self.model).where(self.model.id == id)  # type: ignore[attr-defined]
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        filters: dict[str, Any] | None = None,
    ) -> tuple[Sequence[ModelT], int]:
        stmt = select(self.model)
        count = select(func.count()).select_from(self.model)

        if filters:
            for col, val in filters.items():
                attr = getattr(self.model, col, None)
                if attr is not None and val is not None:
                    stmt = stmt.where(attr == val)
                    count = count.where(attr == val)

        total = (await self.session.execute(count)).scalar_one()
        items = (await self.session.execute(stmt.offset(offset).limit(limit))).scalars().all()
        return items, total

    async def delete(self, id: str) -> bool:
        obj = await self.get(id)
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.flush()
        return True
