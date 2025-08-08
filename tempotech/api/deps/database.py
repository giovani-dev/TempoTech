from typing import Annotated

from tempotech.core.database.repository import location_repository
from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.schemas.location_schema import Location

LocationRepository = Annotated[
    IDefaultRepository[Location], lambda: location_repository
]
