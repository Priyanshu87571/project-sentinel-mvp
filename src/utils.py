import json
from pathlib import Path
from typing import Any, List
from .config import METRICS_PATH, ALERTS_PATH

def write_json(path: Path, data: Any):
    path.write_text(json.dumps(data, indent=2))

def read_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        # if file is half-written / corrupted, start fresh
        return default

def save_metrics(latest_df):
    """
    Append latest batch to metrics history (max 200 rows).
    This lets the dashboard draw time-series charts.
    """
    new_rows = latest_df.to_dict(orient="records")
    try:
        existing = json.loads(METRICS_PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []
    combined = (existing + new_rows)[-200:]
    write_json(METRICS_PATH, combined)

def save_alerts(alerts: List[dict]):
    """Overwrite alerts list with the most recent run."""
    write_json(ALERTS_PATH, alerts)
