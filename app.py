from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import joblib
from utils import load_flows_csv

app = Flask(__name__)

model = joblib.load("model_rf.pkl")

_, features = load_flows_csv("data/demo_flows.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = ""
    form_values = {}  

    if request.method == "POST":
        try:
            
            form_values = {f: request.form[f] for f in features}
            input_data = {f: [float(request.form[f])] for f in features}

            
            df = pd.DataFrame(input_data)
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            df.fillna(0, inplace=True)
            df = df.clip(upper=1e6, lower=-1e6)

            pred = model.predict(df)[0]
            prediction = " 🚨 Attack" if pred else "✅ Normal"

        except Exception as e:
            
            prediction = f"Error: {e}"

    return render_template("index.html", prediction=prediction, form=form_values)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
