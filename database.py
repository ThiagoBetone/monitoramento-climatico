import sqlite3
from contextlib import closing
from pathlib import Path




BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "weather.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

def get_or_create_location(
    name,
    latitude,
    longitude,
    database_path=DATABASE_PATH,
):
    sql = """
        INSERT INTO locations (name, latitude, longitude)
        VALUES (?, ?, ?)
        ON CONFLICT (latitude, longitude)
        DO UPDATE SET name = excluded.name
        RETURNING id
    """

    with closing(sqlite3.connect(database_path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        with connection:
            row = connection.execute(
                sql,
                (name, latitude, longitude),
            ).fetchone()

        return row[0]


def initialize_db(database_path=DATABASE_PATH):
    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with closing(sqlite3.connect(database_path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(schema)


def create_location(name, latitude, longitude, database_path=DATABASE_PATH):
    sql = """
        INSERT INTO locations (name, latitude, longitude)
        VALUES (?, ?, ?)
    """

    with closing(sqlite3.connect(database_path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        with connection:
            cursor = connection.execute(
                sql,
                (name, latitude, longitude),
            )

        return cursor.lastrowid


def create_weather_observation(
        location_id,
        observed_at,
        temperature_c,
        apparent_temperature_c,
        relative_humidity_pct,
        wind_speed_kmh,
        database_path=DATABASE_PATH,
):
    sql = """
        INSERT INTO weather_observations (
        location_id,
        observed_at,
        temperature_c,
        apparent_temperature_c,
        relative_humidity_pct,
        wind_speed_kmh
        ) VALUES (?, ?, ?, ?, ?, ?)
    """

    values = (
        location_id,
        observed_at,
        temperature_c,
        apparent_temperature_c,
        relative_humidity_pct,
        wind_speed_kmh
    )

    with closing(sqlite3.connect(database_path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        with connection:
            cursor = connection.execute(sql, values)

        return cursor.lastrowid


def save_weather_observation(
    location_id,
    observed_at,
    temperature_c,
    apparent_temperature_c,
    relative_humidity_pct,
    wind_speed_kmh,
    database_path=DATABASE_PATH,
):
    sql = """
          INSERT INTO weather_observations (location_id, 
                                            observed_at, 
                                            temperature_c, 
                                            apparent_temperature_c, 
                                            relative_humidity_pct, 
                                            wind_speed_kmh)
          VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT (location_id, observed_at)
        DO 
          UPDATE SET
              temperature_c = excluded.temperature_c, 
              apparent_temperature_c = excluded.apparent_temperature_c, 
              relative_humidity_pct = excluded.relative_humidity_pct, 
              wind_speed_kmh = excluded.wind_speed_kmh 
              RETURNING id 
          """
    values = (
        location_id,
        observed_at,
        temperature_c,
        apparent_temperature_c,
        relative_humidity_pct,
        wind_speed_kmh,
    )

    with closing(sqlite3.connect(database_path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        with connection:
            row = connection.execute(sql, values).fetchone()

        return row[0]


def list_weather_observations(location_id, database_path=DATABASE_PATH):
    sql = """
        SELECT observed_at, temperature_c
        FROM weather_observations
        WHERE location_id = ?
        ORDER BY observed_at
    """

    with closing(sqlite3.connect(database_path)) as connection:
        return connection.execute(sql, (location_id,)).fetchall()


def list_dashboard_data(database_path=DATABASE_PATH):
    sql = """
        SELECT
            l.name AS city,
            w.observed_at,
            w.temperature_c,
            w.apparent_temperature_c,
            w.relative_humidity_pct,
            w.wind_speed_kmh
        FROM weather_observations AS w
        JOIN locations AS l ON l.id = w.location_id
        ORDER BY w.observed_at
    """

    with closing(sqlite3.connect(database_path)) as connection:
        return connection.execute(sql).fetchall()

if __name__ == "__main__":
    initialize_db()
    print(f"Banco criado em: {DATABASE_PATH}")