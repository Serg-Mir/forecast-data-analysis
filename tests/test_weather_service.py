from unittest.mock import MagicMock

import pytest
import httpx
from httpx import HTTPStatusError
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.weather_service import fetch_weather_data, store_weather_data
from app.models import WeatherData
from tests.mocks import MOCK_WEATHER_DATA


@pytest.mark.asyncio
async def test_fetch_weather_data_success(monkeypatch):
    async def mock_get(*args, **kwargs):  # pylint: disable=unused-argument
        mock_response = httpx.Response(
            status_code=200, json=MOCK_WEATHER_DATA, request=httpx.Request("GET", "mock_url")
        )
        return mock_response

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    result = await fetch_weather_data(40.7128, -74.0060)
    assert result == MOCK_WEATHER_DATA


@pytest.mark.asyncio
async def test_fetch_weather_data_failure(monkeypatch):
    async def mock_get(*args, **kwargs):  # pylint: disable=unused-argument
        mock_response = httpx.Response(status_code=500, request=httpx.Request("GET", "mock_url"))
        raise HTTPStatusError("Error", request=mock_response.request, response=mock_response)

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    # Ensure the function raises the appropriate HTTPException
    with pytest.raises(HTTPException):
        await fetch_weather_data(40.7128, -74.0060)


def test_store_weather_data():
    db = MagicMock(Session)
    weather_data = MOCK_WEATHER_DATA
    lat, lon = 40.7128, -74.0060

    store_weather_data(db, weather_data, lat, lon)

    assert db.add.call_count == len(weather_data["timelines"]["hourly"])
    assert db.commit.called

    call_args = db.add.call_args_list[0][0][0]
    assert isinstance(call_args, WeatherData)
    assert call_args.latitude == lat
    assert call_args.longitude == lon
    assert call_args.temperature == weather_data["timelines"]["hourly"][0]["values"]["temperature"]
    assert call_args.wind_speed == weather_data["timelines"]["hourly"][0]["values"]["windSpeed"]
    assert (
        call_args.precipitation
        == weather_data["timelines"]["hourly"][0]["values"]["precipitationProbability"]
    )
    assert call_args.humidity == weather_data["timelines"]["hourly"][0]["values"]["humidity"]
    assert call_args.cloud_cover == weather_data["timelines"]["hourly"][0]["values"]["cloudCover"]
