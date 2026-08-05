CREATE TABLE raw_radiation (
    timestamp_utc TIMESTAMPTZ NOT NULL,
    station_name TEXT NOT NULL,
    solar_radiation_j_cm2 NUMERIC NOT NULL,
    PRIMARY KEY(timestamp_utc, station_name)
);

CREATE TABLE raw_temperature (
    timestamp_utc TIMESTAMPTZ NOT NULL,
    station_name TEXT NOT NULL,
    air_temperature_c NUMERIC NOT NULL,
    PRIMARY KEY(timestamp_utc, station_name)
);

CREATE TABLE energy_prices (
    timestamp_utc TIMESTAMPTZ NOT NULL,
    price_eur_mwh NUMERIC NOT NULL,
    PRIMARY KEY(timestamp_utc)
);