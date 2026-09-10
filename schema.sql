CREATE TABLE IF NOT EXISTS locations(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CHECK (length(trim(name)) > 0),
    CHECK (latitude BETWEEN -90 AND 90),
    CHECK (longitude BETWEEN -180 AND 180),
    UNIQUE (latitude, longitude)
);

CREATE TABLE IF NOT EXISTS weather_observations (
    id INTEGER PRIMARY KEY,
    location_id INTEGER NOT NULL,
    observed_at TEXT NOT NULL,
    temperature_c REAL NOT NULL,
    apparent_temperature_c REAL NOT NULL,
    relative_humidity_pct INTEGER NOT NULL,
    wind_speed_kmh REAL NOT NULL,
    collected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CHECK (relative_humidity_pct BETWEEN 0 AND 100),
    CHECK (wind_speed_kmh >= 0),

    UNIQUE (location_id, observed_at),

    FOREIGN KEY (location_id)
        REFERENCES locations (id)
        ON DELETE RESTRICT
);
