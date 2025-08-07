from sqlmodel import Field, SQLModel


class WeatherLocationModel(SQLModel, table=True):
    weather_id: int = Field(alias="id_Weather")
    location_id: int = Field(alias="id_Location")
