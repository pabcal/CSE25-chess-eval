import chess

# Dictionary storing pieces abbreviations and values
piece_values = {
    "p": 1,
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k": 0
}

def material_balance(board):
    """
    Function that computes the total material count
    for both sides and returns the difference
    """
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

    #  List that stores all the center squares
    center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
    
    white_attacks = 0
    black_attacks = 0

    for square in center_squares:
        # board.attackers(Color, square) calculates number of color attackers on a square
        white_attacks += len(board.attackers(chess.WHITE, square))
        black_attacks += len(board.attackers(chess.BLACK, square))

    return white_attacks - black_attacks

def mobility(board):
    """
    Function that returns the difference in
    number of legal moves between White and Black
    """
    original_turn = board.turn   # Stores the current turn (White or Black)
    
    # Manually switches the turn to count legal moves
    board.turn = chess.WHITE
    white_moves = board.legal_moves.count()

    board.turn = chess.BLACK
    black_moves = board.legal_moves.count()
    
    board.turn = original_turn  # Resets the original turn/position
    
    return white_moves - black_moves
