import tkinter as tk
from tkinter import messagebox, ttk
import random
import threading

# === Nim Game Logic ===
class NimGame:
    def __init__(self, heaps=[1, 3, 5, 7]):
        self.initial_heaps = heaps[:]
        self.reset()

    def reset(self):
        self.heaps = self.initial_heaps[:]
        self.current_player = "Human"
        self.game_over = False
        self.winner = None

    def is_game_over(self):
        return all(h == 0 for h in self.heaps)

    def make_move(self, heap_index, count):
        if 0 <= heap_index < len(self.heaps) and 1 <= count <= self.heaps[heap_index]:
            self.heaps[heap_index] -= count
            
            if self.is_game_over():
                self.game_over = True
                self.winner = "AI" if self.current_player == "Human" else "Human"
            return True
        return False

    def switch_player(self):
        self.current_player = "AI" if self.current_player == "Human" else "Human"

# === AI Player Logic ===
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

def evaluate(state, maximizing):
    return -1 if is_terminal(state) and maximizing else 1 if is_terminal(state) else 0

# Combined AI function with algorithm selection
def ai_search(state, algorithm, depth=3):
    # Helper functions for the search algorithms
    def minimax(state, maximizing, current_depth, max_depth=20):
        if is_terminal(state) or current_depth >= max_depth:
            return evaluate(state, maximizing), None

        best_value = float('-inf') if maximizing else float('inf')
        best_move = None
        moves = get_valid_moves(state)
        
        for move in moves:
            new_state = apply_move(state, move)
            val, _ = minimax(new_state, not maximizing, current_depth + 1, max_depth)

            if (maximizing and val > best_value) or (not maximizing and val < best_value):
                best_value = val
                best_move = move

        return best_value, best_move
    
    def alphabeta(state, maximizing, alpha, beta, current_depth, max_depth=20):
        if is_terminal(state) or current_depth >= max_depth:
            return evaluate(state, maximizing), None

        best_move = None

        if maximizing:
            value = float('-inf')
            for move in get_valid_moves(state):
                new_state = apply_move(state, move)
                eval_val, _ = alphabeta(new_state, False, alpha, beta, current_depth + 1, max_depth)
                if eval_val > value:
                    value = eval_val
                    best_move = move
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        else:
            value = float('inf')
            for move in get_valid_moves(state):
                new_state = apply_move(state, move)
                eval_val, _ = alphabeta(new_state, True, alpha, beta, current_depth + 1, max_depth)
                if eval_val < value:
                    value = eval_val
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break

        return value, best_move
    
    # Select algorithm based on input parameter
    if algorithm == "Minimaxcomplete":
        return minimax(state, True, 0, 20)[1]
    elif algorithm == "ABcomplete":
        return alphabeta(state, True, float('-inf'), float('inf'), 0, 20)[1]
    elif algorithm == "Minimaxlimited":
        return minimax(state, True, 0, depth)[1]
    elif algorithm == "ABlimited":
        return alphabeta(state, True, float('-inf'), float('inf'), 0, depth)[1]
    
    # Fallback to random move
    valid_moves = get_valid_moves(state)
    return random.choice(valid_moves) if valid_moves else None

# === GUI ===
class NimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nim Game")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.game = NimGame()
        self.ai_thinking = False
        
        # Game configuration variables
        self.algo_var = tk.StringVar(value="ABlimited")
        self.depth_var = tk.IntVar(value=3)
        self.first_player = tk.StringVar(value="Human")
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
        self.stick_buttons = []
        self.update_game_display()

    def setup_ui(self):
        # Algorithm and game settings
        top_frame = tk.Frame(self.config_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(top_frame, text="Algorithm:").pack(side=tk.LEFT, padx=5)
        tk.OptionMenu(top_frame, self.algo_var, 
                     "Minimaxcomplete", "ABcomplete", "Minimaxlimited", "ABlimited").pack(side=tk.LEFT, padx=5)
        
        tk.Label(top_frame, text="Depth:").pack(side=tk.LEFT, padx=5)
        tk.Entry(top_frame, textvariable=self.depth_var, width=3).pack(side=tk.LEFT, padx=5)
        
        tk.Label(top_frame, text="First Player:").pack(side=tk.LEFT, padx=5)
        tk.OptionMenu(top_frame, self.first_player, "Human", "AI").pack(side=tk.LEFT, padx=5)
        
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
        self.status_label = tk.Label(self.status_frame, text="Welcome to Nim!", font=('Arial', 14))
        self.instruction_label = tk.Label(self.status_frame, 
                                         text="Instructions: Click on a stick to remove it and all sticks to its right.",
                                         font=('Arial', 10), fg="blue")
        self.ai_thinking_label = tk.Label(self.status_frame, text="", font=('Arial', 12), fg="green")
        
        self.status_label.pack(pady=5)
        self.instruction_label.pack(pady=2)
        self.ai_thinking_label.pack(pady=5)
        
        # Initialize heap entries
        self.update_heap_entries()

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
        self.update_game_display()
        
        if self.first_player.get() == "AI":
            self.game.current_player = "AI"
            self.status_label.config(text="AI's Turn")
            self.root.update()
            self.root.after(100, self.ai_move_threaded)

    def update_game_display(self):
        # Clear existing game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        self.stick_buttons = []
        
        for i, heap_size in enumerate(self.game.heaps):
            if heap_size == 0:
                self.stick_buttons.append([])
                continue
                
            row_frame = tk.Frame(self.game_frame)
            row_frame.pack(pady=5, anchor=tk.CENTER)
            
            tk.Label(row_frame, text=f"Row {i+1}:", font=('Arial', 10), width=6, anchor=tk.E).pack(side=tk.LEFT, padx=(0, 10))
            
            sticks_frame = tk.Frame(row_frame)
            sticks_frame.pack(side=tk.LEFT)
            
            row_buttons = []
            for j in range(heap_size):
                sticks_to_remove = heap_size - j
                btn = tk.Button(
                    sticks_frame, 
                    text="▲", 
                    bg="brown", 
                    fg="white",
                    font=('Arial', 12), 
                    width=2,
                    command=lambda heap=i, count=sticks_to_remove: self.human_move(heap, count)
                )
                btn.grid(row=0, column=j, padx=1)
                self.create_tooltip(btn, f"Remove {sticks_to_remove} stick(s)")
                row_buttons.append(btn)
            
            self.stick_buttons.append(row_buttons)
            tk.Label(row_frame, text="Click a stick to remove it and all sticks to its right", 
                    font=('Arial', 8), fg="gray").pack(side=tk.LEFT, padx=10)

    def create_tooltip(self, widget, text):
        widget.bind("<Enter>", lambda event, t=text: self.show_tooltip(event, t))
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event, text):
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 20
        
        self.tooltip = tk.Toplevel(event.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()

    def human_move(self, heap, count):
        if self.game.current_player != "Human" or self.ai_thinking:
            return
            
        if not self.game.make_move(heap, count):
            messagebox.showerror("Invalid Move", "Try another move")
            return
            
        self.post_move()

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
        
        self.root.after(500, lambda: self.execute_ai_move(move))

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
        else:
            self.game.switch_player()
            self.status_label.config(text=f"{self.game.current_player}'s Turn")
            
            if self.game.current_player == "AI" and not self.ai_thinking:
                self.root.after(500, self.ai_move_threaded)

    def on_closing(self):
        self.ai_thinking = False
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = NimGUI(root)
    root.geometry("600x600")
    root.mainloop()