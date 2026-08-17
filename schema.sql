CREATE TABLE IF NOT EXISTS raw_radiation (
    timestamp_utc TIMESTAMPTZ NOT NULL,
    station_id TEXT NOT NULL,
    solar_radiation_j_cm2 NUMERIC NOT NULL,
    PRIMARY KEY(timestamp_utc, station_id)
);

CREATE TABLE IF NOT EXISTS raw_temperature (
    timestamp_utc TIMESTAMPTZ NOT NULL,
    station_id TEXT NOT NULL,
    air_temperature_c NUMERIC NOT NULL,
    PRIMARY KEY(timestamp_utc, station_id)
);

CREATE TABLE IF NOT EXISTS energy_prices (
    timestamp_utc TIMESTAMPTZ NOT NULL,
    price_eur_mwh NUMERIC NOT NULL,
    PRIMARY KEY(timestamp_utc)
);