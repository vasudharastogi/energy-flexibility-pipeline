import requests
from datetime import datetime, timedelta
import zipfile
from io import BytesIO
from dataclasses import dataclass
import csv

# This script ingests weather from the Deutsche Wetter Dienst (DWD).

STATIONS_ID = 18044


def get_global_radiation(stations_id, weeks: int):
    try:
        r = requests.get(
            f'https://opendata.dwd.de/climate_environment/CDC/derived_germany/climate/hourly/duett/radiation_global/recent/stundenwerte_duett_FG_{stations_id}_akt.zip',
            stream=True, timeout=10)
        r.raise_for_status()

        # Create a new BytesIO object
        binary_buffer = BytesIO(r.content)
        zf = zipfile.ZipFile(binary_buffer)

        text = ""
        with zf.open(zf.namelist()[5]) as f:
            text = f.read().decode('latin-1')

        reader = csv.DictReader(
            text.splitlines(), delimiter=';', skipinitialspace=True)
        for row in reader:
            del row['STATIONS_ID']
            del row['QN_952']
            del row['FG_UN_DUETT']
            del row['eor']
            date = row['MESS_DATUM']
            row['MESS_DATUM'] = datetime(
                int(date[:4]), int(date[4:6]), int(date[6:8]), int(date[8:]))

        # take weeks num and substract it from current date

        now = datetime.now().replace(minute=0, second=0, microsecond=0)

        past_date = now - timedelta(weeks=weeks)
        print(past_date)
        
        '''
        next step: pick out the past date and slice away all the data before that 
        '''

    except requests.exceptions.RequestException as req_err:
        print(f'Error downloading file: {req_err}')
        return False


def get_temperature(stations_id, weeks):
    pass


if __name__ == "__main__":
    data = get_global_radiation(STATIONS_ID, 12)
    # print(data)
    # print(data.keys())
    # print(data['10865'].keys())
    # print(data['G005'].keys())
   # print(data.items())
    # for value in data['10865']['days']:
    #  print(f'{value}')
