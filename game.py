from settings import BOARD_SIZE, DOGS_REQUIRED_TO_WIN
from tkinter import messagebox

tiger_pos = (2, 2)
dogs_killed = 0
turn = 'tiger'

def init_state():
    return [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def get_turn():
    return turn

def get_tiger_pos():
    return tiger_pos

def check_win_conditions(gui):
        if dogs_killed >= DOGS_REQUIRED_TO_WIN:
            messagebox.showinfo("Game Over", "Tiger wins!")
            gui.root.quit()

        # Check if tiger is trapped
        r, c = tiger_pos
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if is_valid_pos(nr, nc) and gui.board[nr][nc] is None:
                    return
        messagebox.showinfo("Game Over", "Dogs win!")
        gui.root.quit()

def handle_tiger_turn(gui, row, col):
    global tiger_pos, turn
    tr, tc = tiger_pos
    if abs(tr - row) <= 1 and abs(tc - col) <= 1 and gui.board[row][col] is None:
        gui.board[tr][tc] = None
        tiger_pos = (row, col)
        try_kill_dogs(gui)
        turn = 'dog'
        gui.update_current_player_label()  # Update the label
        gui.draw_board()
        check_win_conditions(gui)

def handle_dog_turn(gui, row, col):
    if gui.selected:
        sr, sc = gui.selected
        if abs(sr - row) <= 1 and abs(sc - col) <= 1 and gui.board[row][col] is None:
            gui.board[row][col] = 'dog'
            gui.board[sr][sc] = None
            gui.selected = None
            global turn
            turn = 'tiger'
            gui.update_current_player_label()  # Update the label
            gui.draw_board()
            gui.highlight_selected()
            check_win_conditions(gui)
    elif gui.board[row][col] == 'dog':
        gui.selected = (row, col)
        gui.draw_board()
        gui.highlight_selected()

def try_kill_dogs(gui):
        r, c = tiger_pos
        global dogs_killed
        print(f"Checking for dogs to kill at position: {r}, {c}")

        # Check if there is a dog on both sides of the tiger in the same row
        left = c - 1
        right = c + 1
        if is_valid_pos(r, left) and is_valid_pos(r, right):  # Ensure positions are valid
            if gui.board[r][left] == 'dog' and gui.board[r][right] == 'dog':  # Dogs on both sides
                # Ensure no adjacent dogs to the left and right dogs
                if no_adjacent_in_line(gui, (r, left), 0, -1) and no_adjacent_in_line(gui, (r, right), 0, 1):
                    gui.board[r][left] = None  # Remove the left dog
                    gui.board[r][right] = None  # Remove the right dog
                    dogs_killed += 2  # Increment the count of killed dogs
                    print("Dogs killed in row!")
                    gui.draw_board()
                else:
                    print("Cannot kill dogs in row, adjacent dogs in line")
            else:
                print("No dogs on both sides of the tiger in row")
        else:
            print("Invalid positions for dogs in row")

        # Check if there is a dog on both sides of the tiger in the same column
        up = r - 1
        down = r + 1
        if is_valid_pos(up, c) and is_valid_pos(down, c):  # Ensure positions are valid
            if gui.board[up][c] == 'dog' and gui.board[down][c] == 'dog':  # Dogs above and below
                # Ensure no adjacent dogs to the above and below dogs
                if no_adjacent_in_line(gui, (up, c), -1, 0) and no_adjacent_in_line(gui, (down, c), 1, 0):
                    gui.board[up][c] = None  # Remove the upper dog
                    gui.board[down][c] = None  # Remove the lower dog
                    dogs_killed += 2  # Increment the count of killed dogs
                    print("Dogs killed in column!")
                    gui.draw_board()
                else:
                    print("Cannot kill dogs in column, adjacent dogs in line")
            else:
                print("No dogs on both sides of the tiger in column")
        else:
            print("Invalid positions for dogs in column")

        # Check if there is a dog on both sides of the tiger in the diagonals
        diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in diagonals:
            diag1 = (r + dr, c + dc)
            diag2 = (r - dr, c - dc)
            if is_valid_pos(*diag1) and is_valid_pos(*diag2):  # Ensure positions are valid
                if gui.board[diag1[0]][diag1[1]] == 'dog' and gui.board[diag2[0]][diag2[1]] == 'dog':  # Dogs on both diagonals
                    # Ensure no adjacent dogs to the diagonal dogs
                    if no_adjacent_in_line(gui, diag1, dr, dc) and no_adjacent_in_line(gui, diag2, -dr, -dc):
                        gui.board[diag1[0]][diag1[1]] = None  # Remove the first diagonal dog
                        gui.board[diag2[0]][diag2[1]] = None  # Remove the second diagonal dog
                        dogs_killed += 2  # Increment the count of killed dogs
                        print("Dogs killed in diagonal!")
                        gui.draw_board()
                    else:
                        print("Cannot kill dogs in diagonal, adjacent dogs in line")
                else:
                    print("No dogs on both sides of the tiger in diagonal")
            else:
                print("Invalid positions for dogs in diagonal")

def no_adjacent_in_line(gui, pos, dr, dc):
    r, c = pos
    adj1 = (r + dr, c + dc)
    adj2 = (r - dr, c - dc)
    for ar, ac in [adj1, adj2]:
        if is_valid_pos(ar, ac) and gui.board[ar][ac] == 'dog':
            return False
    return True

def is_valid_pos(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE
