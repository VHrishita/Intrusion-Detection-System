# prepare_and_train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

print("[TRAIN] Loading data...")

# ✅ Load your correct dataset
df = pd.read_csv("data/demo_flows.csv", low_memory=False)

# ✅ Clean column names
df.columns = df.columns.str.strip()

# ✅ Make sure Label column exists
if "Label" not in df.columns:
    raise ValueError("⚠️ No 'Label' column found in dataset!")

# ✅ Convert Label to binary (if not already 0/1)
df["Label"] = df["Label"].replace({"BENIGN": 0, "Benign": 0, "Normal": 0})
df["Label"] = df["Label"].apply(lambda x: 1 if str(x).upper() != "0" and str(x).upper() != "BENIGN" else 0)

print(df["Label"].value_counts())

# ✅ Select numeric columns for training
X = df.select_dtypes(include=["number"]).drop(columns=["Label"], errors="ignore")
y = df["Label"]

print(f"[TRAIN] Using {X.shape[1]} features")

# ✅ Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ✅ Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# ✅ Save model
joblib.dump(clf, "model_rf.pkl")
print("✅ Model trained and saved as model_rf.pkl")

# ✅ Evaluate quick accuracy
acc = clf.score(X_test, y_test)
print(f"[TRAIN] Accuracy: {acc:.4f}")
