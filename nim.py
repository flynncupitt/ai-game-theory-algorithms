import tkinter as tk
from tkinter import messagebox
import random
import copy

# === Nim Game Logic ===
class NimGame:
    def __init__(self, heaps=[1, 3, 5, 7]):
        self.initial_heaps = heaps[:]
        self.heaps = heaps[:]
        self.current_player = "Human"

    def reset(self):
        self.heaps = self.initial_heaps[:]
        self.current_player = "Human"

    def is_game_over(self):
        return all(h == 0 for h in self.heaps)

    def make_move(self, heap_index, count):
        if 0 <= heap_index < len(self.heaps) and 1 <= count <= self.heaps[heap_index]:
            self.heaps[heap_index] -= count
            return True
        return False

    def get_valid_moves(self):
        moves = []
        for i, heap in enumerate(self.heaps):
            for j in range(1, heap + 1):
                moves.append((i, j))
        return moves

# === AI Player ===
def is_terminal(state):
    return all(h == 0 for h in state)

def evaluate(state):
    return -1 if is_terminal(state) else 0

# --- Minimax (Complete) ---
def minimax_complete(state, maximizing):
    if is_terminal(state):
        return (-1 if maximizing else 1), None

    best_value = float('-inf') if maximizing else float('inf')
    best_move = None

    for move in get_valid_moves(state):
        new_state = apply_move(state, move)
        val, _ = minimax_complete(new_state, not maximizing)

        if maximizing and val > best_value:
            best_value = val
            best_move = move
        elif not maximizing and val < best_value:
            best_value = val
            best_move = move

    return best_value, best_move

# --- Alpha-Beta Pruning (Complete) ---
def alphabeta_complete(state, maximizing, alpha, beta):
    if is_terminal(state):
        return (-1 if maximizing else 1), None

    best_move = None

    if maximizing:
        value = float('-inf')
        for move in get_valid_moves(state):
            new_state = apply_move(state, move)
            eval, _ = alphabeta_complete(new_state, False, alpha, beta)
            if eval > value:
                value = eval
                best_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
    else:
        value = float('inf')
        for move in get_valid_moves(state):
            new_state = apply_move(state, move)
            eval, _ = alphabeta_complete(new_state, True, alpha, beta)
            if eval < value:
                value = eval
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break

    return value, best_move

# --- Minimax Limited Depth ---
def minimax_limited(state, maximizing, depth):
    if depth == 0 or is_terminal(state):
        return evaluate(state), None

    best_value = float('-inf') if maximizing else float('inf')
    best_move = None

    for move in get_valid_moves(state):
        new_state = apply_move(state, move)
        val, _ = minimax_limited(new_state, not maximizing, depth - 1)

        if maximizing and val > best_value:
            best_value = val
            best_move = move
        elif not maximizing and val < best_value:
            best_value = val
            best_move = move

    return best_value, best_move

# --- Alpha-Beta Limited Depth ---
def alphabeta_limited(state, maximizing, alpha, beta, depth):
    if depth == 0 or is_terminal(state):
        return evaluate(state), None

    best_move = None

    if maximizing:
        value = float('-inf')
        for move in get_valid_moves(state):
            new_state = apply_move(state, move)
            eval, _ = alphabeta_limited(new_state, False, alpha, beta, depth - 1)
            if eval > value:
                value = eval
                best_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
    else:
        value = float('inf')
        for move in get_valid_moves(state):
            new_state = apply_move(state, move)
            eval, _ = alphabeta_limited(new_state, True, alpha, beta, depth - 1)
            if eval < value:
                value = eval
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break

    return value, best_move

# === Helper Functions ===
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

# === GUI ===
class NimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nim Game")
        self.game = NimGame()

        self.algo_var = tk.StringVar(value="Minimaxcomplete")
        self.depth_var = tk.IntVar(value=3)
        self.first_player = tk.StringVar(value="Human")

        self.setup_menu()
        self.status_label = tk.Label(root, text="Welcome to Nim!", font=('Arial', 14))
        self.status_label.pack(pady=10)
        self.buttons = []
        self.draw_game()

    def setup_menu(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text="Algorithm:").grid(row=0, column=0)
        tk.OptionMenu(frame, self.algo_var, "Minimaxcomplete", "ABcomplete", "Minimaxlimited", "ABlimited").grid(row=0, column=1)

        tk.Label(frame, text="Depth:").grid(row=0, column=2)
        tk.Entry(frame, textvariable=self.depth_var, width=3).grid(row=0, column=3)

        tk.Label(frame, text="First Player:").grid(row=0, column=4)
        tk.OptionMenu(frame, self.first_player, "Human", "AI").grid(row=0, column=5)

        tk.Button(frame, text="Start Game", command=self.start_game).grid(row=0, column=6)

    def start_game(self):
        self.game.reset()
        self.draw_game()
        if self.first_player.get() == "AI":
            self.root.after(500, self.ai_move)

    def draw_game(self):
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()

        for i, heap in enumerate(self.game.heaps):
            row = tk.Frame(self.root)
            row.pack()
            for j in range(heap):
                btn = tk.Button(row, text="|", command=lambda i=i, j=j: self.human_move(i, j + 1))
                btn.pack(side=tk.LEFT)
                self.buttons.append(btn)

    def human_move(self, heap, count):
        if not self.game.make_move(heap, count):
            messagebox.showerror("Invalid Move", "Try another move")
            return
        self.post_move()
        self.root.after(500, self.ai_move)

    def ai_move(self):
        state = self.game.heaps[:]
        algorithm = self.algo_var.get()

        if algorithm == "Minimaxcomplete":
            _, move = minimax_complete(state, True)
        elif algorithm == "ABcomplete":
            _, move = alphabeta_complete(state, True, float('-inf'), float('inf'))
        elif algorithm == "Minimaxlimited":
            _, move = minimax_limited(state, True, self.depth_var.get())
        elif algorithm == "ABlimited":
            _, move = alphabeta_limited(state, True, float('-inf'), float('inf'), self.depth_var.get())
        else:
            move = random.choice(get_valid_moves(state))

        if move:
            self.game.make_move(*move)
            self.post_move()

    def post_move(self):
        self.draw_game()
        if self.game.is_game_over():
            winner = "AI" if self.game.current_player == "Human" else "Human"
            messagebox.showinfo("Game Over", f"{winner} wins!")
        else:
            self.game.current_player = "AI" if self.game.current_player == "Human" else "Human"
            self.status_label.config(text=f"{self.game.current_player}'s Turn")

if __name__ == '__main__':
    root = tk.Tk()
    app = NimGUI(root)
    root.mainloop()
