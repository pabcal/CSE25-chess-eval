import chess.pgn
import json
from feature_extractor import material_balance

def parse_pgn(file_path):
    positions = []   # List containing all the positions
    plies_per_game = []  # List containing plies per game
    max_games = 1000  # For testing purposes

    with open(file_path, "r", encoding="utf-8", errors="ignore") as pgn:
        game_index = 1  # Keep track of the game number

        while game_index <= max_games:
            game = chess.pgn.read_game(pgn)

            if game is None:
                break

            board = game.board()  # Set up starting position
            ply = 0  # A ply is one move made by a player (either white or black); full move consists of two plies

            for move in game.mainline_moves():
                fen = board.fen()  # FEN is a string format that represents a position
                ply += 1
                positions.append({
                    "game_index": game_index,
                    "ply": ply,
                    "fen": fen,
                    "move": move.uci()
                })

                board.push(move)   # Simulate game
            game_index += 1
            plies_per_game.append(ply)

    return positions, plies_per_game

if __name__ == "__main__":
    positions, plies_per_game = parse_pgn("data/raw/eliteNov2025Games.pgn")

    total_games = len(plies_per_game)
    total_positions = len(positions)
    avg_plies = sum(plies_per_game) / total_games if total_games > 0 else 0

    # Print metrics
    print("Dataset Summary")
    print(f"Total games parsed: {total_games}")
    print(f"Total positions extracted: {total_positions}")
    print(f"Average plies per game: {avg_plies}")

    # Print position info & material balance
    print("\nFirst 10 examples:")
    for position in positions[:10]:
        print(f"{json.dumps(position, indent=4)}")
        board = chess.Board(position["fen"])
        print("Material balance:", material_balance(board))
        print()

    