from sqlmodel import Field, SQLModel


class WeatherLocationModel(SQLModel, table=True):
    __tablename__ = "WeatherLocation"

    weather_id: int = Field(alias="id_Weather")
    location_id: int = Field(alias="id_Location")
