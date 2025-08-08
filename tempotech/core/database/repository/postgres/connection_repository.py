from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

from tempotech.core.interfaces.database_repository import IConnectionRepository


class ConnectionRepository(IConnectionRepository[Engine]):

    @staticmethod
    def connect(host: str, port: str, user: str, pwd: str) -> Engine:
        engine = create_engine(
            "sqlite:///database.db"
        )  # TODO: Adicionar string de coneção com o Postgresql
        SQLModel.metadata.create_all(engine)
        return engine
