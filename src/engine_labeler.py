import os
import chess
import chess.engine

THRESHOLD = 0.5
ENGINE_PATH = os.path.join(os.path.dirname(__file__), "..", "stockfish", "stockfish.exe")

def create_engine():
    return chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

def evaluate_with_engine(board, engine):
    info = engine.analyse(board, chess.engine.Limit(depth=4))
    score = info["score"].white()

    if score.is_mate():
        return 1000.0 if score.mate() > 0 else -1000.0

    return score.score() / 100.0

def label_move(board, move, engine):
    mover = board.turn

    eval_before = evaluate_with_engine(board, engine)

    board.push(move)
    eval_after = evaluate_with_engine(board, engine)
    board.pop()

    if mover == chess.WHITE:
        diff = eval_after - eval_before
    else:
        diff = eval_before - eval_after

    if diff < -THRESHOLD:
        return 0, diff  # Bad move
    else:
        return 1, diff  # Decent move
    
