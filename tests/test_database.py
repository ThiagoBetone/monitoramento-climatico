import sqlite3
import pytest
from contextlib import closing


from database import (
    create_location,
    create_weather_observation,
    get_or_create_location,
    initialize_db,
    save_weather_observation,
)


def test_create_location(tmp_path):
    database_path = tmp_path / "test_weather.db"

    initialize_db(database_path)

    location_id = create_location(
        "Recife",
        -8.0476,
        -34.8770,
        database_path,
    )

    with closing(sqlite3.connect(database_path)) as connection:
        row = connection.execute(
            """
            SELECT id, name, latitude, longitude
            FROM locations
            WHERE id = ?
            """,
            (location_id,),
        ).fetchone()

    assert location_id == 1
    assert row == (1, "Recife", -8.0476, -34.8770)


def test_create_location_rejects_duplicate(tmp_path):
    database_path = tmp_path / "test_weather.db"
    initialize_db(database_path)

    create_location("São Paulo", -23.5505, -46.6333, database_path)

    with pytest.raises(sqlite3.IntegrityError):
        create_location(
            "Manaus",
            -23.5505,
            -46.6333,
            database_path,
        )

    with closing(sqlite3.connect(database_path)) as connection:
        total = connection.execute(
            "SELECT COUNT(*) FROM locations"
        ).fetchone()[0]

    assert total == 1

@pytest.mark.parametrize(
    ("latitude", "longitude"),
    [
        (90.1, 0),
        (-90.1, 0),
        (0, 180.1),
        (0, -180.1),
    ],
)


def test_create_location_rejects_invalid_coordinates(
    tmp_path,
    latitude,
    longitude,
):
    database_path = tmp_path / "test_weather.db"
    initialize_db(database_path)

    with pytest.raises(sqlite3.IntegrityError):
        create_location(
            "Local inválido",
            latitude,
            longitude,
            database_path,
        )

def test_create_weather_observation(tmp_path):
    database_path = tmp_path / "test_weather.db"
    initialize_db(database_path)

    location_id = create_location(
        "Recife",
        -8.0476,
        -34.8770,
        database_path,
    )

    observation_id = create_weather_observation(
        location_id,
        "2026-09-08T18:00:00+00:00",
        27.5,
        29.0,
        75,
        12.4,
        database_path,
    )

    with closing(sqlite3.connect(database_path)) as connection:
        row = connection.execute(
            """
            SELECT
                location_id,
                observed_at,
                temperature_c,
                apparent_temperature_c,
                relative_humidity_pct,
                wind_speed_kmh
            FROM weather_observations
            WHERE id = ?
            """,
            (observation_id,),
        ).fetchone()

    assert observation_id == 1
    assert row == (
        location_id,
        "2026-09-08T18:00:00+00:00",
        27.5,
        29.0,
        75,
        12.4,
    )

def test_rejects_observation_for_unknown_location(tmp_path):
    database_path = tmp_path / "test_weather.db"
    initialize_db(database_path)

    with pytest.raises(sqlite3.IntegrityError):
        create_weather_observation(
            999,
            "2026-09-08T18:00:00+00:00",
            27.5,
            29.0,
            75,
            12.4,
            database_path,
        )

    with closing(sqlite3.connect(database_path)) as connection:
        total = connection.execute(
            "SELECT COUNT(*) FROM weather_observations"
        ).fetchone()[0]

    assert total == 0

def test_rejects_humidity_above_100(tmp_path):
    database_path = tmp_path / "test_weather.db"
    initialize_db(database_path)

    location_id = create_location(
        "Recife",
        -8.0476,
        -34.8770,
        database_path,
    )

    with pytest.raises(sqlite3.IntegrityError):
        create_weather_observation(
            location_id,
            "2026-09-08T18:00:00+00:00",
            27.5,
            29.0,
            101,
            12.4,
            database_path,
        )


def test_get_or_create_location_reuses_existing_location(tmp_path):
    database_path = tmp_path / "test_weather.db"
    initialize_db(database_path)

    first_id = get_or_create_location(
        "São Paulo",
        -23.5505,
        -46.6333,
        database_path,
    )

    second_id = get_or_create_location(
        "São Paulo - SP",
        -23.5505,
        -46.6333,
        database_path,
    )

    with closing(sqlite3.connect(database_path)) as connection:
        rows = connection.execute(
            "SELECT id, name FROM locations"
        ).fetchall()

    assert second_id == first_id
    assert rows == [(first_id, "São Paulo - SP")]


def test_save_weather_observation_updates_existing_observation(tmp_path):
    database_path = tmp_path / "test_weather.db"
    initialize_db(database_path)

    location_id = create_location(
        "Recife",
        -8.0476,
        -34.8770,
        database_path,
    )

    first_id = save_weather_observation(
        location_id,
        "2026-09-08T18:00:00+00:00",
        27.5,
        29.0,
        75,
        12.4,
        database_path,
    )

    second_id = save_weather_observation(
        location_id,
        "2026-09-08T18:00:00+00:00",
        28.0,
        30.0,
        72,
        14.0,
        database_path,
    )

    with closing(sqlite3.connect(database_path)) as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                temperature_c,
                apparent_temperature_c,
                relative_humidity_pct,
                wind_speed_kmh
            FROM weather_observations
            """
        ).fetchall()

    assert second_id == first_id
    assert rows == [
        (first_id, 28.0, 30.0, 72, 14.0)
    ]
