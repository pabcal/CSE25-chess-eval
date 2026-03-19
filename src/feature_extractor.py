import chess

piece_values = {
    "p": 1,
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k": 0
}

def material_balance(board):
    white = 0
    black = 0

    for piece in board.piece_map().values():
        value = piece_values[piece.symbol().lower()]

        if piece.color:
            white += value
        
        else:
            black += value

    return white - black


# Function that returns the difference in number of legal moves between White and Black
def mobility(board):

    original_turn = board.turn   # Stores the current turn (White or Black)
    
    # Manually switches the turn to count legal moves
    board.turn = chess.WHITE
    white_moves = board.legal_moves.count()

    board.turn = chess.BLACK
    black_moves = board.legal_moves.count()
    
    board.turn = original_turn  # Resets the original turn/position
    
    return white_moves - black_moves