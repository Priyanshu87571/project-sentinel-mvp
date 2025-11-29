# Project Sentinel – Public Health Intelligence System

## 👥 Team
- Priyanshu Raj
- Arham Kelkar

## 🚀 Overview
Project Sentinel is a real-time public health intelligence platform that transforms cities from *reactive* to *proactive*.  
Using an autonomous AI agent, it continuously:

1. **Perceives** – streams multi-source city health data  
2. **Reasons** – detects anomalies and emerging risks  
3. **Acts** – generates early alerts with recommended responses  

This MumbaiHack MVP demonstrates a working Perceive → Reason → Act loop with live visualization.

---

## 🏗️ Architecture
- **Backend AI agent** (Python)
  - short-term sliding window store
  - anomaly detection (AQI spikes, hospital surges)
- **State layer**
  - `latest_metrics.json`
  - `latest_alerts.json`
- **Frontend**
  - Streamlit dashboard with real-time updates

---

## 📊 Features
- Live AQI, hospital admissions & citizen report simulation  
- Real-time anomaly detection  
- Auto-generated alerts (zone, confidence, reasons, recommended action)  
- Interactive dashboard  

---

## ▶️ How to Run

### 1. Start the AI Agent
```bash
python -m src.agent
ARCHITECTURE DIAGRAM
                 ┌──────────────────────────┐
                 │   Simulated Data Sources │
                 │  (AQI, Hospitals, Reports)│
                 └───────────────┬──────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │  Agent Core (Python Loop)│
                    │ Perceive → Reason → Act  │
                    └───────────────┬──────────┘
                                    │
              ┌─────────────────────┴───────────────────────┐
              │                                             │
              ▼                                             ▼
   ┌──────────────────────┐                 ┌────────────────────────┐
   │ Sliding Window Store │                 │ Anomaly Detection      │
   │ (Short-term history) │                 │ (Z-score, trend spikes)│
   └──────────────┬──────┘                 └──────────────┬─────────┘
                  │                                        │
                  ▼                                        ▼
         ┌────────────────┐                        ┌──────────────────┐
         │ latest_metrics │                        │ latest_alerts    │
         │   (JSON file)  │                        │   (JSON file)    │
         └────────┬───────┘                        └────────┬─────────┘
                  │                                        │
                  └────────────────────┬────────────────────┘
                                       ▼
                          ┌────────────────────────────┐
                          │  Streamlit Dashboard (UI)   │
                          │ Live charts + Alerts + UX   │
                          └────────────────────────────┘
