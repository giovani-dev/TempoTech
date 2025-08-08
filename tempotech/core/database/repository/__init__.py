from tempotech.core import config
from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.schemas.location_schema import Location

# location_repository: IDefaultRepository[Location]

if config.DB_ENGINE == "POSTGRESQL":
    from tempotech.core.database.repository.postgres.connection_repository import (
        ConnectionRepository,
    )
    from tempotech.core.database.repository.postgres.location_repository import (
        LocationRepository,
    )

    # _connection = ConnectionRepository.connect(
    #     host=config.DB_HOST,
    #     port=config.DB_PORT,
    #     user=config.DB_USER,
    #     pwd=config.DB_PWD,
    #     db_name=config.DB_NAME,
    # )
    # location_repository = LocationRepository(engine=_connection)
