import numpy as np
import pandas as pd
from datetime import datetime
from .config import CITY_ZONES

np.random.seed(42)

def simulate_air_quality(timestamp: str):
    """Simulate AQI per zone, sharing the same timestamp."""
    records = []
    for zone in CITY_ZONES:
        base_aqi = 70 if zone != "North Ward" else 90  # North Ward slightly worse
        aqi = np.random.normal(base_aqi, 10)
        records.append({
            "timestamp": timestamp,
            "zone": zone,
            "aqi": max(0, round(aqi, 1))
        })
    return pd.DataFrame(records)

def simulate_hospital_admissions(timestamp: str):
    """Simulate hospital admissions per zone, sharing the same timestamp."""
    records = []
    for zone in CITY_ZONES:
        base = 12 if zone != "North Ward" else 18
        admissions = np.random.poisson(base)
        records.append({
            "timestamp": timestamp,
            "zone": zone,
            "admissions": int(admissions)
        })
    return pd.DataFrame(records)

def simulate_citizen_reports(timestamp: str):
    """Simulate citizen complaints/symptoms per zone, sharing the same timestamp."""
    records = []
    for zone in CITY_ZONES:
        base = 5 if zone != "North Ward" else 9
        reports = np.random.poisson(base)
        records.append({
            "timestamp": timestamp,
            "zone": zone,
            "reports": int(reports)
        })
    return pd.DataFrame(records)

def fetch_unified_snapshot():
    """
    Returns one unified dataframe for this time step:
    columns: timestamp, zone, aqi, admissions, reports
    """
    # 🔑 one common timestamp for all sources
    ts = datetime.utcnow().isoformat()

    air = simulate_air_quality(ts)
    hosp = simulate_hospital_admissions(ts)
    rep = simulate_citizen_reports(ts)

    # now timestamp & zone match across all, so merge works
    df = air.merge(hosp, on=["timestamp", "zone"])
    df = df.merge(rep, on=["timestamp", "zone"])

    return df
