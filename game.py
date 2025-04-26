import random
from settings import BOARD_SIZE, DOGS_REQUIRED_TO_WIN

turn = 'tiger'

def init_state():
    return [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def get_turn():
    return turn

def set_turn(new_turn):
    global turn
    turn = new_turn

def evaluate(current_state):
    if enough_dogs_killed(current_state):
        return 10  # Tiger wins
    
    r, c = find_tiger(current_state)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if is_valid_pos(nr, nc) and current_state[nr][nc] is None:
                return 0 # Tiger can still move
    return -10  # Tiger loses (can't move)

def find_tiger(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 'tiger':
                return (row, col)
    calc_start = (BOARD_SIZE - 1) // 2
    return (calc_start, calc_start)

def find_random_dog(board):
    dog_positions = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 'dog':
                dog_positions.append((row, col))

    if dog_positions:
        return random.choice(dog_positions)
    print("No dogs found on the board")
    return None

def enough_dogs_killed(board):
    dogs_alive = 0
    for row in board:
        for cell in row:
            if cell == 'dog':
                dogs_alive += 1
    
    if (4*(BOARD_SIZE - 1)) - dogs_alive >= DOGS_REQUIRED_TO_WIN:
        return True
    
    return False

def count_dogs_killed(board):
    dogs_alive = 0
    for row in board:
        for cell in row:
            if cell == 'dog':
                dogs_alive += 1
    
    return (4*(BOARD_SIZE - 1)) - dogs_alive
    
def try_kill_dogs(board):
        r, c = find_tiger(board)
        left = c - 1
        right = c + 1
        if is_valid_pos(r, left) and is_valid_pos(r, right):
            if board[r][left] == 'dog' and board[r][right] == 'dog':
                if no_adjacent_in_line(board, (r, left), 0, -1) and no_adjacent_in_line(board, (r, right), 0, 1):
                    board[r][left] = None
                    board[r][right] = None

        up = r - 1
        down = r + 1
        if is_valid_pos(up, c) and is_valid_pos(down, c):
            if board[up][c] == 'dog' and board[down][c] == 'dog':
                if no_adjacent_in_line(board, (up, c), -1, 0) and no_adjacent_in_line(board, (down, c), 1, 0):
                    board[up][c] = None
                    board[down][c] = None
                    
        diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in diagonals:
            diag1 = (r + dr, c + dc)
            diag2 = (r - dr, c - dc)
            if is_valid_pos(*diag1) and is_valid_pos(*diag2):
                if board[diag1[0]][diag1[1]] == 'dog' and board[diag2[0]][diag2[1]] == 'dog':
                    if no_adjacent_in_line(board, diag1, dr, dc) and no_adjacent_in_line(board, diag2, -dr, -dc):
                        board[diag1[0]][diag1[1]] = None
                        board[diag2[0]][diag2[1]] = None

def no_adjacent_in_line(board, pos, dr, dc):
    r, c = pos
    adj1 = (r + dr, c + dc)
    adj2 = (r - dr, c - dc)
    for ar, ac in [adj1, adj2]:
        if is_valid_pos(ar, ac) and board[ar][ac] == 'dog':
            return False
    return True

def is_valid_pos(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE
