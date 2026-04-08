from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load model
rf = joblib.load("models/random_forest.pkl")
x_cols = np.load("models/x_cols.npy", allow_pickle=True)

# 🔥 Fuzzy Logic
def fuzzy_decision(cpu, pred):
    if pred == 2 or cpu > 80:
        return "SCALE HIGH"
    elif pred == 1 or cpu > 50:
        return "SCALE SLIGHTLY"
    else:
        return "NO SCALE"

# 🏠 HOME PAGE
@app.route("/")
def home():
    return render_template("home.html")

# 🤖 PREDICTION PAGE
@app.route("/predict", methods=["GET", "POST"])
def predict():
    result = None

    if request.method == "POST":
        try:
            cpu = float(request.form["cpu"])
            idle = float(request.form["idle"])
            load = float(request.form["load"])
            mem = float(request.form["mem"])

            if not (0 <= cpu <= 100 and 0 <= idle <= 100 and 0 <= mem <= 100 and 0 <= load <= 10):
                raise ValueError

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
                elif "lag" in col:
                    base = col.split("_lag")[0]
                    if base in feature_map:
                        noise = np.random.uniform(-5, 5)
                        X[i] = max(0, min(100, feature_map[base] + noise))

            # ML
            model_pred = int(rf.predict([X])[0])
            prob = rf.predict_proba([X])[0] * 100

            # Hybrid logic
            if cpu > 80 or load > 4:
                pred = 2
            elif cpu < 30 and mem < 40:
                pred = 0
            else:
                pred = model_pred

            prob[pred] += 20
            prob = np.clip(prob, 0, 100)

            labels = ["LOW", "MEDIUM", "HIGH"]
            decision = fuzzy_decision(cpu, pred)

            result = {
                "prediction": labels[pred],
                "prob_low": int(prob[0]),
                "prob_med": int(prob[1]),
                "prob_high": int(prob[2]),
                "decision": decision
            }

        except Exception as e:
            print("ERROR:", e)
            result = {
                "prediction": "ERROR",
                "prob_low": 0,
                "prob_med": 0,
                "prob_high": 0,
                "decision": "Invalid Input"
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)