import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 5
TILE_SIZE = 100
DOGS_REQUIRED_TO_WIN = 6

class TigerVsDogs:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=BOARD_SIZE*TILE_SIZE, height=BOARD_SIZE*TILE_SIZE)
        self.canvas.pack()

        # Add a label to display the current player
        self.current_player_label = tk.Label(root, text="Current Player: Tiger", font=("Arial", 14))
        self.current_player_label.pack()

        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.tiger_pos = (2, 2)
        self.dogs_killed = 0
        self.turn = 'tiger'

        self.draw_board()
        self.canvas.bind('<Button-1>', self.handle_click)

        self.selected = None

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x0 = j * TILE_SIZE
                y0 = i * TILE_SIZE
                x1 = x0 + TILE_SIZE
                y1 = y0 + TILE_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="lightyellow", outline="black")

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 'dog':
                    self.draw_piece(i, j, 'black')

        self.draw_piece(*self.tiger_pos, 'white')

    def draw_piece(self, row, col, color):
        x = col * TILE_SIZE + TILE_SIZE // 2
        y = row * TILE_SIZE + TILE_SIZE // 2
        r = TILE_SIZE // 3
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="black")

    def handle_click(self, event):
        row = event.y // TILE_SIZE
        col = event.x // TILE_SIZE

        if self.turn == 'tiger':
            self.handle_tiger_turn(row, col)
        else:
            self.handle_dog_turn(row, col)

    def handle_tiger_turn(self, row, col):
        tr, tc = self.tiger_pos
        if abs(tr - row) <= 1 and abs(tc - col) <= 1 and self.board[row][col] is None:
            self.board[tr][tc] = None
            self.tiger_pos = (row, col)
            self.try_kill_dogs()
            self.turn = 'dog'
            self.update_current_player_label()  # Update the label
            self.draw_board()
            self.check_win_conditions()

    def handle_dog_turn(self, row, col):
        if self.selected:
            sr, sc = self.selected
            if abs(sr - row) <= 1 and abs(sc - col) <= 1 and self.board[row][col] is None:
                self.board[row][col] = 'dog'
                self.board[sr][sc] = None
                self.selected = None
                self.turn = 'tiger'
                self.update_current_player_label()  # Update the label
                self.draw_board()
                self.check_win_conditions()
        elif self.board[row][col] == 'dog':
            self.selected = (row, col)
            self.draw_board()
            self.highlight_selected()

    def highlight_selected(self):
        if self.selected:
            sr, sc = self.selected
            x0 = sc * TILE_SIZE
            y0 = sr * TILE_SIZE
            x1 = x0 + TILE_SIZE
            y1 = y0 + TILE_SIZE
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", width=3)

    def try_kill_dogs(self):
        r, c = self.tiger_pos
        print(f"Checking for dogs to kill at position: {r}, {c}")

        # Check if there is a dog on both sides of the tiger in the same row
        left = c - 1
        right = c + 1

        if self.is_valid_pos(r, left) and self.is_valid_pos(r, right):  # Ensure positions are valid
            if self.board[r][left] == 'dog' and self.board[r][right] == 'dog':  # Dogs on both sides
                # Ensure no adjacent dogs to the left and right dogs
                if self.no_adjacent_in_line((r, left), 0, -1) and self.no_adjacent_in_line((r, right), 0, 1):
                    self.board[r][left] = None  # Remove the left dog
                    self.board[r][right] = None  # Remove the right dog
                    self.dogs_killed += 2  # Increment the count of killed dogs
                    print("Dogs killed!")
                    self.draw_board()
                else:
                    print("Cannot kill dogs, adjacent dogs in line")
            else:
                print("No dogs on both sides of the tiger")
        else:
            print("Invalid positions for dogs")

    def no_adjacent_in_line(self, pos, dr, dc):
        r, c = pos
        adj1 = (r + dr, c + dc)
        adj2 = (r - dr, c - dc)
        for ar, ac in [adj1, adj2]:
            if self.is_valid_pos(ar, ac) and self.board[ar][ac] == 'dog':
                return False
        return True

    def is_valid_pos(self, r, c):
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    def check_win_conditions(self):
        if self.dogs_killed >= DOGS_REQUIRED_TO_WIN:
            messagebox.showinfo("Game Over", "Tiger wins!")
            self.root.quit()

        # Check if tiger is trapped
        r, c = self.tiger_pos
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.is_valid_pos(nr, nc) and self.board[nr][nc] is None:
                    return
        messagebox.showinfo("Game Over", "Dogs win!")
        self.root.quit()

    def update_current_player_label(self):
        """Update the label to show the current player."""
        if self.turn == 'tiger':
            self.current_player_label.config(text="Current Player: Tiger")
        else:
            self.current_player_label.config(text="Current Player: Dog")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Tiger vs Dogs")
    game = TigerVsDogs(root)

    # Initialize board: place tiger in center, dogs around edges
    center = BOARD_SIZE // 2
    game.board = [['dog' if i == 0 or i == BOARD_SIZE - 1 or j == 0 or j == BOARD_SIZE - 1 else None
                   for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    game.board[center][center] = 'tiger'
    game.tiger_pos = (center, center)
    game.draw_board()

    root.mainloop()
