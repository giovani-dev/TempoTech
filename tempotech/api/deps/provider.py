from typing import Annotated

from fastapi import Depends

from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.providers import coutry_provider

CountryProvider = Annotated[ILocationProvider, Depends(lambda: coutry_provider)]
