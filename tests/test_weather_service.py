import sqlite3
from contextlib import closing

from database import initialize_db
from weather_service import collect_and_store_weather


def test_collect_and_store_weather(tmp_path):
    database_path = tmp_path / "test_weather.db"
    initialize_db(database_path)

    def fake_fetch_weather(latitude, longitude):
        assert latitude == -8.0476
        assert longitude == -34.8770

        return {
            "time": 0,
            "temperature_2m": 27.5,
            "apparent_temperature": 29.0,
            "relative_humidity_2m": 75,
            "wind_speed_10m": 12.4,
        }

    observation_id = collect_and_store_weather(
        "Recife",
        -8.0476,
        -34.8770,
        database_path,
        fake_fetch_weather,
    )

    with closing(sqlite3.connect(database_path)) as connection:
        row = connection.execute(
            """
            SELECT
                locations.name,
                weather_observations.observed_at,
                weather_observations.temperature_c,
                weather_observations.apparent_temperature_c,
                weather_observations.relative_humidity_pct,
                weather_observations.wind_speed_kmh
            FROM weather_observations
            JOIN locations
                ON locations.id = weather_observations.location_id
            WHERE weather_observations.id = ?
            """,
            (observation_id,),
        ).fetchone()

    assert observation_id == 1
    assert row == (
        "Recife",
        "1970-01-01T00:00:00+00:00",
        27.5,
        29.0,
        75,
        12.4,
    )