from sqlmodel import SQLModel, create_engine
from tempotech.core.interfaces.database_repository import IConnectionRepository


class ConnectionRepository(IConnectionRepository[any]):
    def connect(self, host: str, port: str, user: str, pwd: str) -> any:
        engine = create_engine("sqlite:///database.db")
        SQLModel.metadata.create_all(engine)
