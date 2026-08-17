from ingestion.price_data import ingest_latest
from ingestion.weather_data import get_air_temperature, get_global_radiation
from persistence import save_prices, save_weather
from db import get_connection

# Prices
FILTER_ID = 4169
REGION = 'DE'
RESOLUTION = 'hour'

# Weather
RADIATION_STATIONS_ID = '18044'     # Berlin-Brandenburg
TEMPERATURE_STATIONS_ID = '00427'   # Berlin-Brandenburg


# fetch and ingest data
prices = ingest_latest(FILTER_ID, REGION, RESOLUTION)
radiation = get_global_radiation(RADIATION_STATIONS_ID, 12)
temperature = get_air_temperature(TEMPERATURE_STATIONS_ID, 12)

# persit
conn = get_connection()

try: 
    save_prices(conn, prices)
    save_weather(conn, TEMPERATURE_STATIONS_ID,
                RADIATION_STATIONS_ID, temperature, radiation)
    conn.commit()

except: conn.rollback()
finally: conn.close()
