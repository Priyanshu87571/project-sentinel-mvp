import time
from datetime import datetime
from .ingestion import fetch_unified_snapshot
from .detection import SlidingWindowStore, detect_anomalies
from .utils import save_metrics, save_alerts
from .config import LOOP_SLEEP_SECONDS

def run_agent():
    print("[Agent] Starting Project Sentinel agent loop...")
    history = SlidingWindowStore(max_len=500)

    while True:
        # 1) Perceive
        latest = fetch_unified_snapshot()
        print(f"[Agent] Fetched batch with {len(latest)} rows at {datetime.utcnow().isoformat()}")
        history.add_batch(latest)
        history_df = history.to_dataframe()

        # 2) Reason
        alerts = detect_anomalies(history_df, latest)
        print(f"[Agent] Alerts this cycle: {len(alerts)}")

        # 3) Act
        save_metrics(latest)
        save_alerts(alerts if alerts else [])

        print("[Agent] State written to JSON. Sleeping...\n")
        time.sleep(LOOP_SLEEP_SECONDS)

if __name__ == "__main__":
    run_agent()
