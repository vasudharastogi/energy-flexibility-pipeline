
# read h25 data Werte pro Monat × Tagestyp × Uhrzeit
# Für jede Stunde in deinem bestehenden Preis-/Wetter-Zeitraum: Monat + Tagestyp bestimmen (drei Kategorien, nicht nur Wochentag/Wochenende: WT, SA, FT — FT enthält auch Feiertage, nicht nur Sonntage — deine Vereinfachung von vorhin entscheiden: Feiertage ignorieren oder holidays-Paket nutzen)
# Die 4 Viertelstundenwerte für diese Stunde aus der Tabelle holen
#  Dynamisierungsfunktion anwenden und zu einem Stundenwert mitteln

import pandas as pd
import datetime
import holidays
from datetime import date
from dataclasses import dataclass

H25_FILEPATH = "../include/Kopie_von_Repräsentative_Profile_BDEW_H25_G25_L25_P25_S25_Veröffentlichung.xlsx"
ANNUAL_CONSUMPTION_KWH = 3500
BERLIN_HOLIDAYS = holidays.country_holidays("DE", subdiv="BE")


@dataclass
class HouseholdLoadReading:
    timestamp_utc: datetime.datetime
    load_kwh: float

# reads and modifies the household load profile header 
def load_H25_profile(filepath: str) -> pd.DataFrame:
    raw_data = pd.read_excel(filepath, sheet_name='H25', header=None)

    months_li = [x.month for x in raw_data.loc[2, 2:]]
    days_li = list(raw_data.loc[3, 2:])

    # building column labels 
    midx = pd.MultiIndex.from_arrays([months_li, days_li])

    profile = raw_data.loc[4:, 2:]
    profile.columns = midx
    profile = profile.reset_index(drop=True).astype(float)
    return profile

# Returns the BDEW day type (WT/SA/FT) for a Berlin local time. Sundays and public holidays count as FT.
def get_day_type(local_time: datetime.datetime) -> str:
    
    weekday = local_time.weekday()
    if local_time in BERLIN_HOLIDAYS or weekday == 6:
        return 'FT'
    if weekday == 5:
        return 'SA'
    return 'WT'
    


def get_price_timestamps(conn) -> list[datetime.datetime]:
    # query only for timestamp_utc which have weather and price data

    with conn.cursor() as cur:
        cur.execute('SELECT e.timestamp_utc FROM energy_prices AS e' 
        ' INNER JOIN raw_radiation AS r ON r.timestamp_utc = e.timestamp_utc' 
        ' ORDER BY e.timestamp_utc')
        data = cur.fetchall()

    timestamps = [item[0] for item in data]
    return timestamps


def apply_dynamization(x0: float, t: int):
    pass


def get_household_load(timestamp: list[datetime.datetime], profile: pd.DataFrame, annual_consumption_kwh: float) -> list[HouseholdLoadReading]:

    # take timestamps, get which day is weekday, weekend and holdiday
    # do i need to convert timezones?
    # lookup the right value for timestamp from profile dataframe and call the apply_dynamization function using that
    pass


if __name__ == "__main__":
    load_H25_profile(H25_FILEPATH)
    print(get_day_type(datetime.datetime(2026, 5, 25, 16, 0, tzinfo=datetime.timezone.utc)))

