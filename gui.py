import random
import time
import tkinter as tk
from tkinter import messagebox
from alpha_beta import AlphaBeta
from minimax import Minimax
from game_setup import GameSetup
from settings import BOARD_SIZE, TILE_SIZE, DOGS_REQUIRED_TO_WIN
from game import count_dogs_killed, evaluate, find_tiger, init_state, get_turn, set_turn, try_kill_dogs

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=BOARD_SIZE*TILE_SIZE, height=BOARD_SIZE*TILE_SIZE)
        self.canvas.pack()

        self.current_player_label = tk.Label(root, text="Current Player: Tiger (Thinking...)", font=("Arial", 14))
        self.current_player_label.pack()
        self.dogs_killed_label = tk.Label(root, text=f"Dogs killed: 0/{DOGS_REQUIRED_TO_WIN}", font=("Arial", 14))
        self.dogs_killed_label.pack()

        self.board = init_state()
        self.draw_board()
        self.selected = None
        self.ai = Minimax(self)
        self.depth = 3

    # Redraws the board when needed
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

            self.draw_piece(*find_tiger(self.board), 'white')

    # Helper function for drawing pieces on the board
    def draw_piece(self, row, col, color):
        x = col * TILE_SIZE + TILE_SIZE // 2
        y = row * TILE_SIZE + TILE_SIZE // 2
        r = TILE_SIZE // 3
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="black")

    # Updates label when turn changes
    def update_current_player_label(self):
        if get_turn() == 'tiger':
            self.current_player_label.config(text="Current Player: Tiger (Thinking...)")
        else:
            self.current_player_label.config(text="Current Player: Dog")

    # Handles move making on given board for players
    def make_move(self, board_state, row, col, player, chosenDog=None):
        if player == 'tiger':
            tr, tc = find_tiger(board_state)
            board_state[tr][tc] = None
            board_state[row][col] = 'tiger'
            try_kill_dogs(board_state)
            set_turn('dog')
        elif player == 'dog':
            if board_state[row][col] is None:
                if chosenDog is not None:
                    board_state[chosenDog[0]][chosenDog[1]] = None
                board_state[row][col] = 'dog'
                set_turn('tiger')
    
    # Handles tiger's turn and GUI updates
    def play_tiger_turn(self):
        root.update()
        time.sleep(0.3)
        best_move = self.ai.find_best_move(self.depth)
        self.make_move(self.board, best_move[0], best_move[1], 'tiger')
        dogs_killed = count_dogs_killed(self.board)
        self.dogs_killed_label.config(text=f"Dogs killed: {dogs_killed}/{DOGS_REQUIRED_TO_WIN}")
        if evaluate(self.board) == 10:
                    messagebox.showinfo("Game Over", "Tiger wins!")
                    self.root.quit()
        else:
            self.update_current_player_label()
            self.draw_board()
            self.play_dog_turn(self.board)

    # Handles dog's turn and GUI updates
    def play_dog_turn(self, board_state):
        root.update()
        time.sleep(0.7)
        valid_dog_moves = self.ai.get_valid_moves(board_state, 'dog')
        if not valid_dog_moves:
            messagebox.showinfo("Error", "No remaining dog moves!")
            self.root.quit()
            return
        
        #Choose random dog from available dogs to make move
        random_dog = random.choice(list(valid_dog_moves.keys()))
        random_move = random.choice(valid_dog_moves[random_dog])
        self.make_move(board_state, random_move[0], random_move[1], 'dog', random_dog)

        if evaluate(board_state) == -10:
            messagebox.showinfo("Game Over", "Dogs wins!")
            self.root.quit()
        set_turn('tiger')
        self.update_current_player_label()
        self.draw_board()
        root.update()
        self.play_tiger_turn()

# Starts the game with the given settings    
def start_game_with_settings(settings):
    game = GameGUI(root)
    center = BOARD_SIZE // 2
    game.board = [['dog' if i == 0 or i == BOARD_SIZE - 1 or j == 0 or j == BOARD_SIZE - 1 else None
                   for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    game.board[center][center] = 'tiger'
    game.draw_board()

    if settings['algorithm'] == "Minimax":
        game.ai = Minimax(game)
    else:
        game.ai = AlphaBeta(game)

    if settings['search_method'] == "Depth Limited":
        game.depth = settings['difficulty']
    else:
        game.depth = -1

    if settings['first_player'] == "Tiger":
        root.after(500, game.play_tiger_turn)
    else:
         root.after(500, lambda: game.play_dog_turn(game.board))

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    def show_main_window(settings):
        root.deiconify()
        start_game_with_settings(settings)

    setup_screen = GameSetup(root, start_callback=show_main_window)
    root.mainloop()
