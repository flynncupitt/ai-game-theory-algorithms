
# 1. Game State Representation: 2D list
MAX_PLAYER = 'X'
MIN_PLAYER = 'O'
EMPTY_CELL = ' '

def initialize_state():
    return [[' ' for _ in range(3)] for _ in range(3)]

# 2. Move Generation Function
def get_valid_moves(current_state):
    """Returns a list of valid moves (empty cell coordinates) in the current state."""
    valid_moves = []
    for i in range(3):
        for j in range(3):
            if current_state[i][j] == EMPTY_CELL:
                valid_moves.append([i, j])
    return valid_moves

def is_valid_move(current_state, row, col):
    """Checks if a move (row, col) is valid in the current state."""
    return 0 <= row < 3 and 0 <= col < 3 and current_state[row][col] == EMPTY_CELL

def make_move(current_state, row, col, player):
    """Makes a move on the state if it is valid."""
    if is_valid_move(current_state, row, col):
        current_state[row][col] = player

# 3. Evaluation Function
def evaluate(current_state):
    """Evaluates the current game state and returns a score."""
    # Check rows, columns, and diagonals for wins
    for i in range(3):
        if current_state[i][0] == current_state[i][1] == current_state[i][2]:
            if current_state[i][0] == MAX_PLAYER:
                return 10
            if current_state[i][0] == MIN_PLAYER:
                return -10
        if current_state[0][i] == current_state[1][i] == current_state[2][i]:
            if current_state[0][i] == MAX_PLAYER:
                return 10
            if current_state[0][i] == MIN_PLAYER:
                return -10
    if current_state[0][0] == current_state[1][1] == current_state[2][2]:
        if current_state[0][0] == MAX_PLAYER:
            return 10
        if current_state[0][0] == MIN_PLAYER:
            return -10
    if current_state[0][2] == current_state[1][1] == current_state[2][0]:
        if current_state[0][2] == MAX_PLAYER:
            return 10
        if current_state[0][2] == MIN_PLAYER:
            return -10
    return 0  # No winner yet or draw (handled in is_game_over)

def is_game_over(current_state):
    """Checks if the game is over (win or draw)."""
    return not get_valid_moves(current_state) or abs(evaluate(current_state)) == 10
