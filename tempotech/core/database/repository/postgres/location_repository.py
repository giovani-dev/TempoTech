from typing import Optional

from sqlalchemy import Engine, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session

from tempotech.core.database.models.location_model import LocationModel
from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.schemas.location_schema import Location


class LocationRepository(IDefaultRepository[Location]):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: Location):
        model = LocationModel(
            state_name=data.state_name,
            state=data.state,
            country=data.country,
            city_name=data.city_name if data.city_name else None,
            latitude=data.coordinates.latitude if data.coordinates else None,
            longitude=data.coordinates.longitude if data.coordinates else None,
        )
        self._session.add(model)
        await self._session.commit()

    async def update(self, data: Location, id: int):
        raise NotImplementedError

    async def delete(self, id: int):
        raise NotImplementedError

    async def search(
        self,
        filters: Optional[dict] = None,
        order_by: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[Location]:
        statement = select(LocationModel)
        if filters:
            for column_name, value in filters.items():
                column = getattr(LocationModel, column_name)
                statement = statement.where(column == value)
        if order_by:
            statement = statement.order_by(order_by)
        if offset:
            statement = statement.offset(offset)
        if limit:
            statement = statement.limit(limit)
        results = await self._session.execute(statement)
        return results
