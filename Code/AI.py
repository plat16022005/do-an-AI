import copy
import random
import math
from queue import PriorityQueue
import heapq
import copy
from collections import deque
import sys
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
    """Đánh giá bàn cờ với cả giá trị quân và vị trí trả về điểm """
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
                    score += pos_score*10
                    
    # white_score = len(generate_all_moves(board, True))
    # black_score = len(generate_all_moves(board, False))
    # score += (white_score - black_score) * 0.1  
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

def ai_make_move(board, depth=1, is_white=True):
    """Giao diện chính để AI thực hiện nước đi"""
    eval, best_move = alpha_beta(board, depth, -float('inf'), float('inf'), is_white)
    if best_move:
        (start_row, start_col), (end_row, end_col) = best_move
        return start_row, start_col, end_row, end_col
    return None

class MCTSAI:
    def __init__(self, exploration_weight=1.414):
        self.exploration_weight = exploration_weight
        self.piece_values = {
            'tt': 1, 'td': -1,   # Tốt
            'nt': 3, 'nd': -3,   # Mã
            'xt': 5, 'xd': -5,   # Xe
            'Tt': 3, 'Td': -3,   # Tượng
            'ht': 9, 'hd': -9,   # Hậu
            'vt': 100, 'vd': -100 # Vua
        }
    
    class Node:
        def __init__(self, board, parent=None, move=None, is_white=True):
            self.board = board
            self.parent = parent
            self.move = move
            self.is_white = is_white
            self.children = []
            self.wins = 0  # Tổng giá trị tích lũy
            self.visits = 0
            self.untried_moves = None
    
    def make_move(self, board, move):
        """Tạo bàn cờ mới sau khi thực hiện nước đi"""
        new_board = copy.deepcopy(board)
        (start_row, start_col), (end_row, end_col) = move
        new_board[end_row][end_col] = new_board[start_row][start_col]
        new_board[start_row][start_col] = '-'
        return new_board
    
    def generate_pawn_moves(self, board, row, col, is_white):
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
    
    def generate_knight_moves(self, board, row, col, is_white):
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
    
    def generate_bishop_moves(self, board, row, col, is_white):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
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
    
    def generate_rook_moves(self, board, row, col, is_white):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
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
    
    def generate_queen_moves(self, board, row, col, is_white):
        moves = self.generate_rook_moves(board, row, col, is_white)
        moves += self.generate_bishop_moves(board, row, col, is_white)
        return moves
    
    def generate_king_moves(self, board, row, col, is_white):
        moves = []
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dr, dc in king_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target == '-' or target[1] != ('t' if is_white else 'd'):
                    moves.append(((row, col), (new_row, new_col)))
        
        return moves
    
    def generate_all_moves(self, board, is_white):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '-' and piece[1] == ('t' if is_white else 'd'):
                    if piece[0] == 't':  # Tốt
                        moves += self.generate_pawn_moves(board, row, col, is_white)
                    elif piece[0] == 'n':  # Mã
                        moves += self.generate_knight_moves(board, row, col, is_white)
                    elif piece[0] == 'x':  # Xe
                        moves += self.generate_rook_moves(board, row, col, is_white)
                    elif piece[0] == 'T':  # Tượng
                        moves += self.generate_bishop_moves(board, row, col, is_white)
                    elif piece[0] == 'h':  # Hậu
                        moves += self.generate_queen_moves(board, row, col, is_white)
                    elif piece[0] == 'v':  # Vua
                        moves += self.generate_king_moves(board, row, col, is_white)
        
        # Thêm hàm kiểm tra ô trung tâm
        def is_center_square(pos):
            r, c = pos
            return 3 <= r <= 4 and 3 <= c <= 4
        
        # Sắp xếp nước đi theo độ ưu tiên
        moves.sort(key=lambda m: (
            -self.piece_values.get(board[m[1][0]][m[1][1]], 0),  # Ưu tiên ăn quân giá trị cao (giảm dần)
            is_center_square(m[1]),                              # Ưu tiên ô trung tâm (True > False)
            -self.piece_values.get(board[m[0][0]][m[0][1]], 0)   # Ưu tiên quân có giá trị cao di chuyển
        ), reverse=True)
        
        return moves
    
    def evaluate_board(self, board):
        # Kiểm tra chiếu bí trước
        if self.is_checkmate(board, False):  # Đen bị chiếu bí
            return float('inf')
        if self.is_checkmate(board, True):   # Trắng bị chiếu bí
            return float('-inf')
        
        # Kiểm tra chiếu
        if self.is_check(board, False):  # Đen bị chiếu
            return 1000
        if self.is_check(board, True):   # Trắng bị chiếu
            return -1000
        
        # Đánh giá bình thường
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece in self.piece_values:
                    score += self.piece_values[piece]
                    # Thưởng điểm vị trí
                    if piece in position_scores:
                        pos_score = position_scores[piece][row][col] if piece[1] == 't' else -position_scores[piece][7-row][col]
                        score += pos_score * 10
                            
            # Thêm phần thưởng cho tấn công
        score += self.calculate_aggression_score(board)
        return score
        
    def calculate_aggression_score(self, board):
        """Tính điểm tấn công - khuyến khích ăn quân"""
        aggression = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '-' and piece[1] == 't':  # Quân trắng
                    moves = self.generate_all_moves(board, True)
                    for (_, _), (r, c) in moves:
                        if board[r][c] != '-' and board[r][c][1] == 'd':  # Ăn quân đen
                            aggression += 0.5 * abs(self.piece_values[board[r][c]])
                elif piece != '-' and piece[1] == 'd':  # Quân đen
                    moves = self.generate_all_moves(board, False)
                    for (_, _), (r, c) in moves:
                        if board[r][c] != '-' and board[r][c][1] == 't':  # Ăn quân trắng
                            aggression -= 0.5 * abs(self.piece_values[board[r][c]])
        return aggression
    
    def rollout(self, board, is_white):
        current_board = copy.deepcopy(board)
        current_player = is_white
        
        for _ in range(1):  # Giới hạn số nước đi
            # Kiểm tra chiếu bí trước khi di chuyển
            if self.is_checkmate(current_board, not current_player):
                return float('inf') if current_player == is_white else float('-inf')
            
            moves = self.generate_all_moves(current_board, current_player)
            if not moves:
                break
                
            # Ưu tiên nước đi chiếu hoặc ăn quân
            checking_moves = []
            capturing_moves = []
            
            for move in moves:
                new_board = self.make_move(current_board, move)
                if self.is_check(new_board, not current_player):
                    checking_moves.append(move)
                elif current_board[move[1][0]][move[1][1]] != '-':
                    capturing_moves.append(move)
            
            if checking_moves:
                move = random.choice(checking_moves)
            elif capturing_moves:
                move = random.choice(capturing_moves)
            else:
                move = random.choice(moves)
                
            current_board = self.make_move(current_board, move)
            current_player = not current_player
        
        return self.evaluate_board(current_board)
    
    def select(self, node):
        while node.untried_moves == [] and node.children != []:
            # Sử dụng cắt tỉa alpha-beta để chọn node con
            best_score = -float('inf')
            best_child = None
            
            for child in node.children:
                score = child.wins/child.visits + self.exploration_weight * math.sqrt(math.log(node.visits)/child.visits)
                
                # Cắt tỉa alpha-beta
                if score > best_score:
                    best_score = score
                    best_child = child
                    
            node = best_child
        return node
        # while node.untried_moves == [] and node.children != []:
        #     # Thêm ưu tiên cho nước đi ăn quân
        #     capturing_children = [c for c in node.children 
        #                     if node.board[c.move[1][0]][c.move[1][1]] != '-']
            
        #     if capturing_children:
        #         node = max(capturing_children, 
        #                 key=lambda c: c.wins/c.visits + 
        #                 self.exploration_weight * math.sqrt(math.log(node.visits)/c.visits))
        #     else:
        #         node = max(node.children, 
        #                 key=lambda c: c.wins/c.visits + 
        #                 self.exploration_weight * math.sqrt(math.log(node.visits)/c.visits))
        # return node
    def expand(self, node):
        """Mở rộng cây bằng cách thêm một node con mới"""
        if not node.untried_moves:
            node.untried_moves = self.generate_all_moves(node.board, node.is_white)
        
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            new_board = self.make_move(node.board, move)
            child = self.Node(new_board, parent=node, move=move, is_white=not node.is_white)
            node.untried_moves.remove(move)
            node.children.append(child)
            return child
        return node
    
    def backpropagate(self, node, result):
        """Cập nhật kết quả từ node lá lên root"""
        while node is not None:
            node.visits += 1
            node.wins += result if node.is_white else -result
            node = node.parent
    
    def best_move(self, board, is_white, iterations=10):
        root = self.Node(board, is_white=is_white)
        
        # Trước tiên kiểm tra xem có nước đi chiếu bí ngay lập tức không
        immediate_moves = self.generate_all_moves(board, is_white)
        for move in immediate_moves:
            new_board = self.make_move(board, move)
            if self.is_checkmate(new_board, not is_white):
                return move
        
        # Nếu không có chiếu bí ngay, thực hiện MCTS bình thường
        for _ in range(iterations):
            node = self.select(root)
            node = self.expand(node)
            result = self.rollout(node.board, node.is_white)
            self.backpropagate(node, result)
        
        if not root.children:
            return None
        
        # Ưu tiên chọn nước đi dẫn đến chiếu
        checking_moves = [c for c in root.children 
                        if self.is_check(self.make_move(board, c.move), not is_white)]
        
        if checking_moves:
            best_child = max(checking_moves, key=lambda c: c.visits)
        else:
            best_child = max(root.children, key=lambda c: c.visits)
        
        return best_child.move
    
    def ai_make_move(self, board, is_white=True, iterations=100):
        """Giao diện chính để AI thực hiện nước đi"""
        best_move = self.best_move(board, is_white, iterations)
        if best_move:
            (start_row, start_col), (end_row, end_col) = best_move
            return start_row, start_col, end_row, end_col
        return None

    def is_check(self, board, is_white):
        """Kiểm tra xem vua có đang bị chiếu không"""
        king_pos = None
        king_symbol = 'vt' if is_white else 'vd'
        
        # Tìm vị trí vua
        for row in range(8):
            for col in range(8):
                if board[row][col] == king_symbol:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # Kiểm tra các quân đối phương có thể tấn công vua
        opponent_moves = self.generate_all_moves(board, not is_white)
        for (_, _), (r, c) in opponent_moves:
            if (r, c) == king_pos:
                return True
        return False

    def is_checkmate(self, board, is_white):
        """Kiểm tra chiếu bí"""
        if not self.is_check(board, is_white):
            return False
        
        # Kiểm tra xem có nước đi hợp lệ nào không
        moves = self.generate_all_moves(board, is_white)
        for move in moves:
            new_board = self.make_move(board, move)
            if not self.is_check(new_board, is_white):
                return False
        return True

def a_star_best_move(board, is_white, max_depth=3):

    def f_score(g, h):
        return g + h

    open_list = []
    visited = set()
    root_h = evaluate_board(board)
    heapq.heappush(open_list, (f_score(0, root_h), 0, root_h, None, board))  # (f, g, h, move, board)

    best_move = None
    best_h = None

    while open_list:
        f, g, h, move_so_far, current_board = heapq.heappop(open_list)

        if g >= max_depth:
            continue

        possible_moves = generate_all_moves(current_board, is_white)

        for move in possible_moves:
            new_board = make_move(current_board, move)
            new_g = g + 1
            new_h = evaluate_board(new_board)
            heapq.heappush(open_list, (f_score(new_g, new_h), new_g, new_h, move, new_board))

            if best_move is None:
                best_move = move
                best_h = new_h
            elif (not is_white and new_h > best_h) or (is_white and new_h < best_h):
                best_move = move
                best_h = new_h

    return best_move

def DFS(board, is_white, max_depth=1):
    open_list = []
    open_list.append((0, None, board))  # (cost, depth, move, board)
    
    best_move = None


    while open_list:
        depth, move, current_board = open_list.pop()

        if depth >= max_depth:
            continue

        possible_moves = generate_all_moves(current_board, is_white)
        for move in possible_moves:
            new_board = make_move(copy.deepcopy(current_board), move)


            open_list.append((depth + 1, move, new_board))


            best_move = move

    return best_move

def Stochastic_Hill_Climbing(board, is_white, max_depth=1):
    current_board = board
    best_move = None

    for _ in range(max_depth):  # giới hạn số bước nếu muốn
        neighbors = []
        possible_moves = generate_all_moves(current_board, is_white)
        for move in possible_moves:
            new_board = make_move(copy.deepcopy(current_board), move)
            if evaluate_board(new_board) > evaluate_board(current_board):
                neighbors.append((new_board, move))
        
        if not neighbors:
            break  # không còn neighbor tốt hơn

        next_board, next_move = random.choice(neighbors)
        current_board = next_board
        best_move = next_move  # cập nhật move tốt hơn
    return best_move

def king_is_checked(board,is_white):
    """kiểm tra xem vua có bị chiếu hay không"""
    if is_white:
        king_symbol = 'vt'
    else:
        king_symbol = 'vd'
    
    pos_king = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == king_symbol:
                pos_king = (row, col)
                break
    
    if not pos_king:
        return False

    enemy_moves = generate_all_moves(board, not is_white)
    for move in enemy_moves:
        _,(e_row,e_col) = move
        if (e_row,e_col) == pos_king:
            return True

    return False

def queen_is_checked(board,is_white):
    """kiểm tra xem quân hậu có bị ăn hay không"""
    if is_white:
        queen_symbol = 'ht'
    else:
        queen_symbol = 'hd'
    
    pos_queen = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == queen_symbol:
                pos_queen = (row, col)
                break
    
    if not pos_queen:
        return False

    enemy_moves = generate_all_moves(board, not is_white)
    for move in enemy_moves:
        _,(e_row,e_col) = move
        if (e_row,e_col) == pos_queen:
            return True

    return False


def constraints(board,is_white,move):
    """ràng buộc cho nhóm thuật toán ràng buộc"""
    
    if king_is_checked(board,is_white):
        return False
    
    # if queen_is_checked(board,is_white):
    #     return False
    
    return True


def is_checkmate( board, is_white):
        """Kiểm tra chiếu bí"""
        if not king_is_checked(board, is_white):
            return False
        
        # Kiểm tra xem có nước đi hợp lệ nào không
        moves = generate_all_moves(board, is_white)
        for move in moves:
            new_board = make_move(board, move)
            if not king_is_checked(new_board, is_white):
                return False
        return True

def backtracking(board, is_white, depth=2): 
    
    best_move = None
    best_eval = -float('inf') if is_white else float('inf')
    
    if depth == 0 or is_checkmate(board, is_white):
        return evaluate_board(board), None
    
    moves = generate_all_moves(board, is_white)
    for move in moves:
        new_board = make_move(board, move)
        if not constraints(board, is_white, move):
            continue
        eval_tmp, _ = backtracking(new_board, not  is_white, depth-1)

        if is_white:
            if eval_tmp > best_eval:
                best_eval = eval_tmp
                best_move = move
        else:
            if eval_tmp < best_eval:
                best_eval = eval_tmp
                best_move = move

    return best_eval,best_move

def AND_OR_SEARCH(board, is_white,depth = 1):
    path = []
    plan = OR_SEARCH(board, is_white, path,depth)
    return plan

def OR_SEARCH(board, is_white, path,depth):
    if is_checkmate(board, not is_white) or depth == 0:
        return path

    moves = generate_all_moves(board, is_white)
    if not moves:
        return None
    
    move_score =[]
    for move in moves:
        if not constraints(board, is_white, move):
            continue
        new_board = make_move(board, move)
        if not new_board:
            continue
        eval_score = evaluate_board(new_board)
        move_score.append((move,eval_score))

    move_score = sorted(move_score,key=lambda x: x[1],reverse=is_white) 

    choice = soft_choice(move_score)
    if not choice:
        return None
    else:
        for move,_ in choice:
            new_board = make_move(board, move)
            plan = AND_SEARCH(new_board, not is_white, path + [move],depth-1)
            if plan:
                return plan[0]
    return None

def AND_SEARCH(board, is_white, path,depth):
    if is_checkmate(board, not is_white) or depth == 0 :
        return path

    moves = generate_all_moves(board, is_white)
    if not moves:
        return None

    for move in moves:
        if not constraints(board, is_white, move):
            continue
        new_board = make_move(board, move)
        if new_board in path:
            continue
        plan = OR_SEARCH(new_board, not is_white, path + [move],depth-1)
        if not plan:
            return None  
    return path

def soft_choice(move_score, k = 3 ):
    if move_score == []:
        return []
    
    weights = []
    for i in range(len(move_score),0,-1):
        weights.append((i+1) * 10)    
    
    selected = random.choices(move_score, weights=weights, k=1)
    
    return selected
