import requests
import datetime
from dataclasses import dataclass

# This script deals with the price ingestion.

FILTER_ID = 4169
REGION = 'DE'
RESOLUTION = 'hour'


@dataclass
class PriceReading:
    timestamp_utc: datetime.datetime
    price_eur_mwh: float


def convert_ms_to_date(ms):
    dt = datetime.datetime.fromtimestamp(ms / 1000.0, tz=datetime.timezone.utc)
    return dt


# calls index_{resolution}.json, returns the list of week-start timestamps
 # quarterhour: gaps are 168h apart -> 1 week, each entry is the start timestamp of one week-long chunk
def get_available_weeks(filter_id, region, resolution):
    r = requests.get(
        f'https://www.smard.de/app/chart_data/{filter_id}/{region}/index_{resolution}.json', timeout=10)
    
    data = r.json()
    latest_week = data['timestamps'][-1]

    print(f'Most recent week {convert_ms_to_date(latest_week)}')
    return data['timestamps']


# calls the per-week endpoint, returns a list of {timestamp_utc, price_eur_mwh} records
def fetch_week_prices(filter_id, region, resolution, week_timestamp_ms):
    res = requests.get(
        f'https://www.smard.de/app/chart_data/{filter_id}/{region}/{filter_id}_{region}_{resolution}_{week_timestamp_ms}.json',
        timeout=10)

    latest_prices = []
    for value in res.json()['series']:
        if value[1] is not None:
            latest_prices.append(PriceReading(
                convert_ms_to_date(value[0]), value[1]))

    return latest_prices

# walks backward through get_available_weeks(), calls fetch_week_prices for each, collects all records
def backfill(filter_id, region, resolution, num_weeks: int) -> list[PriceReading]:
    weeks = get_available_weeks(filter_id, region, resolution)[-num_weeks]
    all_readings = []
    for week_ts in weeks:
        pass


def ingest_latest(filter_id, region, resolution) -> list[dict]:
    # just fetch_week_prices() for the single latest week
    ...


# __name__ == "__main__":
weekly_data = get_available_weeks(4169, 'DE', 'hour')
latest_week = weekly_data[-1]
fetch_week_prices(4169, 'DE', 'hour', latest_week)
