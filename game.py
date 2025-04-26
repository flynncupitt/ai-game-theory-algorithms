import random
from settings import BOARD_SIZE, DOGS_REQUIRED_TO_WIN
from tkinter import messagebox

# tiger_pos = (2, 2)
turn = 'tiger'

def init_state():
    return [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def get_turn():
    return turn

# def get_tiger_pos():
#     return tiger_pos

# def set_tiger_pos(new_pos):
#     global tiger_pos
#     tiger_pos = new_pos

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
                # print("Evaluating: Tiger can move!")
                return 0  # Tiger can move, game continues
    return -10  # Tiger is trapped, dogs win

def find_tiger(board):
    """Find the position of the tiger on the board."""
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 'tiger':
                return (row, col)
    calc_start = (BOARD_SIZE - 1) // 2
    return (calc_start, calc_start)

def find_random_dog(board):
    """Find the position of a random dog on the board."""
    dog_positions = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 'dog':
                dog_positions.append((row, col))  # Collect all dog positions

    if dog_positions:
        return random.choice(dog_positions)  # Return a random dog position
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
        r, c = find_tiger(board)  # Get the tiger's position
        # print(f"Checking for dogs to kill at position: {r}, {c}")

        # Check if there is a dog on both sides of the tiger in the same row
        left = c - 1
        right = c + 1
        if is_valid_pos(r, left) and is_valid_pos(r, right):  # Ensure positions are valid
            if board[r][left] == 'dog' and board[r][right] == 'dog':  # Dogs on both sides
                # Ensure no adjacent dogs to the left and right dogs
                if no_adjacent_in_line(board, (r, left), 0, -1) and no_adjacent_in_line(board, (r, right), 0, 1):
                    board[r][left] = None  # Remove the left dog
                    board[r][right] = None  # Remove the right dog
                    # print("Dogs killed in row!")
                    # gui.draw_board() gets called in gui instead
        #         else:
        #             print("Cannot kill dogs in row, adjacent dogs in line")
        #     else:
        #         print("No dogs on both sides of the tiger in row")
        # else:
        #     print("Invalid positions for dogs in row")

        # Check if there is a dog on both sides of the tiger in the same column
        up = r - 1
        down = r + 1
        if is_valid_pos(up, c) and is_valid_pos(down, c):  # Ensure positions are valid
            if board[up][c] == 'dog' and board[down][c] == 'dog':  # Dogs above and below
                # Ensure no adjacent dogs to the above and below dogs
                if no_adjacent_in_line(board, (up, c), -1, 0) and no_adjacent_in_line(board, (down, c), 1, 0):
                    board[up][c] = None  # Remove the upper dog
                    board[down][c] = None  # Remove the lower dog
                    # print("Dogs killed in column!")
                    # gui.draw_board()
        #         else:
        #             print("Cannot kill dogs in column, adjacent dogs in line")
        #     else:
        #         print("No dogs on both sides of the tiger in column")
        # else:
        #     print("Invalid positions for dogs in column")

        # Check if there is a dog on both sides of the tiger in the diagonals
        diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in diagonals:
            diag1 = (r + dr, c + dc)
            diag2 = (r - dr, c - dc)
            if is_valid_pos(*diag1) and is_valid_pos(*diag2):  # Ensure positions are valid
                if board[diag1[0]][diag1[1]] == 'dog' and board[diag2[0]][diag2[1]] == 'dog':  # Dogs on both diagonals
                    # Ensure no adjacent dogs to the diagonal dogs
                    if no_adjacent_in_line(board, diag1, dr, dc) and no_adjacent_in_line(board, diag2, -dr, -dc):
                        board[diag1[0]][diag1[1]] = None  # Remove the first diagonal dog
                        board[diag2[0]][diag2[1]] = None  # Remove the second diagonal dog
                        # print("Dogs killed in diagonal!")
                        # gui.draw_board()
            #         else:
            #             print("Cannot kill dogs in diagonal, adjacent dogs in line")
            #     else:
            #         print("No dogs on both sides of the tiger in diagonal")
            # else:
            #     print("Invalid positions for dogs in diagonal")

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
