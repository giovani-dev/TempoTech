"""
Módulo de injeção de dependência para provedores de dados externos.

Este módulo configura e gerencia a injeção de dependências para provedores
de dados que buscam informações de APIs externas. A injeção de dependência
para `CountryProvider` garante que o provedor correto seja utilizado,
mantendo o código desacoplado e facilitando a troca de provedores,
se necessário.
"""

from typing import Annotated

from fastapi import Depends

from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.providers import coutry_provider

CountryProvider = Annotated[ILocationProvider, Depends(lambda: coutry_provider)]
"""
Type alias que representa a injeção de dependência para o provedor de localização do país.

Quando um endpoint precisa interagir com um provedor de localização externo,
ele pode injetar esta dependência, que fornecerá a instância configurada do
provedor (ex: IBGEProvider).
"""
