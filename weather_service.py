from datetime import datetime, timezone
from weather_api import buscar_clima

from database import (
    DATABASE_PATH,
    save_weather_observation,
    get_or_create_location,
)


def collect_and_store_weather(
    name,
    latitude,
    longitude,
    database_path=DATABASE_PATH,
    fetch_weather=buscar_clima,
):
    weather = fetch_weather(latitude, longitude)

    observed_at = datetime.fromtimestamp(
        weather["time"],
        tz=timezone.utc,
    ).isoformat()

    location_id = get_or_create_location(
        name,
        latitude,
        longitude,
        database_path,
    )

    observation_id = save_weather_observation(
        location_id,
        observed_at,
        weather["temperature_2m"],
        weather["apparent_temperature"],
        weather["relative_humidity_2m"],
        weather["wind_speed_10m"],
        database_path,
    )

    return observation_id