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

def center_control(board):
    """
    Computes the number of attacks on center squares (d4, e4, d5, e5)
    for both sides and returns the difference.
    """
    center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
    
    white_attacks = 0
    black_attacks = 0

    for square in center_squares:
        white_attacks += len(board.attackers(chess.WHITE, square))
        black_attacks += len(board.attackers(chess.BLACK, square))

    return white_attacks - black_attacks