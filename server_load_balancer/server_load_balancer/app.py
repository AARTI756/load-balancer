from flask import Flask, render_template, session
from fuzzy_system import get_scaling_decision
import joblib
import numpy as np
import psutil

app = Flask(__name__)
app.secret_key = "secret123"

# Load model
rf = joblib.load("models/random_forest.pkl")
x_cols = np.load("models/x_cols.npy", allow_pickle=True)


# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -------------------------
# REAL TIME DATA
# -------------------------
def get_realtime_data():
    cpu = np.clip(psutil.cpu_percent(interval=0.5), 0, 100)
    mem = np.clip(psutil.virtual_memory().percent, 0, 100)

    return {
        "cpu": float(cpu),
        "idle": float(100 - cpu),
        "load": float(cpu / 100),
        "mem": float(mem)
    }


# -------------------------
# FUTURE PREDICTIONS
# -------------------------
def generate_hourly_predictions(base):
    hours, preds, decisions = [], [], []
    labels = ["LOW", "MEDIUM", "HIGH"]

    for i in range(1, 7):

        trend = i * np.random.uniform(1.5, 3.0)

        cpu = np.clip(base["cpu"] + trend + np.random.uniform(-4, 4), 0, 100)
        mem = np.clip(base["mem"] + trend / 2 + np.random.uniform(-4, 4), 0, 100)

        idle = 100 - cpu
        load = cpu / 100

        X = np.zeros(len(x_cols))

        feature_map = {
            "cpu_total": cpu,
            "cpu_idle": idle,
            "load_min1": load,
            "mem_percent": mem
        }

        for j, col in enumerate(x_cols):
            if col in feature_map:
                X[j] = feature_map[col]

        pred = int(np.clip(rf.predict([X])[0], 0, 2))
        pred_label = labels[pred]

        prob = rf.predict_proba([X])[0]
        prob = prob / np.sum(prob)

        predicted_cpu = (
            prob[0] * 25 +
            prob[1] * 65 +
            prob[2] * 85
        )

        fuzzy = get_scaling_decision(predicted_cpu, cpu)

        hours.append(f"{i}h")
        preds.append(pred_label)
        decisions.append(fuzzy["scaling_decision"])

    return hours, preds, decisions


# -------------------------
# SCALING SIMULATION
# -------------------------
def simulate_scaling(preds):
    servers = 2
    result_servers = []
    actions = []
    cooldown = 0

    for p in preds:

        if p == "HIGH":
            servers += 2
            actions.append("+2 servers")
            cooldown = 1

        elif p == "MEDIUM":
            if cooldown == 0:
                servers += 1
                actions.append("+1 server")
                cooldown = 1
            else:
                actions.append("cooldown")
                cooldown = max(0, cooldown - 1)

        else:
            if cooldown == 0 and servers > 2:
                servers -= 1
                actions.append("-1 server")
                cooldown = 1
            else:
                actions.append("no action")
                cooldown = max(0, cooldown - 1)

        result_servers.append(servers)

    return result_servers, actions


# -------------------------
# PEAK + ALERT
# -------------------------
def get_peak_hour(hours, preds):
    priority = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    idx = max(range(len(preds)), key=lambda i: priority[preds[i]])
    return hours[idx], preds[idx]


def generate_alert(preds, hours):
    if "HIGH" in preds:
        return f"⚠ High load expected at {hours[preds.index('HIGH')]}"
    return "✅ No high load expected"


# -------------------------
# MAIN ROUTE
# -------------------------
@app.route("/predict")
def predict():

    data = get_realtime_data()

    cpu = data["cpu"]
    mem = data["mem"]
    idle = data["idle"]
    load = data["load"]

    X = np.zeros(len(x_cols))

    feature_map = {
        "cpu_total": cpu,
        "cpu_idle": idle,
        "load_min1": load,
        "mem_percent": mem
    }

    for i, col in enumerate(x_cols):
        if col in feature_map:
            X[i] = feature_map[col]

    pred = int(np.clip(rf.predict([X])[0], 0, 2))
    labels = ["LOW", "MEDIUM", "HIGH"]
    pred_label = labels[pred]

    prob = rf.predict_proba([X])[0]
    prob = prob / np.sum(prob)

    predicted_cpu = (
        prob[0] * 25 +
        prob[1] * 65 +
        prob[2] * 85
    )

    fuzzy = get_scaling_decision(predicted_cpu, cpu)

    hours, future_preds, future_decisions = generate_hourly_predictions(data)
    servers, actions = simulate_scaling(future_preds)
    peak_hour, peak_load = get_peak_hour(hours, future_preds)

    # ---------------- CLEAN RESULT ----------------
    result = {
        "cpu": cpu,
        "mem": mem,
        "idle": idle,
        "load": load,

        "prediction": pred_label,
        "decision": fuzzy["scaling_decision"],
        "fuzzy_score": round(fuzzy["scaling_crisp"], 2),

        "prob_low": int(prob[0] * 100),
        "prob_med": int(prob[1] * 100),
        "prob_high": int(prob[2] * 100),

        "hours": hours,
        "future_preds": future_preds,
        "future_decisions": future_decisions,

        "servers": servers,
        "actions": actions,

        "peak_hour": peak_hour,
        "peak_load": peak_load,
        "alert": generate_alert(future_preds, hours)
    }

    # ---------------- HISTORY FIX ----------------
    if "history" not in session:
        session["history"] = []

    session["history"].append({
        "cpu": round(cpu, 2),
        "load": round(load, 3),
        "prediction": pred_label,
        "decision": fuzzy["scaling_decision"]
    })

    session["history"] = session["history"][-15:]  # keep clean
    result["history"] = session["history"]

    return render_template("index.html", result=result)


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)