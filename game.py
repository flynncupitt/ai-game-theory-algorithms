# 1. Game State Representation: 2D list
MAX_PLAYER = 'X'
MIN_PLAYER = 'O'
EMPTY_CELL = ' '

game_size = 3  # Size of the Tic-Tac-Toe board

def initialize_state():
    return [[' ' for _ in range(game_size)] for _ in range(game_size)]

# 2. Move Generation Function
def get_valid_moves(current_state):
    """Returns a list of valid moves (empty cell coordinates) in the current state."""
    valid_moves = []
    for i in range(game_size):
        for j in range(game_size):
            if current_state[i][j] == EMPTY_CELL:
                valid_moves.append([i, j])
    return valid_moves

def is_valid_move(current_state, row, col):
    """Checks if a move (row, col) is valid in the current state."""
    return 0 <= row < game_size and 0 <= col < game_size and current_state[row][col] == EMPTY_CELL

def make_move(current_state, row, col, player):
    """Makes a move on the state if it is valid."""
    if is_valid_move(current_state, row, col):
        current_state[row][col] = player

# 3. Evaluation Function
def evaluate(current_state):
    """Evaluates the current game state and returns a score."""
    # Check rows for wins
    for i in range(game_size):
        if all(current_state[i][j] == MAX_PLAYER for j in range(game_size)):
            return 10
        if all(current_state[i][j] == MIN_PLAYER for j in range(game_size)):
            return -10

    # Check columns for wins
    for j in range(game_size):
        if all(current_state[i][j] == MAX_PLAYER for i in range(game_size)):
            return 10
        if all(current_state[i][j] == MIN_PLAYER for i in range(game_size)):
            return -10

    # Check main diagonal for a win
    if all(current_state[i][i] == MAX_PLAYER for i in range(game_size)):
        return 10
    if all(current_state[i][i] == MIN_PLAYER for i in range(game_size)):
        return -10

    # Check anti-diagonal for a win
    if all(current_state[i][game_size - 1 - i] == MAX_PLAYER for i in range(game_size)):
        return 10
    if all(current_state[i][game_size - 1 - i] == MIN_PLAYER for i in range(game_size)):
        return -10

    # No winner yet
    return 0

def is_game_over(current_state):
    """Checks if the game is over (win or draw)."""
    return not get_valid_moves(current_state) or abs(evaluate(current_state)) == 10
