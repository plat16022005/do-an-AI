# """
# Handling the AI moves.
# Có sử dụng thuật toán Negamax và cắt tỉa Alpha-beta
# """
# import random

# piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
# #Đánh giá mức độ quan trọng của từng quân cờ (VD: 0 là không thể để mất,Q là quan trọng nhất và chỉ mang tính tương đối)

# knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
#                  [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
#                  [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
#                  [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
#                  [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
#                  [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
#                  [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
#                  [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

# bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
#                  [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
#                  [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
#                  [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
#                  [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
#                  [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
#                  [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
#                  [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

# rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
#                [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
#                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
#                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
#                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
#                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
#                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
#                [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

# queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
#                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
#                 [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
#                 [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
#                 [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
#                 [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
#                 [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
#                 [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

# pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
#                [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
#                [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
#                [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
#                [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
#                [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
#                [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
#                [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

# piece_position_scores = {"wN": knight_scores,
#                          "bN": knight_scores[::-1],
#                          "wB": bishop_scores,
#                          "bB": bishop_scores[::-1],
#                          "wQ": queen_scores,
#                          "bQ": queen_scores[::-1],
#                          "wR": rook_scores,
#                          "bR": rook_scores[::-1],
#                          "wp": pawn_scores,
#                          "bp": pawn_scores[::-1]}

# CHECKMATE = 1000
# STALEMATE = 0
# DEPTH = 3


# def findBestMove(game_state, valid_moves, return_queue):
#     global next_move
#     next_move = None
#     random.shuffle(valid_moves)
#     findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
#                              1 if game_state.white_to_move else -1)
    
#     # Tạo một bản sao của ma trận bàn cờ sau khi thực hiện nước đi
#     if next_move:
#         game_state.makeMove(next_move)  # Thực hiện nước đi
#         new_board = [row.copy() for row in game_state.board]  # Sao chép ma trận bàn cờ
#         game_state.undoMove()  # Hoàn tác nước đi để tránh ảnh hưởng đến trạng thái hiện tại
#         return_queue.put((next_move, new_board))  # Trả về nước đi và ma trận bàn cờ
#     else:
#         return_queue.put((None, None))  # Trả về None nếu không có nước đi hợp lệ


# def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
#     global next_move
#     if depth == 0:
#         return turn_multiplier * scoreBoard(game_state)
#     # move ordering - implement later //TODO
#     max_score = -CHECKMATE
#     for move in valid_moves:
#         game_state.makeMove(move)
#         next_moves = game_state.getValidMoves()
#         score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
#         if score > max_score:
#             max_score = score
#             if depth == DEPTH:
#                 next_move = move
#         game_state.undoMove()
#         if max_score > alpha:
#             alpha = max_score
#         if alpha >= beta:
#             break
#     return max_score


# def scoreBoard(game_state):
#     """
#     Score the board. A positive score is good for white, a negative score is good for black.
#     """
#     if game_state.checkmate:
#         if game_state.white_to_move:
#             return -CHECKMATE  # black wins
#         else:
#             return CHECKMATE  # white wins
#     elif game_state.stalemate:
#         return STALEMATE #Hòa
#     #Chưa hiểu tạo score làm gì
#     score = 0 #Nếu không có tình huống checkmate hay stalemate thì khởi tạo score
#     for row in range(len(game_state.board)):
#         for col in range(len(game_state.board[row])):
#             piece = game_state.board[row][col]
#             if piece != "--":
#                 piece_position_score = 0
#                 if piece[1] != "K":
#                     piece_position_score = piece_position_scores[piece][row][col]
#                 if piece[0] == "w":
#                     score += piece_score[piece[1]] + piece_position_score
#                 if piece[0] == "b":
#                     score -= piece_score[piece[1]] + piece_position_score

#     return score


# # def findRandomMove(valid_moves):
# #     """
# #     Picks and returns a random valid move.
# #     """
# #     return random.choice(valid_moves)
import copy

# Hệ số giá trị quân cờ
piece_values = {
    'tt': 1, 'td': -1,   # Tốt
    'nt': 3, 'nd': -3,   # Mã
    'xt': 5, 'xd': -5,   # Xe
    'Tt': 3, 'Td': -3,   # Tượng
    'ht': 9, 'hd': -9,   # Hậu
    'vt': 100, 'vd': -100 # Vua
}

# Bảng điểm vị trí cho các quân cờ
position_scores = {
    'tt': [
        [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
        [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
        [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
        [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
        [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
        [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
        [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
        [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
    ],
    'td': [
        [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
        [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
        [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
        [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
        [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
        [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
        [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
        [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
    ],
    'nt': [
        [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
        [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
        [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
        [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
        [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
        [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
        [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
        [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]
    ],
    'nd': [
        [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
        [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
        [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
        [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
        [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
        [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
        [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
        [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]
    ],
    'Tt': [
        [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
        [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
        [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
        [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
        [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
        [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
        [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
        [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]
    ],
    'Td': [
        [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
        [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
        [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
        [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
        [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
        [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
        [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
        [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]
    ],
    'xt': [
        [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
        [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]
    ],
    'xd': [
        [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25],
        [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
        [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
    ],
    'ht': [
        [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
        [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
        [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
        [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
        [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
        [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
        [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
        [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]
    ],
    'hd': [
        [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
        [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
        [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
        [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
        [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
        [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
        [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
        [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]
    ],
    'vt': [
        [0.3, 0.3, 0.2, 0.1, 0.1, 0.2, 0.3, 0.3],
        [0.3, 0.2, 0.1, 0.0, 0.0, 0.1, 0.2, 0.3],
        [0.2, 0.1, 0.0, -0.1, -0.1, 0.0, 0.1, 0.2],
        [0.1, 0.0, -0.1, -0.2, -0.2, -0.1, 0.0, 0.1],
        [0.0, -0.1, -0.2, -0.3, -0.3, -0.2, -0.1, 0.0],
        [-0.1, -0.2, -0.3, -0.4, -0.4, -0.3, -0.2, -0.1],
        [-0.2, -0.3, -0.4, -0.5, -0.5, -0.4, -0.3, -0.2],
        [-0.3, -0.4, -0.5, -0.6, -0.6, -0.5, -0.4, -0.3]
    ],
    'vd': [
        [-0.3, -0.4, -0.5, -0.6, -0.6, -0.5, -0.4, -0.3],
        [-0.2, -0.3, -0.4, -0.5, -0.5, -0.4, -0.3, -0.2],
        [-0.1, -0.2, -0.3, -0.4, -0.4, -0.3, -0.2, -0.1],
        [0.0, -0.1, -0.2, -0.3, -0.3, -0.2, -0.1, 0.0],
        [0.1, 0.0, -0.1, -0.2, -0.2, -0.1, 0.0, 0.1],
        [0.2, 0.1, 0.0, -0.1, -0.1, 0.0, 0.1, 0.2],
        [0.3, 0.2, 0.1, 0.0, 0.0, 0.1, 0.2, 0.3],
        [0.3, 0.3, 0.2, 0.1, 0.1, 0.2, 0.3, 0.3]
    ]
}


def evaluate_board(board):
    """Đánh giá bàn cờ với cả giá trị quân và vị trí"""
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in piece_values:
                # Giá trị quân cờ
                score += piece_values[piece]
                
                # Điểm vị trí
                if piece in position_scores:
                    pos_score = position_scores[piece][row][col] if piece[1] == 't' else -position_scores[piece][7-row][col]
                    score += pos_score
                    
    return score


def generate_pawn_moves(board, row, col, is_white):
    moves = []
    direction = -1 if is_white else 1
    start_row = 6 if is_white else 1
    
    # Di chuyển tiến
    if 0 <= row + direction < 8 and board[row + direction][col] == '-':
        moves.append(((row, col), (row + direction, col)))
        # Di chuyển 2 ô từ vị trí ban đầu
        if row == start_row and board[row + 2*direction][col] == '-':
            moves.append(((row, col), (row + 2*direction, col)))
    
    # Ăn quân chéo
    for dc in [-1, 1]:
        if 0 <= col + dc < 8 and 0 <= row + direction < 8:
            target = board[row + direction][col + dc]
            if target != '-' and target[1] != ('t' if is_white else 'd'):
                moves.append(((row, col), (row + direction, col + dc)))
    
    return moves

def generate_knight_moves(board, row, col, is_white):
    moves = []
    knight_moves = [(-2,-1), (-2,1), (-1,-2), (-1,2),
                    (1,-2), (1,2), (2,-1), (2,1)]
    
    for dr, dc in knight_moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target == '-' or target[1] != ('t' if is_white else 'd'):
                moves.append(((row, col), (new_row, new_col)))
    
    return moves

def generate_rook_moves(board, row, col, is_white):
    """Tạo nước đi cho quân Xe"""
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        while 0 <= new_row < 8 and 0 <= new_col < 8:  # Trong phạm vi bàn cờ
            target = board[new_row][new_col]
            # Nếu ô trống, thêm nước đi
            if target == '-':
                moves.append(((row, col), (new_row, new_col)))
            # Nếu gặp quân đối phương, thêm nước đi và dừng
            elif target[1] != ('t' if is_white else 'd'):
                moves.append(((row, col), (new_row, new_col)))
                break
            # Nếu gặp quân cùng màu, dừng
            else:
                break
            new_row += dr
            new_col += dc
    
    return moves

def generate_bishop_moves(board, row, col, is_white):
    """Tạo nước đi cho quân Tượng"""
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 4 hướng chéo
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        while 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target == '-':
                moves.append(((row, col), (new_row, new_col)))
            elif target[1] != ('t' if is_white else 'd'):
                moves.append(((row, col), (new_row, new_col)))
                break
            else:
                break
            new_row += dr
            new_col += dc
    
    return moves

def generate_queen_moves(board, row, col, is_white):
    """Tạo nước đi cho quân Hậu (kết hợp Xe và Tượng)"""
    moves = []
    # Hậu di chuyển như Xe
    moves += generate_rook_moves(board, row, col, is_white)
    # Hậu di chuyển như Tượng
    moves += generate_bishop_moves(board, row, col, is_white)
    return moves

def generate_king_moves(board, row, col, is_white):
    """Tạo nước đi cho quân Vua"""
    moves = []
    king_moves = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]  # 8 hướng xung quanh
    
    for dr, dc in king_moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target == '-' or target[1] != ('t' if is_white else 'd'):
                moves.append(((row, col), (new_row, new_col)))
    
    # TODO: Thêm logic nhập thành (castling) nếu cần
    return moves

# Cập nhật lại hàm generate_all_moves để sử dụng các hàm mới
def generate_all_moves(board, is_white):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '-' and piece[1] == ('t' if is_white else 'd'):
                if piece[0] == 't':  # Tốt
                    moves += generate_pawn_moves(board, row, col, is_white)
                elif piece[0] == 'n':  # Mã
                    moves += generate_knight_moves(board, row, col, is_white)
                elif piece[0] == 'x':  # Xe
                    moves += generate_rook_moves(board, row, col, is_white)
                elif piece[0] == 'T':  # Tượng
                    moves += generate_bishop_moves(board, row, col, is_white)
                elif piece[0] == 'h':  # Hậu
                    moves += generate_queen_moves(board, row, col, is_white)
                elif piece[0] == 'v':  # Vua
                    moves += generate_king_moves(board, row, col, is_white)
    return moves

def alpha_beta(board, depth, alpha, beta, is_white):
    """Thuật toán Alpha-Beta Pruning cải tiến"""
    # Kiểm tra chiếu bí hoặc hết nước đi
    if depth == 0:
        return evaluate_board(board), None
    
    moves = generate_all_moves(board, is_white)
    if not moves:
        # Kiểm tra chiếu bí hoặc hòa
        return evaluate_board(board), None
    
    best_move = None
    
    if is_white:
        max_eval = -float('inf')
        for move in moves:
            new_board = make_move(board, move)
            eval, _ = alpha_beta(new_board, depth-1, alpha, beta, False)
            
            if eval > max_eval:
                max_eval = eval
                best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = make_move(board, move)
            eval, _ = alpha_beta(new_board, depth-1, alpha, beta, True)
            
            if eval < min_eval:
                min_eval = eval
                best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval, best_move

def make_move(board, move):
    """Tạo bàn cờ mới sau khi thực hiện nước đi"""
    new_board = copy.deepcopy(board)
    (start_row, start_col), (end_row, end_col) = move
    new_board[end_row][end_col] = new_board[start_row][start_col]
    new_board[start_row][start_col] = '-'
    return new_board

def ai_make_move(board, depth=3, is_white=True):
    """Giao diện chính để AI thực hiện nước đi"""
    eval, best_move = alpha_beta(board, depth, -float('inf'), float('inf'), is_white)
    if best_move:
        (start_row, start_col), (end_row, end_col) = best_move
        return start_row, start_col, end_row, end_col
    return None