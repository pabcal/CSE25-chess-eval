import chess

# Dictionary storing pieces abbreviations and values
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def material_balance(board):
    """
    Function that computes the total material count
    for both sides and returns the difference
    """
    white = 0
    black = 0

    for piece in board.piece_map().values():
        value = PIECE_VALUES[piece.piece_type]

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
    Returns White legal moves - Black legal moves.
    """
    original_turn = board.turn

    try:
        board.turn = chess.WHITE
        white_moves = board.legal_moves.count()

        board.turn = chess.BLACK
        black_moves = board.legal_moves.count()
    finally:
        board.turn = original_turn

    return white_moves - black_moves

def piece_value_at(board, square):
    """
    Helper function for finding the value of a piece on a square
    """

    piece = board.piece_at(square)
    if piece is None:
        return 0
    return PIECE_VALUES[piece.piece_type]

def cheapest_attacker_value(board: chess.Board, color: chess.Color, square: chess.Square):
    attackers = board.attackers(color, square)
    if not attackers:
        return None
    return min(piece_value_at(board, attacker_sq) for attacker_sq in attackers)

def cheapest_defender_value(board: chess.Board, color: chess.Color, square: chess.Square):
    defenders = board.attackers(color, square)
    if not defenders:
        return None
    return min(piece_value_at(board, defender_sq) for defender_sq in defenders)

def tactical_pressure(board: chess.Board) -> float:
    """
    The function evaluates the total attacking/tactical pressure on the board
    If a piece is attacked:
    1. Hanging/Undefended piece
    2. Attacking piece vs attacked piece
    3. Attacking piece vs defender
    Returns a score relative to the difference in piece values (material) in those scenarios 

    Positive -> Black has more tactically vulnerable material -> Good for White
    Negative -> White has more tactically vulnerable material -> Good for Black
    """

    white_squares = (
        board.pieces(chess.PAWN, chess.WHITE)
        | board.pieces(chess.KNIGHT, chess.WHITE)
        | board.pieces(chess.BISHOP, chess.WHITE)
        | board.pieces(chess.ROOK, chess.WHITE)
        | board.pieces(chess.QUEEN, chess.WHITE)
    )

    black_squares = (
        board.pieces(chess.PAWN, chess.BLACK)
        | board.pieces(chess.KNIGHT, chess.BLACK)
        | board.pieces(chess.BISHOP, chess.BLACK)
        | board.pieces(chess.ROOK, chess.BLACK)
        | board.pieces(chess.QUEEN, chess.BLACK)
    )

    def square_pressure(square, color):
        target_value = piece_value_at(board, square)   # Calls helper function
        enemy = not color  # Sets the opposite color as comparison

        attacker_val = cheapest_attacker_value(board, enemy, square)
        defender_val = cheapest_defender_value(board, color, square)

        if attacker_val is None:
            return 0.0

        # 1. Hanging piece is attacked and undefended
        if defender_val is None:
            return float(target_value)

        score = 0.0

        # 2. Less valuable attacker threatening more valuable piece
        if attacker_val < target_value:
            score += target_value - attacker_val

        # 3. Inefficient defense: valuable defender vs less valuable attacker
        if defender_val > attacker_val:
            # Using a more expensive defender is slightly punished
            score += 0.5 * (defender_val - attacker_val)

        return min(score, float(target_value))

    white_pressure = sum(square_pressure(sq, chess.WHITE) for sq in white_squares)
    black_pressure = sum(square_pressure(sq, chess.BLACK) for sq in black_squares)

    return black_pressure - white_pressure

def doubled_pawns(board):
    """
    Returns the number of doubled pawns in the positions
    Positive -> Black has more, good for White
    Negative-> White has more, good for Black
    """
    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    black_pawns = board.pieces(chess.PAWN, chess.BLACK)

    def count_doubled(pawns_bb):
        count = 0
        files = [0]*8

        for sq in pawns_bb: 
            file = chess.square_file(sq)
            files[file]+=1

        for f in files: 
            if f > 1: 
                count+=(f-1)  # Substract one because two pawns doubled count as one
        return count

    white_doubled = count_doubled(white_pawns)
    black_doubled = count_doubled(black_pawns)
    return black_doubled - white_doubled

def isolated_pawns(board): 
    """
    Returns number of isolated pawns
    Positive -> Black has more, good for White
    Negative -> White has more, good for Black
    """
    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    black_pawns = board.pieces(chess.PAWN, chess.BLACK)

    white_files = set(chess.square_file(sq) for sq in white_pawns)
    black_files = set(chess.square_file(sq) for sq in black_pawns)

    def count_isolated(pawns_bb, own_files): 
        count = 0
        for sq in pawns_bb: 
            file = chess.square_file(sq)

            neighbor_files = []
            if file > 0: 
                neighbor_files.append(file-1)
            if file < 7: 
                neighbor_files.append(file+1)

            if not any(f in own_files for f in neighbor_files):
                count += 1

        return count

    white_isolated = count_isolated(white_pawns, white_files)
    black_isolated = count_isolated(black_pawns, black_files)
    return black_isolated - white_isolated

def passed_pawns(board):
    """
    Returns number of passed pawns
    Postive -> White has more, good for White
    Negative -> Black has more, good for Black
    """
    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    black_pawns = board.pieces(chess.PAWN, chess.BLACK)

    def is_white_passed(sq):
        """
        Evaluates if a White pawn is a passed pawn
        """
        file = chess.square_file(sq)
        rank = chess.square_rank(sq)

        for f in range(max(0, file-1), min(7, file+1)+1):
            for r in range(rank+1, 8): # Squares in front of White pawn
                test_sq = chess.square(f, r)
                if (
                    board.piece_type_at(test_sq) == chess.PAWN
                    and board.color_at(test_sq) == chess.BLACK
                ): 
                    return False
        return True

    def is_black_passed(sq):
        """
        Evaluates if a Black pawn is a passed pawn
        """
        file = chess.square_file(sq)
        rank = chess.square_rank(sq)

        for f in range(max(0, file-1), min(7, file+1)+1):
            for r in range(0, rank):  # Square in front of Black pawn
                test_sq = chess.square(f, r)
                if (
                    board.piece_type_at(test_sq) == chess.PAWN 
                    and board.color_at(test_sq) == chess.WHITE
                ): 
                    return False
        return True

    white_passed = sum(1 for sq in white_pawns if is_white_passed(sq))
    black_passed = sum(1 for sq in black_pawns if is_black_passed(sq))
    return white_passed - black_passed

def king_safety(board):
    """
    Calculates king safety as a
    result of castling status + pawn shield
    Positive -> White king is safer
    Negative -> Black king is safer
    """
    def safety_score(color):
        king_sq = board.king(color)
        king_file = chess.square_file(king_sq)
        king_rank = chess.square_rank(king_sq)

        # Castling status: king moved off e-file and has no castling rights
        castled = (king_file != 4) and not board.has_castling_rights(color)
        castle_score = 1 if castled else 0

        # Pawn shield: count pawns directly in front of king (3 squares)
        # Left, middle, right
        pawn_shield = 0
        direction = 1 if color == chess.WHITE else -1
        for df in [-1, 0, 1]:
            f = king_file + df
            r = king_rank + direction
            if 0 <= f <= 7 and 0 <= r <= 7:
                sq = chess.square(f, r)
                if board.piece_type_at(sq) == chess.PAWN and board.color_at(sq) == color:
                    pawn_shield += 1

        return castle_score + pawn_shield
    return safety_score(chess.WHITE) - safety_score(chess.BLACK)

def extract_features(board):
    """
    Extract features for training/evaluation
    """
    return {
        "material": material_balance(board),
        "center": center_control(board),
        "mobility": mobility(board),
        "tactical": tactical_pressure(board),
        "doubled": doubled_pawns(board),
        "isolated": isolated_pawns(board),
        "passed": passed_pawns(board),
        "king_safety": king_safety(board),
    }

def extract_move_features(board, move):
    """
    Extract and computer the feature difference before and after a move
    """
    before = extract_features(board)
    board.push(move)

    after = extract_features(board)
    board.pop()

    feat_diff = {feat: after[feat] - before[feat] for feat in before}
    return feat_diff
