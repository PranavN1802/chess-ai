import chess
import random
import time

def random_move(board):
    legal_moves = list(board.legal_moves)
    random_move = random.choice(legal_moves)
    return random_move

def evaluate_board(board):
    # Piece values (same as before)
    piece_values = {
        'P': 124, 'N': 781, 'B': 825, 'R': 1276, 'Q': 2538, 'K': 20000,
        'p': -124, 'n': -781, 'b': -825, 'r': -1276, 'q': -2538, 'k': -20000
    }

    # Piece-square tables (adjusted for each piece)
    pawn_table = [
        0,   0,   0,   0,   0,   0,   0,   0,
       -7,   7,  -3, -13,   5, -16,  10,  -8,
        5, -12,  -7,  22,  -8,  -5, -15,  -9,
       13,   0, -13,   1,  11,  -2, -13,   5,
       -4, -23,   6,  20,  40,  17,   4,  -8,
       -9, -15,  11,  15,  32,  22,   5, -22,
        3,   3,  10,  19,  16,  19,   7,  -5,
        0,   0,   0,   0,   0,   0,   0,   0
    ]

    knight_table = [
      -175, -92, -74, -73, -73, -74, -92, -175,
      -77,  -41, -27, -15, -15, -27, -41,  -77,
      -61,  -17,   6,  12,  12,   6, -17,  -61,
      -35,    8,  40,  49,  49,  40,   8,  -35,
      -34,   13,  44,  51,  51,  44,  13,  -34,
        -9,   22,  58,  53,  53,  58,  22,   -9,
      -67,  -27,   4,  37,  37,   4, -27,  -67,
     -201,  -83, -56, -26, -26, -56, -83, -201
    ]

    bishop_table = [
      -53,  -5,  -8, -23, -23,  -8,  -5, -53,
      -15,   8,  19,   4,   4,  19,   8, -15,
      -7,   21,  -5,  17,  17,  -5,  21,  -7,
      -5,   11,  25,  39,  39,  25,  11,  -5,
     -12,  29,  22,  31,  31,  22,  29, -12,
     -16,   6,   1,  11,  11,   1,   6, -16,
     -17, -14,   5,   0,   0,   5, -14, -17,
     -48,   1, -14, -23, -23, -14,   1, -48
    ]

    rook_table = [
      -31, -20, -14,  -5,  -5, -14, -20, -31,
      -21, -13,  -8,   6,   6,  -8, -13, -21,
      -25, -11,  -1,   3,   3,  -1, -11, -25,
      -13,  -5,  -4,  -6,  -6,  -4,  -5, -13,
      -27, -15,  -4,   3,   3,  -4, -15, -27,
      -22,  -2,   6,  12,  12,   6,  -2, -22,
       -2,  12,  16,  18,  18,  16,  12,  -2,
      -17, -19,  -1,   9,   9,  -1, -19, -17
    ]

    queen_table = [
       3, -5, -5,  4,  4, -5, -5,  3,
      -3,  5,  8, 12, 12,  8,  5, -3,
      -3,  6, 13,  7,  7, 13,  6, -3,
       4,  5,  9,  8,  8,  9,  5,  4,
       0, 14, 12,  5,  5, 12, 14,  0,
      -4, 10,  6,  8,  8,  6, 10, -4,
      -5,  6, 10,  8,  8, 10,  6, -5,
      -2, -2,  1, -2, -2,  1, -2, -2
    ]

    king_table = [
      -30, -40, -40, -50, -50, -40, -40, -30,
      -30, -40, -40, -50, -50, -40, -40, -30,
      -30, -40, -40, -50, -50, -40, -40, -30,
      -30, -40, -40, -50, -50, -40, -40, -30,
      -20, -30, -30, -40, -40, -30, -30, -20,
      -10, -20, -20, -20, -20, -20, -20, -10,
       10,  10,   0,   0,   0,   0,  10,  10,
       20,  40,  10,   0,   0,  10,  40,  20
    ]

    # Reverse the tables for black
    pawn_table_black = pawn_table[::-1]
    knight_table_black = knight_table[::-1]
    bishop_table_black = bishop_table[::-1]
    rook_table_black = rook_table[::-1]
    queen_table_black = queen_table[::-1]
    king_table_black = king_table[::-1]

    # Evaluate the board based on piece values and square positions
    board_value = 0
    for square in range(64):
        piece = board.piece_at(square)
        if piece is not None:
            piece_type = piece.symbol()

            # Add piece value
            board_value += piece_values[piece_type]

            # Add positional value based on the piece-square table
            if piece_type == 'P':
                board_value += pawn_table[square]
            elif piece_type == 'N':
                board_value += knight_table[square]
            elif piece_type == 'B':
                board_value += bishop_table[square]
            elif piece_type == 'R':
                board_value += rook_table[square]
            elif piece_type == 'Q':
                board_value += queen_table[square]
            elif piece_type == 'K':
                board_value += king_table[square]
            elif piece_type == 'p':
                board_value += pawn_table_black[square]
            elif piece_type == 'n':
                board_value += knight_table_black[square]
            elif piece_type == 'b':
                board_value += bishop_table_black[square]
            elif piece_type == 'r':
                board_value += rook_table_black[square]
            elif piece_type == 'q':
                board_value += queen_table_black[square]
            elif piece_type == 'k':
                board_value += king_table_black[square]

    # Checkmate and stalemate evaluation
    if board.is_checkmate():
        if board.turn:
            return -9999  # White is checkmated
        else:
            return 9999  # Black is checkmated
    if board.is_stalemate():
        return 0

    return board_value

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizing_player:
        max_eval = -9999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = 9999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def main():
    board = chess.Board()
    print(board)

    while not board.is_game_over():
        if board.turn:  # White's turn
            # Use minimax for White's move
            print("Using minimax for White's turn.")
            best_move = None
            max_eval = -9999
            for move in board.legal_moves:
                board.push(move)
                eval = minimax(board, 3, -9999, 9999, True)  # Maximizing player is True for White
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            board.push(best_move)
            print(board)
            print("Time taken: ", time.process_time())

        else:  # Black's turn
            move = input("Enter your move (e.g., e2e4): ")
            board.push_san(move)
            print(board)
            print("")

if __name__ == "__main__":
    main()
