import csv
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Constants
FEATURE_COLS = ["material", "center", "mobility", "tactical", "doubled", "isolated", "passed", "king_safety"]
DATA_PATH = "data/processed/test_dataset.csv"
MODEL_PATH = "results/model.pkl"
SCALER_PATH = "results/scaler.pkl"

# Pulls 7 features into X and the labels into y
def load_dataset(csv_path):
    X, y = [], []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            X.append([float(row[col]) for col in FEATURE_COLS])
            y.append(int(row["label"]))
    return np.array(X), np.array(y)

# Train/Test split 80-20
if __name__ == "__main__":
    X, y = load_dataset(DATA_PATH)
    print(f"Loaded {len(X)} samples  (good={sum(y)}, bad={len(y)-sum(y)})")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scales/standardizes each feature 
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    model.fit(X_train_scaled, y_train)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    print(f"Model saved to {MODEL_PATH}")
    print(f"Train accuracy: {model.score(X_train_scaled, y_train):.3f}")
    print(f"Test  accuracy: {model.score(X_test_scaled,  y_test):.3f}")

    print("\nFeature weights (larger = more influential):")
    for name, coef in sorted(zip(FEATURE_COLS, model.coef_[0]), key=lambda x: abs(x[1]), reverse=True):
        print(f"  {name:12s}  {coef:+.4f}")
