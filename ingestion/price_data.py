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


# calls index_{resolution}.json, returns the list of weekly start timestamps
def get_available_weeks(filter_id, region, resolution) -> list[int]:
    try:
        r = requests.get(
            f'https://www.smard.de/app/chart_data/{filter_id}/{region}/index_{resolution}.json', timeout=10)
        r.raise_for_status()

        data = r.json()
        latest_week = data['timestamps'][-1]
    except requests.exceptions.HTTPError as err_h:
        print("HTTP Error")
        print(err_h)
        return []
    except requests.exceptions.ConnectionError as con_err:
        print("Connection error.")
        return []

    print(f'Data of total {len(data['timestamps'])} weeks available.')
    print(f'Most recent week {convert_ms_to_date(latest_week)}')
    return data['timestamps']


# calls the per-week endpoint, returns a list of daily {timestamp_utc, price_eur_mwh} records
def fetch_week_prices(filter_id, region, resolution, week_timestamp_ms) -> list[PriceReading]:
    try:
        res = requests.get(
            f'https://www.smard.de/app/chart_data/{filter_id}/{region}/{filter_id}_{region}_{resolution}_{week_timestamp_ms}.json',
            timeout=10)
        latest_prices = []
        for value in res.json()['series']:
            if value[1] is not None:
                latest_prices.append(PriceReading(
                    convert_ms_to_date(value[0]), value[1]))
    except requests.exceptions.HTTPError as err_h:
        print("HTTP Error")
        print(err_h)
        return []
    except requests.exceptions.ConnectionError as con_err:
        print("Connection error.")
        return []

    return latest_prices


# walks backward through get_available_weeks(), calls fetch_week_prices for each, collects all records
def backfill(filter_id, region, resolution, num_weeks: int) -> list[PriceReading]:
    all_weeks = get_available_weeks(filter_id, region, resolution)
    all_readings = []
    if len(all_weeks) > num_weeks:
        weeks = all_weeks[-num_weeks:]
        for week_ts in weeks:
            all_readings.extend(fetch_week_prices(
                filter_id, region, resolution, week_ts))
    else:
        print(
            f'Requested number of weeks: {num_weeks} exceeds available data of {len(all_weeks)}.')
    return all_readings


# just fetch_week_prices() for the single latest week
def ingest_latest(filter_id, region, resolution) -> list[PriceReading]:
    latest_week_ts = get_available_weeks(filter_id, region, resolution)[-1]
    return fetch_week_prices(filter_id, region, resolution, latest_week_ts)


if __name__ == "__main__":
    print(ingest_latest(FILTER_ID, REGION, RESOLUTION))
