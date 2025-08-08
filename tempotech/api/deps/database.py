from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine

from tempotech.core.database.repository import LocationRepository
from tempotech.core.database.repository.postgres.connection_repository import (
    ConnectionRepository,
)
from tempotech.core.interfaces.database_repository import (
    IConnectionRepository,
    IDefaultRepository,
)
from tempotech.core.schemas.location_schema import Location

DbSession = Annotated[
    IConnectionRepository[Engine], Depends(ConnectionRepository.connect)
]


def get_location_repository(session: DbSession) -> IDefaultRepository[Location]:
    return LocationRepository(session=session)


LocationDbRepository = Annotated[
    IDefaultRepository[Location], Depends(get_location_repository)
]
