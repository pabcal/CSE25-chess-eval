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


def mobility(board):
    white_moves = board.legal_moves.count()
    
    board.turn = False
    black_moves = board.legal_moves.count()
    board.turn = True
    
    return white_moves - black_moves