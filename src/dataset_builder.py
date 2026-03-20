import chess
import csv
from pgn_parser import iter_positions
from feature_extractor import extract_move_features
from engine_labeler import create_engine, label_move
from collections import Counter

counts = Counter()

with open("data/processed/test_dataset.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        counts[row["label"]] += 1

print(counts)

def build_dataset(pgn_path, output_csv, max_games=10):
    engine = create_engine()

    try:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = None

            for pos in iter_positions(pgn_path, max_games=max_games):
                board = chess.Board(pos["fen"])
                move = chess.Move.from_uci(pos["move"])

                features = extract_move_features(board, move)
                label, diff = label_move(board, move, engine)

                if label is None:
                    continue

                row = {
                    "game_index": pos["game_index"],
                    "ply": pos["ply"],
                    "fen": pos["fen"],
                    "move": pos["move"],
                    **features,
                    "eval_diff": diff, 
                    "label": label
                }

                if writer is None:
                    writer = csv.DictWriter(f, fieldnames=row.keys())
                    writer.writeheader()

                writer.writerow(row)

    finally:
        engine.quit()

if __name__ == "__main__":
    build_dataset(
        "data/raw/eliteNov2025Games.pgn",
        "data/processed/test_dataset.csv",
        max_games=1000
    )