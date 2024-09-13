from datetime import datetime
from typing import List, Optional
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


class WeatherValues(BaseModel):
    cloudBase: Optional[float] = None
    cloudCeiling: Optional[float] = None
    cloudCover: float
    dewPoint: Optional[float] = None
    evapotranspiration: Optional[float] = None
    freezingRainIntensity: Optional[float] = None
    humidity: float
    iceAccumulation: Optional[float] = None
    iceAccumulationLwe: Optional[float] = None
    precipitationProbability: float
    pressureSurfaceLevel: Optional[float] = None
    rainAccumulation: Optional[float] = None
    rainAccumulationLwe: Optional[float] = None
    rainIntensity: Optional[float] = None
    sleetAccumulation: Optional[float] = None
    sleetAccumulationLwe: Optional[float] = None
    sleetIntensity: Optional[float] = None
    snowAccumulation: Optional[float] = None
    snowAccumulationLwe: Optional[float] = None
    snowDepth: Optional[float] = None
    snowIntensity: Optional[float] = None
    temperature: float
    temperatureApparent: Optional[float] = None
    uvHealthConcern: Optional[float] = None
    uvIndex: Optional[int] = None
    visibility: Optional[float] = None
    weatherCode: Optional[int] = None
    windDirection: float
    windGust: Optional[float] = None
    windSpeed: float


class HourlyWeatherData(BaseModel):
    time: datetime
    values: WeatherValues


class Timelines(BaseModel):
    hourly: List[HourlyWeatherData]


class WeatherDataResponse(BaseModel):
    timelines: Timelines
