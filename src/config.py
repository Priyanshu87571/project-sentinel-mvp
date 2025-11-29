from pathlib import Path

# Base directory of the project (project-sentinel-mvp)
BASE_DIR = Path(__file__).resolve().parent.parent

# State directory where the agent writes JSON files
STATE_DIR = BASE_DIR / "state"
STATE_DIR.mkdir(exist_ok=True)

METRICS_PATH = STATE_DIR / "latest_metrics.json"
ALERTS_PATH = STATE_DIR / "latest_alerts.json"

# thresholds for simple anomaly detection
AQI_ANOMALY_ZSCORE = 2.0
HOSPITAL_ANOMALY_ZSCORE = 2.0
CITIZEN_REPORT_SPIKE_FACTOR = 1.5  # 50% jump vs recent average

CITY_ZONES = ["North Ward", "South Ward", "East Ward", "West Ward"]

# how often the agent loop runs (seconds)
LOOP_SLEEP_SECONDS = 5
