
# read h25 data Werte pro Monat × Tagestyp × Uhrzeit)
# Für jede Stunde in deinem bestehenden Preis-/Wetter-Zeitraum: Monat + Tagestyp bestimmen (drei Kategorien, nicht nur Wochentag/Wochenende: WT, SA, FT — FT enthält auch Feiertage, nicht nur Sonntage — deine Vereinfachung von vorhin entscheiden: Feiertage ignorieren oder holidays-Paket nutzen)
# Die 4 Viertelstundenwerte für diese Stunde aus der Tabelle holen
#  Dynamisierungsfunktion anwenden und zu einem Stundenwert mitteln

import pandas as pd
import datetime
from dataclasses import dataclass

H25_FILEPATH = "/Users/vasudharastogi/Documents/02_Coding/energy-flexibility-pipeline/Kopie_von_Repräsentative_Profile_BDEW_H25_G25_L25_P25_S25_Veröffentlichung.xlsx"
ANNUAL_CONSUMPTION_KWH = 3500


@dataclass
class HouseholdLoadReading:
    timestamp_utc: datetime.datetime
    load_kwh: float


def load_H25_profile(filepath: str) -> pd.DataFrame:
    df = pd.read_excel(filepath, sheet_name='H25', header=None)
    pd.set_option('display.max_columns', None)
    print(df.info())
    #print(df.iloc[4, 5])


def get_day_type(date: datetime.datetime) -> str:
    pass


def get_price_timestamps(conn) -> list[datetime.datetime]:
    pass


def apply_dynamization(x0: float, t: int):
    pass


def get_household_load(timestamp: list[datetime.datetime], profile: pd.DataFrame, annual_consumption_kwh: float) -> list[HouseholdLoadReading]:
    pass


if __name__ == "__main__":
    load_H25_profile(H25_FILEPATH)
