import copy
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#testing testing

# 1. Game State Representation: 2D list
state = [[' ' for _ in range(3)] for _ in range(3)]
MAX_PLAYER = 'X'
MIN_PLAYER = 'O'
EMPTY_CELL = ' '

def initialize_state():
    """Initializes the game state (board) to empty."""
    global state
    state = [[' ' for _ in range(3)] for _ in range(3)]

def print_state():
    """Prints the current game state (board) to the console."""
    print("--------------")
    for i in range(3):
        print("| ", end="")
        for j in range(3):
            print(state[i][j] + " | ", end="")
        print()
        print("--------------")

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

# 4. max_value(state, depth) Function
def max_value(current_state, depth):
    """Maximizing player's (MAX) value function in Minimax."""
    if is_game_over(current_state) or (depth != -1 and depth == 0):
        return evaluate(current_state)

    max_eval = -float('inf')
    for move in get_valid_moves(current_state):
        next_state = copy_state(current_state)
        make_move(next_state, move[0], move[1], MAX_PLAYER)
        #depth handling not ideal maybe should change
        next_depth = depth - 1 if depth != -1 else depth
        eval_score = min_value(next_state, next_depth)
        max_eval = max(max_eval, eval_score)
    return max_eval

# 5. min_value(state, depth) Function
def min_value(current_state, depth):
    """Minimizing player's (MIN) value function in Minimax."""
    if is_game_over(current_state) or (depth != -1 and depth == 0):
        return evaluate(current_state)

    min_eval = float('inf')
    for move in get_valid_moves(current_state):
        next_state = copy_state(current_state)
        make_move(next_state, move[0], move[1], MIN_PLAYER)
        next_depth = depth - 1 if depth != -1 else depth
        eval_score = max_value(next_state, next_depth)
        min_eval = min(min_eval, eval_score)
    return min_eval

# 6. Get Best Move Function
def find_best_move(current_state, depth):
    """Finds the best move for MAX player using Minimax."""
    best_move_row = -1
    best_move_col = -1
    max_eval = -float('inf')

    for move in get_valid_moves(current_state):
        next_state = copy_state(current_state)
        make_move(next_state, move[0], move[1], MAX_PLAYER)
        next_depth = depth - 1 if depth != -1 else depth
        eval_score = min_value(next_state, next_depth) # MIN's response to MAX's move

        if eval_score > max_eval:
            max_eval = eval_score
            best_move_row = move[0]
            best_move_col = move[1]

    return [best_move_row, best_move_col]

# Helper function to copy the state state (for minimax simulation)
def copy_state(current_state):
    """Creates a deep copy of the game state."""
    return copy.deepcopy(current_state)

# Basic Game Loop
if __name__ == "__main__":
    initialize_state()
    current_player = MAX_PLAYER
    depth = 3
    root = tk.Tk()
    root.title("Tic Tac Toe")
    start_screen = tk.Frame(root)
    game_screen = tk.Frame(root)

    for frame in (start_screen, game_screen):
        frame.grid(row=0, column=0, sticky='nsew')

    depth_var = tk.StringVar(value="3")
    first_player_var = tk.StringVar(value="computer")

    def start_game():
        global depth
        depth = int(depth_var.get())
        first_player = first_player_var.get()
        if first_player == "computer":
            print("Computer (X) will make the first move.")
            current_player = MAX_PLAYER
            current_player_label.config(text="Computer's turn")
            play_computer_turn()
        else:
            print("You (O) will make the first move.")
            current_player = MIN_PLAYER
            current_player_label.config(text="Your turn")
        
        game_screen.tkraise()

        

    def gui_game_complete():
        if is_game_over(state):
            print("Game is over")
            score = evaluate(state)
            for row in buttons:
                for button in row:
                    if button is not None:
                        button.config(state=tk.DISABLED)
            if score == 10:
                print("Computer (MAX - X) wins!")
                current_player_label.config(text="Computer wins!")
            elif score == -10:
                print("You (MIN - O) win!")
                current_player_label.config(text="You win!")
            else:
                print("It's a draw!")
                current_player_label.config(text="It's a draw!")
            return True
        else:
            return False
    
    def on_method_change(event=None):
        selected_method = method_var.get()
        if selected_method == "Depth Limited":
            depth_var.set("3")
            difficulty_frame.pack(after=method_dropdown, pady=5)
        else:
            depth_var.set("-1")
            difficulty_frame.pack_forget()
            


    # Start screen
    welcome_label = tk.Label(start_screen, text="Tic Tac Toe", font=("Helvetica", 14))
    welcome_label.pack(pady=10)

    # Search method selection
    method_var = tk.StringVar()
    method_label = tk.Label(start_screen, text="Choose Search Method:")
    method_label.pack()

    method_dropdown = ttk.Combobox(start_screen, textvariable=method_var, state="readonly")
    method_dropdown['values'] = ("Depth Limited", "Complete")
    method_dropdown.current(0)
    method_dropdown.pack(pady=5)
    method_dropdown.bind("<<ComboboxSelected>>", on_method_change)

    difficulty_frame = tk.Frame(start_screen)
    difficulty_label = tk.Label(difficulty_frame, text="Set difficulty (depth):")
    difficulty_label.pack()
    difficulty_entry = tk.Entry(difficulty_frame, textvariable=depth_var)
    difficulty_entry.pack(pady=5)

    difficulty_frame.pack(after=method_dropdown, pady=5)

    first_player_label = tk.Label(start_screen, text="Who plays first?")
    first_player_label.pack()
    tk.Radiobutton(start_screen, text="Computer (X)", variable=first_player_var, value="computer").pack()
    tk.Radiobutton(start_screen, text="You (O)", variable=first_player_var, value="human").pack()

    start_button = tk.Button(start_screen, text="Start Game", command=start_game)
    start_button.pack(pady=20)

    # Game screen
    current_player_label = tk.Label(game_screen, text="", font=("Helvetica", 14))
    current_player_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))
    buttons = [[None for _ in range(len(state))] for _ in range(len(state))]

    def play_computer_turn():
        current_player_label.config(text="Thinking...")
        best_move = find_best_move(state, depth)
        make_move(state, best_move[0], best_move[1], MAX_PLAYER)
        buttons[best_move[0]][best_move[1]].config(text="X")
        buttons[best_move[0]][best_move[1]].config(state=tk.DISABLED)
        if gui_game_complete() == False:
            current_player = MIN_PLAYER
            current_player_label.config(text="Your turn")
        

    def on_button_click(row, col):
        #Perform user turn
        make_move(state, row, col, MIN_PLAYER)
        buttons[row][col].config(text="O")
        buttons[row][col].config(state=tk.DISABLED)
        if gui_game_complete() == False:
            current_player = MAX_PLAYER
            current_player_label.config(text="Computer's turn")
            play_computer_turn()

    for i in range(len(state)):
        for j in range(len(state)):
            btn = tk.Button(
                game_screen,
                text="",
                font=("Helvetica", 24),
                width=4,
                height=2,
                command=lambda row=i, col=j: on_button_click(row, col)
            )
            btn.grid(row=i+1, column=j, padx=5, pady=5)
            buttons[i][j] = btn


    start_screen.tkraise()
    root.mainloop()