# ⚡ Predictive Server Load Balancer

### Machine Learning + Fuzzy Logic (Soft Computing) + Real-Time Flask Dashboard

**Mini Project – 3rd Year Computer Engineering**

---

## 📌 Project Overview

Modern computing systems face **unpredictable server load spikes**, which can lead to performance degradation or system crashes.

This project builds an **intelligent hybrid load balancing system** that combines:

* 🤖 Machine Learning (Random Forest) → Predicts system load
* 🧠 Fuzzy Logic (Soft Computing) → Makes intelligent scaling decisions
* 🌐 Flask Web Dashboard → Real-time visualization
* 📊 System Monitoring → Uses actual CPU & memory data

The system ensures **proactive scaling decisions instead of reactive responses**.

---

## 🚀 Key Features

### 🧠 ML + Soft Computing Core

* ✔ Random Forest-based load prediction (LOW / MEDIUM / HIGH)
* ✔ Logistic Regression (comparison model)
* ✔ Fuzzy Logic decision system (NO SCALE / SCALE SLIGHTLY / SCALE HIGH)
* ✔ Lag-based time-series feature engineering

### ⚙️ Real-Time System

* ✔ Live CPU usage tracking (psutil)
* ✔ Memory usage monitoring
* ✔ Load average calculation
* ✔ Session-based history tracking

### 🌐 Web Dashboard (NEW ADDITION)

* ✔ Flask-based UI (app.py)
* ✔ Auto-refresh live dashboard
* ✔ Interactive charts (Chart.js)
* ✔ CPU trend visualization
* ✔ Prediction confidence visualization
* ✔ Server scaling simulation
* ✔ Smart alerts + peak detection

---

## 📁 Project Structure

```text
Predictive-Server-Load-Balancer/
│
├── app.py                         # Flask backend (LIVE UI system)
├── fuzzy_system.py               # Fuzzy Logic engine (skfuzzy)
│
├── models/
│   ├── random_forest.pkl         # Trained ML model
│   ├── logistic_regression.pkl   # Comparison model
│   ├── scaler.pkl                # MinMaxScaler
│   └── x_cols.npy                # Feature columns
│
├── data/
│   ├── generate_data.py          # Synthetic dataset generator
│   └── final-complete-data-set.csv
│
├── templates/
│   ├── index.html               # Main dashboard UI
│   └── home.html                # Landing page
│
├── static/
│   ├── script.js                # Frontend logic + charts
│   └── style.css                # Glassmorphism UI styling
│
├── results/                     # ML analysis outputs
│   ├── confusion_matrices.png
│   ├── cpu_trend.png
│   ├── feature_importance.png
│   ├── fuzzy_output_trend.png
│   └── batch_results.csv
│
└── README.md
```

---

## ⚙️ System Architecture

```text
             Real-Time CPU + Memory
                       │
                       ▼
              Flask Backend (app.py)
                       │
        ┌──────────────┴──────────────┐
        │                             │
   Machine Learning            System Metrics
   (Random Forest)             (psutil)
        │                             │
        └──────────────┬──────────────┘
                       ▼
              Fuzzy Logic System
                       │
           Intelligent Scaling Decision
                       │
                       ▼
             Web Dashboard (UI)
```

---

## 🧠 Machine Learning Module

### 🔹 Models Used

* Random Forest Classifier (Primary)
* Logistic Regression (Comparison)

### 🔹 Input Features

* cpu_total
* cpu_idle
* load_min1
* mem_percent
* network activity (dataset-based)
* lag features (t-1, t-2, t-3)

### 🔹 Output Classes

```text
0 → LOW
1 → MEDIUM
2 → HIGH
```

### 🔹 Why Random Forest?

* Handles nonlinear system behavior
* Works well with noisy system data
* Provides high accuracy
* Supports feature importance analysis

---

## 🧠 Fuzzy Logic (Soft Computing)

### 🔹 Inputs

* Predicted Load (from ML)
* Current CPU usage

### 🔹 Output

* NO SCALE
* SCALE SLIGHTLY
* SCALE HIGH

### 🔹 Membership Functions

* LOW → trapezoidal
* MEDIUM → triangular
* HIGH → trapezoidal

### 🔹 Rule Base (9 Rules)

| Rule | Predicted | CPU    | Action         |
| ---- | --------- | ------ | -------------- |
| R1   | HIGH      | HIGH   | SCALE HIGH     |
| R2   | HIGH      | MEDIUM | SCALE HIGH     |
| R3   | MEDIUM    | HIGH   | SCALE SLIGHTLY |
| R4   | MEDIUM    | MEDIUM | SCALE SLIGHTLY |
| R5   | MEDIUM    | LOW    | SCALE SLIGHTLY |
| R6   | LOW       | LOW    | NO SCALE       |
| R7   | LOW       | MEDIUM | NO SCALE       |
| R8   | LOW       | HIGH   | SCALE SLIGHTLY |
| R9   | HIGH      | LOW    | SCALE SLIGHTLY |

### 🔹 Defuzzification

* Method: Centroid (Center of Gravity)
* Output mapping:

```text
0 – 3.5   → NO SCALE
3.5 – 6.5 → SCALE SLIGHTLY
6.5 – 10  → SCALE HIGH
```

---

## 🌐 Web Dashboard (NEW FEATURE)

### Run UI:

```bash
python app.py
```

### Open:

```
http://127.0.0.1:5000/predict
```

### Dashboard Features:

* 🔥 Live CPU & Memory monitoring
* 🤖 ML prediction display
* 🧠 Fuzzy scaling decision
* 📊 Confidence bar chart
* 📈 CPU trend graph
* ⏳ Future load simulation
* 🖥️ Server scaling simulation
* 🚨 Smart alerts
* 🔥 Peak load detection
* 🧾 Prediction history table

---

## 🔮 Future Prediction System

* Generates next **6-hour load simulation**
* Uses:

  * CPU trend drift
  * Random noise injection
  * Incremental load modeling

👉 Used for:

* Forecast visualization
* Scaling simulation
* Peak detection

---

## ⚙️ Installation

```bash
pip install flask numpy pandas psutil scikit-learn joblib scikit-fuzzy matplotlib
```

---

## ▶ Run Project

### 1. Start Flask Server

```bash
python app.py
```

### 2. Open in Browser

```
http://127.0.0.1:5000/predict
```

---

## 📊 Example Output

```text
CPU Usage: 57.3%
Memory Usage: 84.8%

Prediction: MEDIUM
Decision: SCALE SLIGHTLY

Confidence:
LOW → 30%
MED → 51%
HIGH → 19%
```

---

## 💡 Why This Project is Strong

✔ Real-world cloud computing problem
✔ Hybrid AI system (ML + Fuzzy Logic)
✔ Real-time system integration
✔ Interactive web dashboard
✔ Industry-relevant architecture

---

## ⚠ Limitations

* Future prediction is simulated (not real-time cloud data)
* Model trained on controlled dataset
* No actual cloud deployment (yet)

---

## 🚀 Future Enhancements

* Kubernetes auto-scaling integration
* Real cloud metrics (AWS / Azure / Prometheus)
* LSTM-based time-series prediction
* Multi-server load balancing
* Anomaly detection (DDoS / cryptojacking)

---

## 🛠 Tech Stack

| Layer          | Technology    |
| -------------- | ------------- |
| Backend        | Flask         |
| ML             | Scikit-learn  |
| Soft Computing | scikit-fuzzy  |
| Frontend       | HTML, CSS, JS |
| Charts         | Chart.js      |
| Monitoring     | psutil        |

---

## 🏁 Final Summary

This project demonstrates a **hybrid intelligent load balancing system** that:

* Predicts server load using ML
* Makes decisions using fuzzy logic
* Monitors real system metrics
* Displays results in a live dashboard

👉 A complete **AI + Soft Computing + Real-Time System project**

---

