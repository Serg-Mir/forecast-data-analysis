from sqlalchemy import Column, Integer, Float, DateTime
from app.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)
    temperature = Column(Float)
    wind_speed = Column(Float)
    precipitation = Column(Float)
    humidity = Column(Float)
    cloud_cover = Column(Float)
    forecast_time = Column(DateTime)
