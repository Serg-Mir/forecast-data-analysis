from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    DATABASE_URL: str
    TOMORROW_IO_API_KEY: str
    TOMORROW_IO_API_URL: HttpUrl = "https://api.tomorrow.io/v4/weather/forecast"
    FORECAST_HOURS: int = 1  # Fetch 24 hours of forecast data

    class Config:
        env_file = ".env"


settings = Settings()
