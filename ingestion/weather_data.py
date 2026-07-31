import requests
import datetime
import zipfile
from io import BytesIO
from io import StringIO
from dataclasses import dataclass
import csv

# This script ingests weather from the Deutsche Wetter Dienst (DWD).

STATIONS_ID = 18044


def get_available_weeks(stations_id):
    try:
        r = requests.get(
            f'https://opendata.dwd.de/climate_environment/CDC/derived_germany/climate/hourly/duett/radiation_global/recent/stundenwerte_duett_FG_{stations_id}_akt.zip',
            stream=True, timeout=10)
        r.raise_for_status()

        # Create a new BytesIO object
        binary_buffer = BytesIO(r.content)
        zf = zipfile.ZipFile(binary_buffer)

        text  = ""
        with zf.open(zf.namelist()[5]) as f:
            text = f.read().decode('latin-1')

        reader = csv.DictReader(text.splitlines(), delimiter=';', skipinitialspace=True)
        for row in reader:
            del row['STATIONS_ID']
            del row['eor']
            print(row)

        '''
        next step: decide how old data I want, 
        convert it to a fucntion, give it weeks as param, then take current date and substract 
        the weeks

        do I need to consider the qn_952 quality flag? 
        can I drop FG_UN_DUETT?
        and if FG_UN_DUETT has a higher value, does that mean FG_DUETT is not that credible?
        '''

    except requests.exceptions.RequestException as req_err:
        print(f'Error downloading file: {req_err}')
        return False


# calls the per-week endpoint, returns a list of daily {timestamp_utc, price_eur_mwh} records
def fetch_week_prices(filter_id, region, resolution, week_timestamp_ms):
    pass


# walks backward through get_available_weeks(), calls fetch_week_prices for each, collects all records
def backfill(filter_id, region, resolution, num_weeks: int):
    pass


# just fetch_week_prices() for the single latest week
def ingest_latest(filter_id, region, resolution):
    pass


if __name__ == "__main__":
    data = get_available_weeks(STATIONS_ID)
    # print(data)
    # print(data.keys())
    # print(data['10865'].keys())
    # print(data['G005'].keys())
   # print(data.items())
    # for value in data['10865']['days']:
    #  print(f'{value}')
