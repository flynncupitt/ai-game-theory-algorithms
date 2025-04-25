import tkinter as tk
from minimax import Minimax
from settings import BOARD_SIZE, TILE_SIZE
from game import get_tiger_pos, init_state, get_turn, set_tiger_pos, set_turn, try_kill_dogs
class GameGUI:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=BOARD_SIZE*TILE_SIZE, height=BOARD_SIZE*TILE_SIZE)
        self.canvas.pack()

        # Add a label to display the current player
        self.current_player_label = tk.Label(root, text="Current Player: Tiger", font=("Arial", 14))
        self.current_player_label.pack()

        self.board = init_state()
        # self.tiger_pos = (2, 2)
        # self.dogs_killed = 0
        # self.turn = 'tiger'
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

            self.draw_piece(*get_tiger_pos(), 'white')

    def draw_piece(self, row, col, color):
        x = col * TILE_SIZE + TILE_SIZE // 2
        y = row * TILE_SIZE + TILE_SIZE // 2
        r = TILE_SIZE // 3
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="black")
    
    def highlight_selected(self):
        if get_turn() == 'tiger':  # Automatically highlight the tiger when it's the tiger's turn
            print("Highlighting tiger position", get_tiger_pos())
            tr, tc = get_tiger_pos()
            x0 = tc * TILE_SIZE
            y0 = tr * TILE_SIZE
            x1 = x0 + TILE_SIZE
            y1 = y0 + TILE_SIZE
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", width=3)
        elif self.selected:  # Highlight the selected dog when it's the dog's turn
            sr, sc = self.selected
            x0 = sc * TILE_SIZE
            y0 = sr * TILE_SIZE
            x1 = x0 + TILE_SIZE
            y1 = y0 + TILE_SIZE
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", width=3)

    def update_current_player_label(self):
        """Update the label to show the current player."""
        if get_turn() == 'tiger':
            self.current_player_label.config(text="Current Player: Tiger")
        else:
            self.current_player_label.config(text="Current Player: Dog")
   
    def handle_click(self, event):
        row = event.y // TILE_SIZE
        col = event.x // TILE_SIZE

        if get_turn() == 'tiger':
            self.handle_tiger_turn(self.board, row, col)
        else:
            self.handle_dog_turn(self.board, row, col)
    #need to track killed dogs
    def make_move(self, board_state, row, col, player, chosenDog=None):
        if player == 'tiger':
            # self.handle_tiger_turn(board_state, row, col)
            tr, tc = get_tiger_pos()
            board_state[tr][tc] = None
            board_state[row][col] = 'tiger'
            set_tiger_pos((row, col))
            try_kill_dogs(board_state)
            set_turn('dog')
            
        elif player == 'dog' and chosenDog:
            # self.handle_dog_turn(board_state, row, col)
            sr, sc = chosenDog
            board_state[row][col] = 'dog'
            board_state[sr][sc] = None
            self.selected = None
            set_turn('tiger')

# DO NEXT: pass killed dogs var to make_move, but turn handlers need to reflect in gui for NON SIMULATED moves
    # def handle_tiger_turn(self, board_state, row, col):
    #     print("playing tiger turn")
    #     tr, tc = get_tiger_pos()
    #     if abs(tr - row) <= 1 and abs(tc - col) <= 1 and board_state[row][col] is None:
    #         board_state[tr][tc] = None
    #         board_state[row][col] = 'tiger' #should mean tiger move saved to board
    #         set_tiger_pos((row, col))
    #         print("New tiger position:", get_tiger_pos())
    #         try_kill_dogs(board_state)
    #         set_turn('dog')  # Switch turn to dog
    #         self.update_current_player_label()  # Update the label
    #         self.draw_board()
    #         #check_win_conditions(self)

    # def handle_dog_turn(self, board_state, row, col):
    #     print("playing dog turn")
    #     if self.selected:
    #         sr, sc = self.selected
    #         if abs(sr - row) <= 1 and abs(sc - col) <= 1 and board_state[row][col] is None:
    #             board_state[row][col] = 'dog'
    #             board_state[sr][sc] = None
    #             self.selected = None
    #             set_turn('tiger')
    #             self.update_current_player_label()  # Update the label
    #             self.draw_board()
    #             self.highlight_selected()
    #             #check_win_conditions(self)
    #     elif board_state[row][col] == 'dog':
    #         self.selected = (row, col)
    #         self.draw_board()
    #         self.highlight_selected()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Tiger vs Dogs")
    game = GameGUI(root)
    state = game.board
    minimax = Minimax(game)
    # Initialize board: place tiger in center, dogs around edges
    center = BOARD_SIZE // 2
    game.board = [['dog' if i == 0 or i == BOARD_SIZE - 1 or j == 0 or j == BOARD_SIZE - 1 else None
                for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    game.board[center][center] = 'tiger'
    game.draw_board()
    game.highlight_selected()
    best_move = minimax.find_best_move(4)
    print("Best move for Tiger:", best_move)  # Example usage of Minimax
    root.mainloop()