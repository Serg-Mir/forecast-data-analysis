from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models, schemas, weather_service

app = FastAPI(title="forecast-data-analysis")

models.Base.metadata.create_all(bind=engine)


@app.post("/fetch_weather/")
async def fetch_weather(coord_list: schemas.CoordinateList):
    results = []
    for coord in coord_list.coordinates:
        weather_data = await weather_service.fetch_weather_data(coord.lat, coord.lon)
        results.append(weather_data)
    return results


@app.post("/store_weather/")
async def store_weather(coord_list: schemas.CoordinateList, db: Session = Depends(get_db)):
    for coord in coord_list.coordinates:
        weather_data = await weather_service.fetch_weather_data(coord.lat, coord.lon)
        weather_service.store_weather_data(db, weather_data, coord.lat, coord.lon)
    return {"message": "Weather data stored successfully"}


@app.get("/get_weather/{lat}/{lon}", response_model=List[schemas.WeatherDataSchema])
def get_weather(lat: float, lon: float, db: Session = Depends(get_db)):
    weather_data = (
        db.query(models.WeatherData)
        .filter(models.WeatherData.latitude == lat, models.WeatherData.longitude == lon)
        .order_by(models.WeatherData.timestamp.desc())
        .limit(24)
        .all()
    )
    if not weather_data:
        raise HTTPException(
            status_code=404, detail="Weather data not found for the given coordinates"
        )
    return weather_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
