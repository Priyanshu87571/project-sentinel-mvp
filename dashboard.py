import streamlit as st
import pandas as pd
import threading

from src.config import METRICS_PATH, ALERTS_PATH
from src.utils import read_json
from src.agent import run_agent


# ---------------------------------------------------
# Start Agent in Background Thread (for Deploy)
# ---------------------------------------------------
if "agent_started" not in st.session_state:
    st.session_state["agent_started"] = False

def start_agent_background():
    if not st.session_state["agent_started"]:
        thread = threading.Thread(target=run_agent, daemon=True)
        thread.start()
        st.session_state["agent_started"] = True

start_agent_background()
# ---------------------------------------------------


# Streamlit Setup
st.set_page_config(
    page_title="Project Sentinel - Public Health Guardian",
    layout="wide"
)

st.title("🛰️ Project Sentinel – Public Health Intelligence Dashboard")
st.caption("From reaction to foresight: proactive intelligence for urban health.")


# ---------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------
col1, col2 = st.columns([2, 1])


# --------------------------
# LEFT COLUMN – METRICS
# --------------------------
with col1:
    st.subheader("Live City Health Snapshot")

    metrics_data = read_json(METRICS_PATH, default=[])

    if metrics_data:
        df = pd.DataFrame(metrics_data)

        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            st.markdown("**Latest observations (per zone):**")
            st.dataframe(df.tail(16))

            st.markdown("**Air Quality Index (AQI) over time:**")
            aqi_pivot = df.pivot(index="timestamp", columns="zone", values="aqi")
            st.line_chart(aqi_pivot)

            st.markdown("**Hospital admissions over time:**")
            adm_pivot = df.pivot(index="timestamp", columns="zone", values="admissions")
            st.line_chart(adm_pivot)

        else:
            st.info("Metrics file is empty. Waiting for agent...")

    else:
        st.info("Waiting for agent to generate metrics...")


# --------------------------
# RIGHT COLUMN – ALERTS
# --------------------------
with col2:
    st.subheader("Active Alerts")

    alerts_data = read_json(ALERTS_PATH, default=[])

    if not alerts_data:
        st.success("No active anomalies detected. City health looks stable. ✅")
    else:
        for alert in alerts_data:
            with st.container():
                st.markdown(f"**Zone:** {alert['zone']}")
                st.markdown(f"**Title:** {alert['title']}")
                confidence_pct = int(alert["confidence"] * 100)
                st.markdown(f"**Confidence:** {confidence_pct}%")

                st.markdown("**Reasons:**")
                for r in alert["reasons"]:
                    st.write(f"- {r}")

                st.markdown("**Recommended Action:**")
                st.write(alert["recommended_action"])


# --------------------------
# SIDEBAR – SYSTEM STATUS
# --------------------------
st.sidebar.subheader("System Status")
st.sidebar.write("Agent is running in the background inside this app. ✅")
st.sidebar.write("Dashboard updates automatically every few seconds.")
