import chess.pgn
import json

"""def parse_pgn(file_path, max_games = None):
    positions = []   # List containing all the positions
    plies_per_game = []  # List containing plies per game

    with open(file_path, "r", encoding="utf-8", errors="ignore") as pgn:
        game_index = 1  # Keep track of the game number

        while max_games is None or game_index <= max_games:
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

    return positions, plies_per_game"""

def iter_positions(file_path, max_games = None):

    with open(file_path, "r", encoding="utf-8", errors="ignore") as pgn:
        game_index = 1  # Keep track of the game number

        while max_games is None or game_index <= max_games:
            game = chess.pgn.read_game(pgn)

            if game is None:
                break

            board = game.board()  # Set up starting position
            ply = 0  # A ply is one move made by a player (either white or black); full move consists of two plies

            for move in game.mainline_moves():
                fen = board.fen()  # FEN is a string format that represents a position
                ply += 1
                yield {
                    "game_index": game_index,
                    "ply": ply,
                    "fen": fen,
                    "move": move.uci()
                }

                board.push(move)   # Simulate game
            game_index += 1