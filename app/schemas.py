from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class Coordinate(BaseModel):
    lat: float = Field(..., example=25.7617)
    lon: float = Field(..., example=-80.1918)


class CoordinateList(BaseModel):
    coordinates: List[Coordinate]


class WeatherDataSchema(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime
    temperature: float
    wind_speed: float
    precipitation: float
    humidity: float
    cloud_cover: float
    forecast_time: datetime

    class Config:
        orm_mode = True
