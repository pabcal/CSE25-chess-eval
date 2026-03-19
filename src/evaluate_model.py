import csv
import pickle
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# Constants
FEATURE_COLS = ["material", "center", "mobility", "tactical", "doubled", "isolated", "passed", "king_safety"]
DATA_PATH = "data/processed/test_dataset.csv"
MODEL_PATH = "results/model.pkl"
SCALER_PATH = "results/scaler.pkl"

# Similar format to train_model.py
# Load dataset; meta stores fen, move and eval_diff
def load_dataset(csv_path):
    X, y, meta = [], [], []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            X.append([float(row[col]) for col in FEATURE_COLS])
            y.append(int(row["label"]))
            meta.append({"fen": row["fen"], "move": row["move"], "eval_diff": float(row["eval_diff"])})
    return np.array(X), np.array(y), meta

# Loads the model that train_model.py produced
# Runs predict() to get 0/1 predictions
if __name__ == "__main__":
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)

    # Metrics for report
    X, y, meta = load_dataset(DATA_PATH)
    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)

    acc  = accuracy_score(y, y_pred)
    prec = precision_score(y, y_pred)
    rec  = recall_score(y, y_pred)
    cm   = confusion_matrix(y, y_pred)

    print("=== Quantitative Evaluation ===")
    print(f"Accuracy : {acc:.3f}")
    print(f"Precision: {prec:.3f}  (of predicted good moves, how many truly are)")
    print(f"Recall   : {rec:.3f}  (of actual good moves, how many we caught)")
    print(f"\nConfusion matrix (rows=actual, cols=predicted):")
    print(f"          Pred Bad  Pred Good")
    print(f"Act Bad   {cm[0][0]:8d}  {cm[0][1]:9d}")
    print(f"Act Good  {cm[1][0]:8d}  {cm[1][1]:9d}")

    print("\n=== Feature Importance (logistic regression weights) ===")
    for name, coef in sorted(zip(FEATURE_COLS, model.coef_[0]), key=lambda x: abs(x[1]), reverse=True):
        direction = "good" if coef > 0 else "bad"
        print(f"  {name:12s}  {coef:+.4f}  -> higher value pushes prediction toward '{direction}'")

    # Qualitative: show 5 correct and 5 incorrect predictions
    probs = model.predict_proba(X_scaled)[:, 1]
    correct_idx   = [i for i in range(len(y)) if y_pred[i] == y[i]]
    incorrect_idx = [i for i in range(len(y)) if y_pred[i] != y[i]]

    def show_examples(indices, label, n=5):
        print(f"\n--- {label} (showing {min(n, len(indices))}) ---")
        for i in indices[:n]:
            actual = "good" if y[i] == 1 else "bad"
            predicted = "good" if y_pred[i] == 1 else "bad"
            feats = dict(zip(FEATURE_COLS, X[i]))
            print(f"  Move: {meta[i]['move']}  actual={actual}  predicted={predicted}  "
                  f"confidence={probs[i]:.2f}  eval_diff={meta[i]['eval_diff']:+.2f}")
            print(f"    features: { {k: f'{v:+.1f}' for k, v in feats.items()} }")

    show_examples(correct_idx,   "Correct predictions")
    show_examples(incorrect_idx, "Incorrect predictions (errors)")
