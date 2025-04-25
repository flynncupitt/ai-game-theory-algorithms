import tkinter as tk
from tkinter import messagebox, ttk
import random
import copy
import time

class ConnectFour:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.current_player = 1  # 1 for Human (Red), 2 for AI (Yellow)

    def make_move(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return True
        return False

    def valid_moves(self):
        return [c for c in range(self.cols) if self.board[0][c] == 0]

    def switch_player(self):
        self.current_player = 3 - self.current_player

    #AI has helped generate this check_winner function to check for win conditions in all possible directions
    def check_winner(self):
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if self.line_check(r, c, 0, 1):
                    return self.board[r][c]
        for r in range(self.rows - 3):
            for c in range(self.cols):
                if self.line_check(r, c, 1, 0):
                    return self.board[r][c]
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if self.line_check(r, c, 1, 1):
                    return self.board[r][c]
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if self.line_check(r, c, -1, 1):
                    return self.board[r][c]
        return 0

    def line_check(self, r, c, dr, dc):
        token = self.board[r][c]
        if token == 0:
            return False
        for i in range(1, 4):
            if self.board[r + i * dr][c + i * dc] != token:
                return False
        return True

    def is_full(self):
        return all(self.board[0][c] != 0 for c in range(self.cols))

    def clone(self):
        clone = ConnectFour(self.rows, self.cols)
        clone.board = copy.deepcopy(self.board)
        clone.current_player = self.current_player
        return clone

class ConnectFourGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect Four AI vs Human")
        
        # Board size presets
        self.board_sizes = {
            "Standard": (6, 7),     
            "Medium": (8, 9),    
            "Large": (10, 11),   
            "Extra Large": (12, 13)     
        }
        
        # Current board size
        self.board_size = "Standard"
        self.rows, self.cols = self.board_sizes[self.board_size]
        
        # Dictionary mapping difficulty levels to search depths
        self.difficulty_depths = {
            "Easy": 2,
            "Medium": 4,
            "Hard": 6,
            "Expert": 8
        }
        self.difficulty = "Medium"  # Default difficulty
        
        self.human_player = 1   # Human is Red (1)
        self.ai_player = 2      # AI is Yellow (2)
        self.first_player = "Human"
        self.ai_algo = "Minimaxcomplete"
        self.game = ConnectFour(self.rows, self.cols)
        self.game_speed = 1000  # Milliseconds between moves
        self.game_active = False
        self.waiting_for_human = False  # Flag to indicate we're waiting for human input
        
        self.board_canvas = None
        self.status_label = None
        self.setup_screen()
        
    def setup_screen(self):
        # Create a main frame for all controls
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Game initialized.", font=("Arial", 12))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left frame for controls
        controls_frame = tk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, padx=10, sticky="n")
        
        # First player selection
        tk.Label(controls_frame, text="Choose First Player").pack(pady=(0, 5))
        self.first_var = tk.StringVar(value="Human")
        tk.OptionMenu(controls_frame, self.first_var, "Human", "AI").pack(pady=(0, 10), fill="x")
        
        # AI Algorithm selection
        tk.Label(controls_frame, text="Choose AI Algorithm").pack(pady=(0, 5))
        self.algo_var = tk.StringVar(value="Minimaxcomplete")
        tk.OptionMenu(controls_frame, self.algo_var, "Minimaxcomplete", "ABcomplete", "Minimaxlimited", "ABlimited").pack(pady=(0, 10), fill="x")
        
        # Difficulty selection
        tk.Label(controls_frame, text="Difficulty").pack(pady=(0, 5))
        self.difficulty_var = tk.StringVar(value="Easy")
        difficulty_combobox = ttk.Combobox(controls_frame, textvariable=self.difficulty_var, 
                                          values=list(self.difficulty_depths.keys()),
                                          state="readonly")
        difficulty_combobox.pack(pady=(0, 10), fill="x")
        
        # Board size selection
        tk.Label(controls_frame, text="Board Size").pack(pady=(0, 5))
        self.size_var = tk.StringVar(value="Standard")
        size_combobox = ttk.Combobox(controls_frame, textvariable=self.size_var, 
                                    values=list(self.board_sizes.keys()),
                                    state="readonly")
        size_combobox.pack(pady=(0, 10), fill="x")
                
        # Start/Stop game buttons
        self.start_button = tk.Button(controls_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=(10, 5), fill="x")
        
        self.stop_button = tk.Button(controls_frame, text="Stop Game", command=self.stop_game)
        self.stop_button.pack(pady=(5, 10), fill="x")
        self.stop_button.config(state=tk.DISABLED)
        
        # Create frame for the game board
        self.board_frame = tk.Frame(main_frame)
        self.board_frame.grid(row=1, column=1, padx=10, pady=10)
        
        # Set initial window size
        self.root.geometry(f"{900}x{600}")
        
    def start_game(self):
        # Update configuration from inputs
        self.board_size = self.size_var.get()
        self.rows, self.cols = self.board_sizes[self.board_size]
        self.difficulty = self.difficulty_var.get()
        self.first_player = self.first_var.get()
        self.ai_algo = self.algo_var.get()
    
        # Update button states
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.game_active = True
    
        # Destroy any existing board elements
        if self.board_canvas:
            self.board_canvas.destroy()
    
        # Remove any game over elements
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        # Create a new game
        self.game = ConnectFour(self.rows, self.cols)
    
        # Create the board canvas
        canvas_width = min(600, self.cols * 80)
        canvas_height = min(500, self.rows * 80)
    
        self.board_canvas = tk.Canvas(
            self.board_frame, 
            width=canvas_width,
            height=canvas_height, 
            bg="blue"
        )
        self.board_canvas.pack()
    
        # Force an update to ensure the canvas is drawn
        self.root.update_idletasks()
    
        # Set up click handlers for human player
        self.board_canvas.bind("<Button-1>", self.handle_click)
    
        # Determine who goes first
        if self.first_player == "AI":
            self.game.current_player = self.ai_player  # AI is Yellow (2)
            self.waiting_for_human = False
            self.status_label.config(text="Game started. AI's turn (Yellow).")
        else:  # Human
            self.game.current_player = self.human_player  # Human goes first (Red)
            self.waiting_for_human = True
            self.status_label.config(text="Game started. Human player's turn (Red).")
    
        self.update_canvas()
    
        # Start the game loop
        self.play_turn()
        
    def stop_game(self):
        self.game_active = False
        self.waiting_for_human = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Game stopped.")
        
    def handle_click(self, event):
        if not self.game_active or not self.waiting_for_human:
            return
            
        # Convert click to column
        canvas_width = self.board_canvas.winfo_width()
        cell_width = canvas_width / self.cols
        col = int(event.x / cell_width)
        
        # Make sure the column is valid
        if col >= 0 and col < self.cols and col in self.game.valid_moves():
            self.game.make_move(col)
            self.update_canvas()
            self.status_label.config(text=f"You placed in column {col+1}")
            
            # Switch to AI player
            self.game.switch_player()
            self.waiting_for_human = False
            
            # Check if game is over after human move
            if self.check_game_over():
                return
                
            # AI's turn
            self.status_label.config(text="AI player's turn (Yellow)...")
            self.root.after(500, self.play_turn)  # Short delay before AI move
        else:
            self.status_label.config(text="Invalid move! Select another column.")
    
    def check_game_over(self):
        winner = self.game.check_winner()
        if winner != 0:
            winner_name = "Human player (Red)" if winner == self.human_player else "AI player (Yellow)"
            messagebox.showinfo("Game Over", f"{winner_name} wins!")
            self.status_label.config(text=f"Game Over: {winner_name} wins!")
            self.game_active = False
            self.waiting_for_human = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            return True
        elif self.game.is_full():
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.status_label.config(text="Game Over: Draw!")
            self.game_active = False
            self.waiting_for_human = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            return True
        return False
    
    def play_turn(self):
        if not self.game_active:
            return
            
        # Check if game is over
        if self.check_game_over():
            return

        # Make a move based on current player
        if self.game.current_player == self.human_player:
            # Human player's turn - wait for their input
            self.waiting_for_human = True
            self.status_label.config(text="Human player's turn (Red). Click a column to place your piece.")
        else:
            # AI player makes a strategic move
            move = self.get_ai_move()
            self.game.make_move(move)
            self.update_canvas()
            self.status_label.config(text=f"AI player (Yellow) placed in column {move+1}")
            
            # Switch to human player
            self.game.switch_player()
            
            # Check if game is over after AI move
            if self.check_game_over():
                return
                
            # Now it's human's turn
            self.waiting_for_human = True
            self.status_label.config(text="Human player's turn (Red). Click a column to place your piece.")
    
    def update_canvas(self):
        self.board_canvas.delete("all")
    
        # Get the actual canvas dimensions, or use the intended dimensions if not yet available
        canvas_width = self.board_canvas.winfo_width()
        canvas_height = self.board_canvas.winfo_height()
    
        # If the canvas hasn't been fully rendered yet, use the intended dimensions
        if canvas_width <= 1:
            canvas_width = min(600, self.cols * 80)
        if canvas_height <= 1:
            canvas_height = min(500, self.rows * 80)

        cell_width = canvas_width / self.cols
        cell_height = canvas_height / self.rows

        # First draw the blue background
        self.board_canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill="blue")

        # Then draw the white circles (empty slots) or colored circles (tokens)
        for r in range(self.rows):
            for c in range(self.cols):
                # Calculate center position for each circle
                x_center = c * cell_width + cell_width/2
                y_center = r * cell_height + cell_height/2
                radius = min(cell_width, cell_height) * 0.4  # Size that fits within cell

                # Determine token color
                token = self.game.board[r][c]
                if token == 1:
                    color = "red"
                elif token == 2:
                    color = "yellow"
                else:
                    color = "white"

                # Draw the circle
                self.board_canvas.create_oval(
                    x_center - radius, 
                    y_center - radius, 
                    x_center + radius, 
                    y_center + radius, 
                    fill=color, 
                    outline="black"
                )
    
    def get_ai_move(self):
        # Get the current difficulty depth
        depth = self.difficulty_depths[self.difficulty]
        
        # Choose AI algorithm based on selection
        algo = self.ai_algo
        ai_player = self.ai_player
        
        if algo == "Minimaxcomplete":
            # Use depth for complete search too, but limit it to prevent hanging
            actual_depth = min(depth, 5)  # Limit depth for complete search
            move, _ = minimax_limited(self.game.clone(), actual_depth, True, ai_player)
        elif algo == "ABcomplete":
            # Use depth for complete search too, but limit it to prevent hanging
            actual_depth = min(depth, 5)  # Limit depth for complete search
            move, _ = alphabeta_limited(self.game.clone(), actual_depth, True, float('-inf'), float('inf'), ai_player)
        elif algo == "Minimaxlimited":
            move, _ = minimax_limited(self.game.clone(), depth, True, ai_player)
        elif algo == "ABlimited":
            move, _ = alphabeta_limited(self.game.clone(), depth, True, float('-inf'), float('inf'), ai_player)
        else:
            move = random.choice(self.game.valid_moves())
            
        return move

#Ai has helped complete this evaluate function which is used to score non-terminal board positions by considering mutiple strategic factors
def evaluate(board: ConnectFour, player):
    """Evaluation function for depth-limited search."""
    opponent = 3 - player
    score = 0
    
    # Check for immediate win/loss (highest priority)
    winner = board.check_winner()
    if winner == player:
        return float('inf')
    elif winner == opponent:
        return float('-inf')
    
    # Center column control (good strategy in Connect Four)
    center_col = board.cols // 2
    center_count = 0
    for r in range(board.rows):
        if board.board[r][center_col] == player:
            center_count += 1
    score += center_count * 3
    
    # Count different patterns
    def count_patterns(token, length, empty_count):
        """Count patterns with 'length' tokens and 'empty_count' empty spaces"""
        count = 0
        
        # Horizontal patterns
        for r in range(board.rows):
            for c in range(board.cols - length + 1):
                line = [board.board[r][c + i] for i in range(length)]
                if line.count(token) == length - empty_count and line.count(0) == empty_count and line.count(3 - token) == 0:
                    count += 1
        
        # Vertical patterns
        for c in range(board.cols):
            for r in range(board.rows - length + 1):
                line = [board.board[r + i][c] for i in range(length)]
                if line.count(token) == length - empty_count and line.count(0) == empty_count and line.count(3 - token) == 0:
                    count += 1
        
        # Diagonal patterns (down-right)
        for r in range(board.rows - length + 1):
            for c in range(board.cols - length + 1):
                line = [board.board[r + i][c + i] for i in range(length)]
                if line.count(token) == length - empty_count and line.count(0) == empty_count and line.count(3 - token) == 0:
                    count += 1
        
        # Diagonal patterns (up-right)
        for r in range(length - 1, board.rows):
            for c in range(board.cols - length + 1):
                line = [board.board[r - i][c + i] for i in range(length)]
                if line.count(token) == length - empty_count and line.count(0) == empty_count and line.count(3 - token) == 0:
                    count += 1
                    
        return count
    
    # Score for different patterns (weighted by how close to winning)
    score += count_patterns(player, 4, 0) * 1000  # Four in a row (win)
    score += count_patterns(player, 4, 1) * 50    # Three in a row with an empty space
    score += count_patterns(player, 3, 0) * 10    # Three in a row
    score += count_patterns(player, 2, 0) * 1     # Two in a row
    
    # Subtract opponent's threats
    score -= count_patterns(opponent, 4, 0) * 1000  # Block opponent win
    score -= count_patterns(opponent, 4, 1) * 80    # Block opponent three in a row with empty
    score -= count_patterns(opponent, 3, 0) * 15    # Block opponent three in a row
    
    return score
#AI has helped to complete this minimax_limited function
def minimax_limited(board: ConnectFour, depth, maximizing, player):
    winner = board.check_winner()
    if winner == player:
        return (None, float('inf'))
    elif winner == 3 - player:
        return (None, float('-inf'))
    elif board.is_full() or depth == 0:
        return (None, evaluate(board, player))

    valid_moves = board.valid_moves()
    if not valid_moves:
        return (None, evaluate(board, player))
        
    # Sort moves to check center columns first (better pruning)
    center_col = board.cols // 2
    valid_moves.sort(key=lambda x: -abs(x - center_col))
    
    best_move = valid_moves[0]  # Default to first move
    
    if maximizing:
        best_score = float('-inf')
        for move in valid_moves:
            child = board.clone()
            child.make_move(move)
            child.switch_player()
            _, score = minimax_limited(child, depth - 1, False, player)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move, best_score
    else:
        best_score = float('inf')
        for move in valid_moves:
            child = board.clone()
            child.make_move(move)
            child.switch_player()
            _, score = minimax_limited(child, depth - 1, True, player)
            if score < best_score:
                best_score = score
                best_move = move
        return best_move, best_score

#AI has helped to complete this alpha_limited function
def alphabeta_limited(board: ConnectFour, depth, maximizing, alpha, beta, player):
    winner = board.check_winner()
    if winner == player:
        return (None, float('inf'))
    elif winner == 3 - player:
        return (None, float('-inf'))
    elif board.is_full() or depth == 0:
        return (None, evaluate(board, player))

    valid_moves = board.valid_moves()
    if not valid_moves:
        return (None, evaluate(board, player))
    
    # Sort moves to check center columns first (better pruning)
    center_col = board.cols // 2
    valid_moves.sort(key=lambda x: -abs(x - center_col))
    
    best_move = valid_moves[0]  # Default to first move
    
    if maximizing:
        best_score = float('-inf')
        for move in valid_moves:
            child = board.clone()
            child.make_move(move)
            child.switch_player()
            _, score = alphabeta_limited(child, depth - 1, False, alpha, beta, player)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_move, best_score
    else:
        best_score = float('inf')
        for move in valid_moves:
            child = board.clone()
            child.make_move(move)
            child.switch_player()
            _, score = alphabeta_limited(child, depth - 1, True, alpha, beta, player)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_move, best_score

def main():
    gui = ConnectFourGUI()
    gui.root.mainloop()

if __name__ == "__main__":
    main()