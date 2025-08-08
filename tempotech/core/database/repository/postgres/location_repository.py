"""
Módulo de repositório para interações com dados de localização no PostgreSQL.

Esta classe implementa a lógica de persistência e recuperação de dados
de localização, como estados e cidades, utilizando o SQLModel e uma sessão
assíncrona do SQLAlchemy.
"""

from typing import Optional

from sqlalchemy import Engine, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session

from tempotech.core.database.models.location_model import LocationModel
from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.schemas.location_schema import Coordinates, Location


class LocationRepository(IDefaultRepository[Location]):
    """
    Repositório responsável por operações CRUD de localização no banco de dados.

    Implementa a interface `IDefaultRepository` para operações como criar
    e buscar dados de localização.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa o repositório com uma sessão de banco de dados.

        Args:
            session (AsyncSession): A sessão assíncrona do banco de dados.
        """
        self._session = session

    async def create(self, data: Location):
        """
        Cria um novo registro de localização no banco de dados.

        Converte um objeto `Location` em um `LocationModel` e o adiciona
        à sessão para ser persistido.

        Args:
            data (Location): O objeto de localização a ser criado.
        """
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
        """
        Atualiza um registro de localização existente.

        Esta função ainda não foi implementada.
        """
        raise NotImplementedError

    async def delete(self, id: int):
        """
        Exclui um registro de localização.

        Esta função ainda não foi implementada.
        """
        raise NotImplementedError

    async def search(
        self,
        filters: Optional[dict] = None,
        order_by: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[Location]:
        """
        Busca registros de localização no banco de dados com filtros e paginação.

        Args:
            filters (Optional[dict]): Dicionário de filtros para a busca.
            order_by (Optional[str]): Coluna para ordenação dos resultados.
            offset (Optional[int]): Deslocamento para paginação.
            limit (Optional[int]): Limite de resultados por página.

        Returns:
            list[Location]: Uma lista de objetos Location encontrados.
        """
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
