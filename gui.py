import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from alpha_beta import AlphaBeta
from game import initialize_state, is_game_over, evaluate, make_move
from minimax import Minimax

if __name__ == "__main__":
    state = initialize_state()
    ai = Minimax()
    depth = 3
    root = tk.Tk()
    root.title("Tic Tac Toe")
    start_screen = tk.Frame(root)
    game_screen = tk.Frame(root)
    MAX_PLAYER = 'X'
    MIN_PLAYER = 'O'
    EMPTY_CELL = ' '


    for frame in (start_screen, game_screen):
        frame.grid(row=0, column=0, sticky='nsew')

    depth_var = tk.StringVar(value="3")
    first_player_var = tk.StringVar(value="computer")

    def start_game():
        global depth
        global ai
        depth = int(depth_var.get())
        first_player = first_player_var.get()
        if first_player == "computer":
            print("Computer (X) will make the first move.")
            current_player_label.config(text="Computer's turn")
            play_computer_turn()
        else:
            print("You (O) will make the first move.")
            current_player_label.config(text="Your turn")
        
        if algorithm_var.get() == 'alpha_beta':
            print("alpha beta chosen")
            ai = AlphaBeta()

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
 
    def play_computer_turn():
        current_player_label.config(text="Thinking...")
        best_move = ai.find_best_move(state, depth)
        make_move(state, best_move[0], best_move[1], MAX_PLAYER)
        buttons[best_move[0]][best_move[1]].config(text="X")
        buttons[best_move[0]][best_move[1]].config(state=tk.DISABLED)
        if gui_game_complete() == False:
            current_player_label.config(text="Your turn")
        

    def on_button_click(row, col):
        #Perform user turn
        make_move(state, row, col, MIN_PLAYER)
        buttons[row][col].config(text="O")
        buttons[row][col].config(state=tk.DISABLED)
        if gui_game_complete() == False:
            current_player_label.config(text="Computer's turn")
            play_computer_turn()

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

    # Algorithm selection
    algorithm_var = tk.StringVar(value="minimax")  # Default selection

    algorithm_label = tk.Label(start_screen, text="Choose Algorithm:")
    algorithm_label.pack(pady=(10, 0))

    tk.Radiobutton(start_screen, text="Minimax", variable=algorithm_var, value="minimax").pack()
    tk.Radiobutton(start_screen, text="Alpha-Beta Pruning", variable=algorithm_var, value="alpha_beta").pack()

    start_button = tk.Button(start_screen, text="Start Game", command=start_game)
    start_button.pack(pady=20)

    # Game screen
    current_player_label = tk.Label(game_screen, text="", font=("Helvetica", 14))
    current_player_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))
    buttons = [[None for _ in range(len(state))] for _ in range(len(state))]

    
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