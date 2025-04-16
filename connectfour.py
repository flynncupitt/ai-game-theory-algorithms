import tkinter as tk
from tkinter import messagebox
import random
import copy
import time

class ConnectFour:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.current_player = 1

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
        self.root.title("Connect Four")
        self.rows = 6
        self.cols = 7
        self.depth = 4
        self.first_player = "Random"
        self.ai_algo = "Minimaxcomplete"
        self.game = ConnectFour(self.rows, self.cols)
        self.board_canvas = None
        self.status_label = None
        self.setup_screen()
        self.root.geometry(f"{self.cols * 100 + 20}x{self.rows * 100 + 100}")

    def setup_screen(self):
        self.status_label = tk.Label(self.root, text="Game initialized.")
        self.status_label.pack()
        tk.Label(self.root, text="Choose First Player").pack()
        self.first_var = tk.StringVar(value="Random")
        tk.OptionMenu(self.root, self.first_var, "Random", "AI").pack()

        tk.Label(self.root, text="Choose AI Algorithm").pack()
        self.algo_var = tk.StringVar(value="Minimaxcomplete")
        tk.OptionMenu(self.root, self.algo_var, "Minimaxcomplete", "ABcomplete", "Minimaxlimited", "ABlimited").pack()

        tk.Label(self.root, text="AI Search Depth (for limited only)").pack()
        self.depth_entry = tk.Entry(self.root)
        self.depth_entry.insert(0, "4")
        self.depth_entry.pack()

        tk.Label(self.root, text="Rows").pack()
        self.row_entry = tk.Entry(self.root)
        self.row_entry.insert(0, "6")
        self.row_entry.pack()

        tk.Label(self.root, text="Columns").pack()
        self.col_entry = tk.Entry(self.root)
        self.col_entry.insert(0, "7")
        self.col_entry.pack()

        tk.Button(self.root, text="Start Game", command=self.start_game).pack()

        self.root.mainloop()

    def start_game(self):
        self.rows = int(self.row_entry.get())
        self.cols = int(self.col_entry.get())
        self.depth = int(self.depth_entry.get())
        self.first_player = self.first_var.get()  # Get the selected first player
        self.ai_algo = self.algo_var.get()

        # Destroy any existing board elements
        if self.board_canvas:
            self.board_canvas.destroy()
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Play Again":
                widget.destroy()
            if isinstance(widget, tk.Label) and widget.cget("text").startswith("Game Over"):
                widget.destroy()

        self.game = ConnectFour(self.rows, self.cols)
        # Create the board_canvas here, before calling update_canvas
        self.board_canvas = tk.Canvas(self.root, width=self.cols * 100, height=self.rows * 100, bg="blue")
        self.board_canvas.pack()
        self.update_canvas()

        if self.first_player == "AI":
            self.status_label.config(text="Game started. AI's (Yellow) turn.")
            self.game.current_player = 2  # AI goes first (Yellow)
            self.root.after(500, self.play_turn)
        elif self.first_player == "Random":
            if random.choice([True, False]):
                self.status_label.config(text="Game started. AI's (Yellow) turn.")
                self.game.current_player = 2  # AI goes first (Yellow)
                self.root.after(500, self.play_turn)
            else:
                self.status_label.config(text="Game started. Random player's (Red) turn.")
                self.game.current_player = 1  # Human goes first (Red)
                # Human's move will be triggered by clicking the canvas (to be implemented)
        else:  # Default to Human (Red) if something goes wrong
            self.status_label.config(text="Game started. Random player's (Red) turn.")
            self.game.current_player = 1

    def update_canvas(self):
        self.board_canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * 100 + 5, r * 100 + 5
                x2, y2 = x1 + 90, y1 + 90
                color = "white"
                if self.game.board[r][c] == 1:
                    color = "red"
                elif self.game.board[r][c] == 2:
                    color = "yellow"
                self.board_canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black")
        self.root.update()

    def play_turn(self):
        winner = self.game.check_winner()
        if winner != 0:
            winner_name = ""
            if self.first_player == "Random":
                winner_name = "Random player" if winner == 1 else "AI player"
            else:  # self.first_player == "AI"
                winner_name = "AI player" if winner == 1 else "Random player" # Assuming AI is player 2

            messagebox.showinfo("Game Over", f"{winner_name} wins!")
            self.status_label.config(text=f"Game Over: {winner_name} wins!")
            reset_button = tk.Button(self.root, text="Play Again", command=self.reset_game)
            reset_button.pack()
            return
        elif self.game.is_full():
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.status_label.config(text="Game Over: Draw!")
            reset_button = tk.Button(self.root, text="Play Again", command=self.reset_game)
            reset_button.pack()
            return

        if (self.game.current_player == 1 and self.first_player == "Random") or \
           (self.game.current_player == 2 and self.first_player == "AI"):
            move = random.choice(self.game.valid_moves())
        else:
            move = self.get_ai_move()

        self.game.make_move(move)
        self.update_canvas()
        self.game.switch_player()
        self.root.after(500, self.play_turn)

    def reset_game(self):
        self.game = ConnectFour(self.rows, self.cols)
        self.update_canvas()
        # Destroy the "Play Again" button if it exists
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Play Again":
                widget.destroy()
        self.status_label.config(text="Game started. Red's turn.")
        if self.first_player == "AI" and self.game.current_player == 2:
            self.root.after(500, self.play_turn)
        elif self.first_player == "Random" and self.game.current_player == 2: # If AI starts randomly
            self.root.after(500, self.play_turn)

    def get_ai_move(self):
        algo = self.ai_algo
        ai_player = self.game.current_player
        if algo == "Minimaxcomplete":
            move, _ = minimax(self.game.clone(), True, ai_player)
        elif algo == "ABcomplete":
            move, _ = alphabeta(self.game.clone(), True, float('-inf'), float('inf'), ai_player)
        elif algo == "Minimaxlimited":
            move, _ = minimax_limited(self.game.clone(), self.depth, True, ai_player)
        elif algo == "ABlimited":
            move, _ = alphabeta_limited(self.game.clone(), self.depth, True, float('-inf'), float('inf'), ai_player)
        else:
            move = random.choice(self.game.valid_moves())
        return move


def evaluate(board: ConnectFour, player):
    """Simple evaluation function for depth-limited search."""
    opponent = 3 - player
    score = 0

    def count_patterns(token, length):
        count = 0
        for r in range(board.rows):
            for c in range(board.cols - length + 1):
                line = [board.board[r][c + i] for i in range(length)]
                if line.count(token) == length and line.count(0) == 0:
                    count += 1
        for c in range(board.cols):
            for r in range(board.rows - length + 1):
                line = [board.board[r + i][c] for i in range(length)]
                if line.count(token) == length and line.count(0) == 0:
                    count += 1
        return count

    score += count_patterns(player, 2) * 1
    score += count_patterns(player, 3) * 10
    score += count_patterns(player, 4) * 1000
    score -= count_patterns(opponent, 3) * 10
    score -= count_patterns(opponent, 4) * 1000

    return score

def minimax(board: ConnectFour, maximizing, player):
    winner = board.check_winner()
    if winner == player:
        return (None, float('inf'))
    elif winner == 3 - player:
        return (None, float('-inf'))
    elif board.is_full():
        return (None, 0)

    best_move = None
    best_score = float('-inf') if maximizing else float('inf')
    for move in board.valid_moves():
        child = board.clone()
        child.make_move(move)
        child.switch_player()
        _, score = minimax(child, not maximizing, player)
        if maximizing and score > best_score:
            best_score = score
            best_move = move
        elif not maximizing and score < best_score:
            best_score = score
            best_move = move
    return best_move, best_score

def alphabeta(board: ConnectFour, maximizing, alpha, beta, player):
    winner = board.check_winner()
    if winner == player:
        return (None, float('inf'))
    elif winner == 3 - player:
        return (None, float('-inf'))
    elif board.is_full():
        return (None, 0)

    best_move = None
    if maximizing:
        best_score = float('-inf')
        for move in board.valid_moves():
            child = board.clone()
            child.make_move(move)
            child.switch_player()
            _, score = alphabeta(child, False, alpha, beta, player)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break
    else:
        best_score = float('inf')
        for move in board.valid_moves():
            child = board.clone()
            child.make_move(move)
            child.switch_player()
            _, score = alphabeta(child, True, alpha, beta, player)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break
    return best_move, best_score

def minimax_limited(board: ConnectFour, depth, maximizing, player):
    winner = board.check_winner()
    if winner == player:
        return (None, float('inf'))
    elif winner == 3 - player:
        return (None, float('-inf'))
    elif board.is_full() or depth == 0:
        return (None, evaluate(board, player))

    best_move = None
    best_score = float('-inf') if maximizing else float('inf')
    for move in board.valid_moves():
        child = board.clone()
        child.make_move(move)
        child.switch_player()
        _, score = minimax_limited(child, depth - 1, not maximizing, player)
        if maximizing and score > best_score:
            best_score = score
            best_move = move
        elif not maximizing and score < best_score:
            best_score = score
            best_move = move
    return best_move, best_score

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
        return (None, evaluate(board, player))  # Handle no valid moves

    best_move = None
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
            alpha = max(alpha, score)
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
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_move, best_score

if __name__ == "__main__":
    gui = ConnectFourGUI()
    
    
    
            
    
    

