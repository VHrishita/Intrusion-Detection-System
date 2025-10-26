import pandas as pd

def load_flows_csv(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()  # remove extra spaces

    # Features to use for training
    features = [
        'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
        'Total Length of Fwd Packets', 'Total Length of Bwd Packets',
        'Fwd Packet Length Max', 'Fwd Packet Length Min',
        'Fwd Packet Length Mean', 'Bwd Packet Length Mean',
        'Flow Packets/s', 'Flow IAT Mean'
    ]

    # keep only columns that exist in your csv
    features = [f for f in features if f in df.columns]

    if 'Label' not in df.columns:
        raise KeyError("Column 'Label' not found — check your dataset label column!")

    print(f"[utils] Loaded data with {len(df)} rows and {len(features)} usable features.")
    return df, features
