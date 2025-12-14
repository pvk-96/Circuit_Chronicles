import fastf1
import pandas as pd


def clean_laps(laps):
    laps = laps.copy()

    # Only keep laps with complete valid timing
    laps = laps[
        laps["LapTime"].notna() &
        laps["Sector1Time"].notna() &
        laps["Sector2Time"].notna() &
        laps["Sector3Time"].notna()
    ]

    # Remove out laps (Lap starts from pit)
    laps = laps[laps["PitOutTime"].isna()]

    # Remove in laps (Lap ends into pit)
    laps = laps[laps["PitInTime"].isna()]

    # Remove garbage laps (over 200s)
    laps = laps[laps["LapTime"].dt.total_seconds() < 200]

    return laps


def load_session(year, gp, session_type):
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    return session


def get_lap_data(session):
    return session.laps


def get_telemetry_for_lap(lap):
    return lap.get_telemetry()

