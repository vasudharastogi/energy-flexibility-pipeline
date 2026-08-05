import requests
from datetime import datetime, timedelta
import zipfile
from io import BytesIO
from dataclasses import dataclass
import csv

# This script ingests weather from the Deutsche Wetter Dienst (DWD).

# Both id's refernce to Berlin-Brandneburg
RADIATION_STATIONS_ID = '18044'
TEMPERATURE_STATIONS_ID = '00427'
MISSING_VALUE = -999


@dataclass
class WeatherReading:
    timestamp_utc: datetime
    global_radiation_jcm2: float
    air_temperature_celsius: float


def parse_response(response, column: str, cast, weeks: int) -> dict:

    binary_buffer = BytesIO(response.content)
    zf = zipfile.ZipFile(binary_buffer)
    filename = next(name for name in zf.namelist() if 'produkt' in name)

    with zf.open(filename) as f:
        text = f.read().decode('latin-1')

    reader = csv.DictReader(
        text.splitlines(), delimiter=';', skipinitialspace=True)
    data = {}
    past_date = time_period(weeks)

    for row in reader:
        date = row['MESS_DATUM']
        timestamp = datetime(int(date[:4]), int(
            date[4:6]), int(date[6:8]), int(date[8:]))
        if timestamp < past_date:
            continue
        if cast(row[column]) == MISSING_VALUE:
            continue    # to be improved: maybe consider QN-flags or special value
        data[timestamp] = cast(row[column])
    return data


def time_period(weeks):
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    past_date = now - timedelta(weeks=weeks)
    return past_date


def get_global_radiation(stations_id, weeks: int):
    try:
        response = requests.get(
            f'https://opendata.dwd.de/climate_environment/CDC/derived_germany/climate/hourly/duett/radiation_global/recent/stundenwerte_duett_FG_{stations_id}_akt.zip',
            stream=True, timeout=10)
        response.raise_for_status()
        return parse_response(response, 'FG_DUETT', float, weeks)

    except requests.exceptions.RequestException as req_err:
        print(f'Error downloading file: {req_err}')
        return None


def get_air_temperature(stations_id, weeks):
    try:
        response = requests.get(f'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/recent/stundenwerte_TU_{stations_id}_akt.zip',
                                stream=True, timeout=10)
        response.raise_for_status()
        return parse_response(response, 'TT_TU', float, weeks)

    except requests.exceptions.RequestException as req_err:
        print(f'Error downloading file: {req_err}')
        return None


def merge_weather_readings(radiation: dict, temperature: dict) -> list[WeatherReading]:
    if radiation is None or temperature is None:
        return []
    weather_data = []
    for key, value in radiation.items():
        if key not in temperature:
            continue
        weather_data.append(WeatherReading(key, value, temperature[key]))

    return weather_data


if __name__ == "__main__":
    r_data = get_global_radiation(RADIATION_STATIONS_ID, 12)
    temp_data = get_air_temperature(TEMPERATURE_STATIONS_ID, 12)
    data = merge_weather_readings(r_data, temp_data)
