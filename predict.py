# predict.py
import pandas as pd
import joblib

print("[PREDICT] Loading model and data...")

model = joblib.load("model_rf.pkl")
df = pd.read_csv("data/demo_flows.csv", low_memory=False)

df.columns = df.columns.str.strip()
df["Label"] = df["Label"].replace({"BENIGN": 0, "Benign": 0, "Normal": 0})
df["Label"] = df["Label"].apply(lambda x: 1 if str(x).upper() != "0" and str(x).upper() != "BENIGN" else 0)

# Show label distribution
print("Label counts:")
print(df["Label"].value_counts())

X = df.select_dtypes(include=["number"]).drop(columns=["Label"], errors="ignore")

# Predict one random row
sample = X.sample(1, random_state=42)
prediction = model.predict(sample)[0]

print("\nSample row:")
print(sample)
print("\nPredicted:", "🚨 Attack" if prediction == 1 else "✅ Normal")
