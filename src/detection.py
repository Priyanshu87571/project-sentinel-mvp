import pandas as pd
from .config import (
    AQI_ANOMALY_ZSCORE,
    HOSPITAL_ANOMALY_ZSCORE,
    CITIZEN_REPORT_SPIKE_FACTOR,
)

class SlidingWindowStore:
    """Keeps last N observations for quick stats."""
    def __init__(self, max_len=50):
        self.max_len = max_len
        self.rows = []

    def add_batch(self, df: pd.DataFrame):
        for _, row in df.iterrows():
            self.rows.append(row.to_dict())
        if len(self.rows) > self.max_len:
            self.rows = self.rows[-self.max_len:]

    def to_dataframe(self) -> pd.DataFrame:
        if not self.rows:
            return pd.DataFrame(columns=["timestamp", "zone", "aqi", "admissions", "reports"])
        return pd.DataFrame(self.rows)

def compute_zscore(series: pd.Series, value: float):
    """Return z-score of 'value' vs 'series'."""
    if len(series) < 5:
        # too little history, treat as normal
        return 0.0
    mean = series.mean()
    std = series.std(ddof=0) or 1e-6
    return (value - mean) / std

def recommend_action(zone: str, aqi: float, admissions: int, reports: int) -> str:
    """Very simple rule-based recommendation generator."""
    if aqi > 120 and admissions > 15:
        return (
            f"Recommend dispatching a mobile respiratory check-up camp to {zone} "
            f"and issuing an air quality awareness advisory."
        )
    elif admissions > 20:
        return (
            f"Recommend deploying a mobile testing unit to {zone} "
            f"and increasing staff at nearby clinics."
        )
    elif reports > 15:
        return (
            f"Recommend a targeted public health awareness campaign in {zone} "
            f"via SMS and local channels."
        )
    else:
        return (
            f"Increase monitoring in {zone} for the next few hours and prepare "
            f"a contingency testing plan."
        )

def detect_anomalies(history_df: pd.DataFrame, latest_df: pd.DataFrame):
    """
    history_df: all previous rows (for stats)
    latest_df: current time-step snapshot
    Returns: list of alert dicts
    """
    alerts = []
    if history_df.empty:
        return alerts

    for _, row in latest_df.iterrows():
        zone = row["zone"]
        ts = row["timestamp"]
        aqi = row["aqi"]
        adm = row["admissions"]
        rep = row["reports"]

        zone_hist = history_df[history_df["zone"] == zone]

        aqi_z = compute_zscore(zone_hist["aqi"], aqi)
        adm_z = compute_zscore(zone_hist["admissions"], adm)

        if len(zone_hist) >= 5:
            recent_reports_mean = zone_hist["reports"].tail(10).mean()
        else:
            recent_reports_mean = zone_hist["reports"].mean() if len(zone_hist) > 0 else 0

        report_factor = (rep / recent_reports_mean) if recent_reports_mean > 0 else 1

        reasons = []

        if abs(aqi_z) >= AQI_ANOMALY_ZSCORE and aqi > zone_hist["aqi"].mean():
            reasons.append(f"Unusual AQI level (z={aqi_z:.1f})")

        if abs(adm_z) >= HOSPITAL_ANOMALY_ZSCORE and adm > zone_hist["admissions"].mean():
            reasons.append(f"Unusual hospital admissions (z={adm_z:.1f})")

        if report_factor >= CITIZEN_REPORT_SPIKE_FACTOR and rep > 0:
            reasons.append(f"Citizen reports spike ({report_factor:.1f}x recent)")

        if reasons:
            confidence = min(0.95, 0.5 + 0.1 * len(reasons))
            alerts.append({
                "timestamp": ts,
                "zone": zone,
                "title": "Potential local health issue detected",
                "reasons": reasons,
                "confidence": round(confidence, 2),
                "recommended_action": recommend_action(zone, aqi, adm, rep)
            })
    return alerts
