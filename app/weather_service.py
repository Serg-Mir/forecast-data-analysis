from datetime import datetime
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.models import WeatherData
from app.schemas import WeatherDataResponse


async def fetch_weather_data(lat: float, lon: float) -> WeatherDataResponse:
    params = {
        "location": f"{lat},{lon}",
        "apikey": settings.TOMORROW_IO_API_KEY,
        "fields": [
            "temperature",
            "windSpeed",
            "precipitationProbability",
            "humidity",
            "cloudCover",
        ],
        "units": "metric",
        "timesteps": f"{settings.FORECAST_HOURS}h",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(settings.TOMORROW_IO_API_URL, params=params)
            response.raise_for_status()
            return WeatherDataResponse(**response.json())
        except httpx.HTTPStatusError as error:
            raise HTTPException(
                status_code=error.response.status_code, detail=str(error)
            ) from error


def store_weather_data(db: Session, weather_data: WeatherDataResponse, lat: float, lon: float):
    forecast_time = datetime.utcnow()
    for entry in weather_data.timelines.hourly:
        timestamp = datetime.fromisoformat(str(entry.time).rstrip("Z"))
        db_entry = WeatherData(
            latitude=lat,
            longitude=lon,
            timestamp=timestamp,
            temperature=entry.values.temperature,
            wind_speed=entry.values.windSpeed,
            precipitation=entry.values.precipitationProbability,
            humidity=entry.values.humidity,
            cloud_cover=entry.values.cloudCover,
            forecast_time=forecast_time,
        )
        db.add(db_entry)
    db.commit()
