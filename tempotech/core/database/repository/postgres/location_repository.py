from typing import Optional

from sqlalchemy import Engine, select
from sqlmodel import Session

from tempotech.core.database.models.location_model import LocationModel
from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.schemas.location_schema import Location


class LocationRepository(IDefaultRepository[Location]):

    def __init__(self, engine: Engine):
        self._engine = engine

    def create(self, data: Location):
        model = LocationModel(
            city_name=data.city_name,
            state_name=data.state_name,
            state=data.state,
            country=data.country,
            latitude=data.coordinates.latitude,
            longitude=data.coordinates.longitude,
        )
        with Session(self._engine) as session:
            session.add(model)
            session.commit()

    def update(self, data: Location, id: int):
        raise NotImplementedError

    def delete(self, id: int):
        raise NotImplementedError

    def search(
        self,
        filters: Optional[dict] = None,
        order_by: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[Location]:
        statement = select(LocationModel)
        if filters:
            statement = statement.where(**filters)
        if order_by:
            statement = statement.order_by(order_by)
        if offset:
            statement = statement.offset(offset)
        if limit:
            statement = statement.limit(limit)
        with Session(self._engine) as session:
            results = session.exec(statement)
        return results
