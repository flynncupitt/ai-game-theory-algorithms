import tkinter as tk
from tkinter import messagebox, ttk
import random
import threading
import time

# === Nim Game Logic ===
class NimGame:
    def __init__(self, heaps=[1, 3, 5, 7]):
        self.initial_heaps = heaps[:]
        self.reset()

    def reset(self):
        self.heaps = self.initial_heaps[:]
        self.current_player = "AI"  # Changed default to AI
        self.game_over = False
        self.winner = None

    def is_game_over(self):
        return all(h == 0 for h in self.heaps)

    def make_move(self, heap_index, count):
        if 0 <= heap_index < len(self.heaps) and 1 <= count <= self.heaps[heap_index]:
            self.heaps[heap_index] -= count
            
            if self.is_game_over():
                self.game_over = True
                self.winner = "Random Human" if self.current_player == "AI" else "AI"
            return True
        return False

    def switch_player(self):
        self.current_player = "Random Human" if self.current_player == "AI" else "AI"


# === Move Generation and Game State Logic ===
def get_valid_moves(state):
    moves = []
    for i, heap in enumerate(state):
        for j in range(1, heap + 1):
            moves.append((i, j))
    return moves

def apply_move(state, move):
    i, count = move
    new_state = state[:]
    new_state[i] -= count
    return new_state

def is_terminal(state):
    return all(h == 0 for h in state)

def nim_sum(state):
    """Calculate the nim-sum (XOR of all heap sizes) of the state"""
    result = 0
    for heap in state:
        result ^= heap
    return result

# === Random Human Player Logic ===
def random_human_move(state):
    """Generate a random move for the human player"""
    valid_moves = get_valid_moves(state)
    if valid_moves:
        return random.choice(valid_moves)
    return None

def is_misere_winning(state):
    non_empty = [h for h in state if h > 0]
    if all(h == 1 for h in non_empty):
        return len(non_empty) % 2 == 0
    else:
        return nim_sum(state) != 0

# === AI Player Logic ===
def ai_search(state, algorithm, depth=3):
    """AI search with different algorithms"""
    
    def evaluate(state):
        """Evaluate the state from AI's perspective"""
        return 100 if is_misere_winning else -100
    
    # Complete Minimax (no depth limit)
    def minimaxcomplete(state, is_ai_turn):
        if is_terminal(state):
            # In misère Nim, if terminal state, current player loses
            return -100 if is_ai_turn else 100, None

        valid_moves = get_valid_moves(state)
        if not valid_moves:
            return evaluate(state, is_ai_turn), None
            
        if is_ai_turn:  # AI is maximizing
            best_value = float('-inf')
            best_move = None
            for move in valid_moves:
                new_state = apply_move(state, move)
                value, _ = minimaxcomplete(new_state, False)  # Switch to opponent's turn
                if value > best_value:
                    best_value = value
                    best_move = move
            return best_value, best_move
        else:  # Opponent is minimizing
            best_value = float('inf')
            best_move = None
            for move in valid_moves:
                new_state = apply_move(state, move)
                value, _ = minimaxcomplete(new_state, True)  # Switch back to AI's turn
                if value < best_value:
                    best_value = value
                    best_move = move
            return best_value, best_move
    
    # Complete Alpha-Beta (no depth limit)
    def alphabetacomplete(state, is_ai_turn, alpha=float('-inf'), beta=float('inf')):
        if is_terminal(state):
            return -100 if is_ai_turn else 100, None

        valid_moves = get_valid_moves(state)
        if not valid_moves:
            return evaluate(state, is_ai_turn), None
            
        best_move = None

        if is_ai_turn:  # AI is maximizing
            value = float('-inf')
            for move in valid_moves:
                new_state = apply_move(state, move)
                eval_val, _ = alphabetacomplete(new_state, False, alpha, beta)
                if eval_val > value:
                    value = eval_val
                    best_move = move
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        else:  # Opponent is minimizing
            value = float('inf')
            for move in valid_moves:
                new_state = apply_move(state, move)
                eval_val, _ = alphabetacomplete(new_state, True, alpha, beta)
                if eval_val < value:
                    value = eval_val
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break

        return value, best_move
    
    # Depth-limited Minimax
    def minimaxlimited(state, is_ai_turn, current_depth, max_depth):
        if is_terminal(state) or current_depth >= max_depth:
            return evaluate(state), None

        valid_moves = get_valid_moves(state)
        if not valid_moves:
            return evaluate(state), None
            
        if is_ai_turn:  # AI is maximizing
            best_value = float('-inf')
            best_move = None
            for move in valid_moves:
                new_state = apply_move(state, move)
                value, _ = minimaxlimited(new_state, False, current_depth + 1, max_depth)
                if value > best_value:
                    best_value = value
                    best_move = move
            return best_value, best_move
        else:  # Opponent is minimizing
            best_value = float('inf')
            best_move = None
            for move in valid_moves:
                new_state = apply_move(state, move)
                value, _ = minimaxlimited(new_state, True, current_depth + 1, max_depth)
                if value < best_value:
                    best_value = value
                    best_move = move
            return best_value, best_move
    
    # Depth-limited Alpha-Beta
    def alphabetalimited(state, is_ai_turn, alpha, beta, current_depth, max_depth):
        if is_terminal(state) or current_depth >= max_depth:
            return evaluate(state), None

        valid_moves = get_valid_moves(state)
        if not valid_moves:
            return evaluate(state), None
            
        best_move = None

        if is_ai_turn:  # AI is maximizing
            value = float('-inf')
            for move in valid_moves:
                new_state = apply_move(state, move)
                eval_val, _ = alphabetalimited(new_state, False, alpha, beta, current_depth + 1, max_depth)
                if eval_val > value:
                    value = eval_val
                    best_move = move
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        else:  # Opponent is minimizing
            value = float('inf')
            for move in valid_moves:
                new_state = apply_move(state, move)
                eval_val, _ = alphabetalimited(new_state, True, alpha, beta, current_depth + 1, max_depth)
                if eval_val < value:
                    value = eval_val
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break

        return value, best_move
    
    # === Select algorithm based on input parameter ===
    if algorithm == "Minimaxcomplete":
        value, move = minimaxcomplete(state, True)
        return move

    elif algorithm == "ABcomplete":
        value, move = alphabetacomplete(state, True)
        return move

    elif algorithm == "Minimaxlimited":
        value, move = minimaxlimited(state, True, 0, depth)
        return move

    elif algorithm == "ABlimited":
        value, move = alphabetalimited(state, True, float('-inf'), float('inf'), 0, depth)
        return move
    
    # Fallback to random move
    import random
    valid_moves = get_valid_moves(state)
    return random.choice(valid_moves) if valid_moves else None

# === GUI ===
class NimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nim Game - AI vs Random Human")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.game = NimGame()
        self.ai_thinking = False
        self.human_thinking = False
        
        # Game configuration variables
        self.algo_var = tk.StringVar(value="ABlimited")
        self.depth_var = tk.IntVar(value=3)
        self.difficulty_label = tk.StringVar(value="Medium")
        self.first_player = tk.StringVar(value="AI")
        self.num_heaps_var = tk.IntVar(value=4)
        self.heap_settings = [] 
        
        # Create frames
        self.config_frame = tk.Frame(self.root, padx=10, pady=10)
        self.status_frame = tk.Frame(self.root, padx=10, pady=5)
        self.game_frame = tk.Frame(self.root, padx=10, pady=10)
        
        self.config_frame.pack(fill=tk.X)
        self.status_frame.pack(fill=tk.X)
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        
        # Setup UI components
        self.setup_ui()
        self.update_game_display()

    def setup_ui(self):
        # Algorithm and game settings
        top_frame = tk.Frame(self.config_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(top_frame, text="AI Algorithm:").pack(side=tk.LEFT, padx=5)
        tk.OptionMenu(top_frame, self.algo_var, 
                     "Minimaxcomplete", "ABcomplete", "Minimaxlimited", "ABlimited").pack(side=tk.LEFT, padx=5)
        
        # Difficulty/depth setting with visual indicator
        tk.Label(top_frame, text="Depth (for limited search):").pack(side=tk.LEFT, padx=5)
        depth_frame = tk.Frame(top_frame)
        depth_frame.pack(side=tk.LEFT, padx=5)
        
        depth_scale = tk.Scale(depth_frame, from_=1, to=10, orient=tk.HORIZONTAL, 
                              variable=self.depth_var, command=self.update_difficulty_label)
        depth_scale.pack(side=tk.TOP)
        
        difficulty_label = tk.Label(depth_frame, textvariable=self.difficulty_label)
        difficulty_label.pack(side=tk.TOP)
        
        tk.Label(top_frame, text="First Player:").pack(side=tk.LEFT, padx=5)
        tk.OptionMenu(top_frame, self.first_player, "AI", "Random Human").pack(side=tk.LEFT, padx=5)
        
        tk.Button(top_frame, text="Start Game", command=self.start_game, 
                 bg="green", fg="white", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=20)

        # Heap configuration
        heap_config_frame = tk.Frame(self.config_frame)
        heap_config_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(heap_config_frame, text="Number of Rows:").pack(side=tk.LEFT, padx=5)
        num_heaps_spinner = tk.Spinbox(heap_config_frame, from_=1, to=10, width=3, 
                                      textvariable=self.num_heaps_var, command=self.update_heap_entries)
        num_heaps_spinner.pack(side=tk.LEFT, padx=5)
        
        self.heap_entry_frame = tk.Frame(self.config_frame)
        self.heap_entry_frame.pack(fill=tk.X, pady=5)
        
        # Status indicators
        self.status_label = tk.Label(self.status_frame, text="Welcome to Nim Game - AI vs Random Human!", font=('Arial', 14))
        self.instruction_label = tk.Label(self.status_frame, 
                                         text="Game is completely automated - watch AI and Random Human play!",
                                         font=('Arial', 10), fg="blue")
        self.ai_thinking_label = tk.Label(self.status_frame, text="", font=('Arial', 12), fg="green")
        self.human_move_label = tk.Label(self.status_frame, text="", font=('Arial', 12), fg="blue")
        
        self.status_label.pack(pady=5)
        self.instruction_label.pack(pady=2)
        self.ai_thinking_label.pack(pady=2)
        self.human_move_label.pack(pady=2)

        self.winning_state_label = tk.Label(self.status_frame, text="", font=('Arial', 10, 'italic'), fg="purple")
        self.winning_state_label.pack(pady=5)
        
        # Initialize heap entries and difficulty label
        self.update_heap_entries()
        self.update_difficulty_label(self.depth_var.get())

    def update_difficulty_label(self, *args):
        depth = self.depth_var.get()
        if depth <= 2:
            self.difficulty_label.set("Easy")
        elif depth <= 5:
            self.difficulty_label.set("Medium")
        elif depth <= 7:
            self.difficulty_label.set("Hard")
        else:
            self.difficulty_label.set("Expert")

    def update_heap_entries(self):
        # Clear existing entries
        for widget in self.heap_entry_frame.winfo_children():
            widget.destroy()
        
        self.heap_settings = []
        num_heaps = self.num_heaps_var.get()
        default_sizes = [2*i + 1 for i in range(num_heaps)]
        
        for i in range(num_heaps):
            frame = tk.Frame(self.heap_entry_frame)
            frame.pack(side=tk.LEFT, padx=5)
            
            tk.Label(frame, text=f"Row {i+1}:").pack()
            heap_var = tk.IntVar(value=default_sizes[i])
            tk.Spinbox(frame, from_=1, to=20, width=3, textvariable=heap_var).pack()
            self.heap_settings.append(heap_var)

    def start_game(self):
        heap_sizes = [var.get() for var in self.heap_settings]
        self.game = NimGame(heap_sizes)
        self.human_move_label.config(text="")
        self.ai_thinking_label.config(text="")
        
        # Set first player
        self.game.current_player = self.first_player.get()
        
        self.update_game_display()
        self.make_next_move()

    def update_game_display(self):
        # Clear existing game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        for i, heap_size in enumerate(self.game.heaps):
            if heap_size == 0:
                continue
                
            row_frame = tk.Frame(self.game_frame)
            row_frame.pack(pady=5, anchor=tk.CENTER)
            
            tk.Label(row_frame, text=f"Row {i+1}:", font=('Arial', 10), width=6, anchor=tk.E).pack(side=tk.LEFT, padx=(0, 10))
            
            sticks_frame = tk.Frame(row_frame)
            sticks_frame.pack(side=tk.LEFT)
            
            for j in range(heap_size):
                stick_label = tk.Label(
                    sticks_frame, 
                    text="|", 
                    bg="brown", 
                    fg="white",
                    font=('Arial', 12), 
                    width=2,
                    padx=1,
                    relief=tk.RAISED
                )
                stick_label.grid(row=0, column=j, padx=1)
            
            tk.Label(row_frame, text=f"{heap_size} sticks", 
                   font=('Arial', 8), fg="gray").pack(side=tk.LEFT, padx=10)
            
        self.update_winning_state()
        self.status_label.config(text=f"{self.game.current_player}'s Turn")

    def make_next_move(self):
        """Determine which player's turn it is and make the appropriate move"""
        if self.game.game_over:
            return
            
        if self.game.current_player == "AI":
            self.root.after(500, self.ai_move_threaded)
        else:  # Random Human's turn
            self.root.after(500, self.human_move_threaded)

    def human_move_threaded(self):
        if self.game.current_player != "Random Human" or self.game.game_over:
            return
            
        self.human_thinking = True
        self.human_move_label.config(text="Random Human is thinking...")
        self.root.update()
        
        # Add small delay for visual effect
        self.root.after(1000, self.execute_human_move)

    def execute_human_move(self):
        move = random_human_move(self.game.heaps[:])
        
        if move:
            heap_index, count = move
            self.game.make_move(heap_index, count)
            self.human_thinking = False
            self.human_move_label.config(text=f"Random Human removed {count} stick(s) from row {heap_index+1}")
            self.post_move()
        else:
            self.human_thinking = False
            self.human_move_label.config(text="Random Human couldn't find a move")

    def ai_move_threaded(self):
        if self.game.current_player != "AI" or self.game.game_over:
            return
            
        self.ai_thinking = True
        self.ai_thinking_label.config(text="AI is thinking...")
        self.root.update()
        
        ai_thread = threading.Thread(target=self.calculate_ai_move)
        ai_thread.daemon = True
        ai_thread.start()

    def calculate_ai_move(self):
        algorithm = self.algo_var.get()
        depth = self.depth_var.get()
        
        try:
            move = ai_search(self.game.heaps[:], algorithm, depth)
        except Exception as e:
            print(f"AI error: {e}")
            valid_moves = get_valid_moves(self.game.heaps[:])
            move = random.choice(valid_moves) if valid_moves else None
        
        # Add a thinking delay for realism
        # Make complete algorithms take longer as they do more computation
        is_complete = "complete" in algorithm
        thinking_time = 1500 if is_complete else 500
        self.root.after(thinking_time, lambda: self.execute_ai_move(move))

    def execute_ai_move(self, move):
        if move:
            heap_index, count = move
            self.game.make_move(heap_index, count)
            self.ai_thinking = False
            self.ai_thinking_label.config(text=f"AI removed {count} stick(s) from row {heap_index+1}")
            self.post_move()
        else:
            self.ai_thinking = False
            self.ai_thinking_label.config(text="AI couldn't find a move")

    def post_move(self):
        self.update_game_display()
        
        if self.game.game_over:
            messagebox.showinfo("Game Over", f"{self.game.winner} wins! The player who took the last stick ({self.game.current_player}) lost.")
            self.status_label.config(text=f"Game Over! {self.game.winner} wins!")
            self.ai_thinking_label.config(text="")
            self.human_move_label.config(text="")
        else:
            self.game.switch_player()
            self.status_label.config(text=f"{self.game.current_player}'s Turn")
            self.make_next_move()

    def update_winning_state(self):
        nimsum = nim_sum(self.game.heaps)
        if nimsum == 0:
            winner = "Random Human" if self.game.current_player == "AI" else "AI"
        else:
            winner = self.game.current_player
        self.winning_state_label.config(text=f"Winning Position: {winner}")

    def on_closing(self):
        self.ai_thinking = False
        self.human_thinking = False
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = NimGUI(root)
    root.geometry("1000x600")
    root.mainloop()