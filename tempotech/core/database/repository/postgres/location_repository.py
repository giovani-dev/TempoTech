from typing import Optional

from sqlalchemy import Engine, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session

from tempotech.core.database.models.location_model import LocationModel
from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.schemas.location_schema import Coordinates, Location


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

        if offset is not None and limit is not None:
            statement = statement.offset(offset).limit(limit)

        if filters:
            for column_name, value in filters.items():
                column = getattr(LocationModel, column_name)
                statement = statement.where(column == value)

        statement = (
            statement.order_by(LocationModel.city_name)
            if not order_by
            else statement.order_by(order_by)
        )

        results = await self._session.execute(statement)
        locations = results.scalars().all()
        return [
            Location(
                country=item.country,
                state=item.state,
                stateName=item.state_name,
                cityName=item.city_name,
                coordinates=(
                    Coordinates(latitude=item.latitude, longitude=item.longitude)
                    if item.latitude and item.longitude
                    else None
                ),
            )
            for item in locations
        ]
