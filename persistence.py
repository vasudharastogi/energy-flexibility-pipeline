from db import get_connection
from ingestion.price_data import PriceReading
from psycopg2.extras import execute_values


def save_prices(conn, price_readings: list[PriceReading]):

    readings_tup = tuple([(x.timestamp_utc, x.price_eur_mwh)
                         for x in price_readings])

    with conn.cursor() as cur:
        execute_values(
            cur, "INSERT INTO energy_prices (timestamp_utc, price_eur_mwh) VALUES %s ON CONFLICT (timestamp_utc) DO NOTHING", readings_tup)


def save_weather(conn, temperture_station_id, radiation_station_id, temperature_readings, radiation_readings):
    temperature_tup = [(key, temperture_station_id, val)
                       for key, val in temperature_readings.items()]
    radiation_tup = [(key, radiation_station_id, val)
                     for key, val in radiation_readings.items()]

    with conn.cursor() as cur:
        execute_values(
            cur, "INSERT INTO raw_temperature (timestamp_utc, station_id, air_temperature_c) VALUES %s ON CONFLICT (timestamp_utc, station_id) DO NOTHING",
            temperature_tup)
        execute_values(
            cur, "INSERT INTO raw_radiation (timestamp_utc, station_id, solar_radiation_j_cm2) VALUES %s ON CONFLICT (timestamp_utc, station_id) DO NOTHING",
            radiation_tup)
