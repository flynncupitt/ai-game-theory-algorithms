import tkinter as tk
from tkinter import ttk

class GameSetup(tk.Toplevel):
    def __init__(self, master, start_callback):
        super().__init__(master)
        self.title("Tiger vs Dogs - Setup")
        self.start_callback = start_callback

        self.search_method = tk.StringVar(value="Depth Limited")
        self.difficulty = tk.StringVar(value="1")
        self.first_player = tk.StringVar(value="Tiger")
        self.algorithm = tk.StringVar(value="Minimax")

        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Tiger vs Dogs", font=("Helvetica", 18, "bold")).pack(pady=10)

        #Search method
        tk.Label(self, text="Search Method:").pack(anchor='w', padx=10)
        search_frame = tk.Frame(self)
        search_frame.pack(anchor='w', padx=20)
        ttk.Radiobutton(search_frame, text="Depth Limited", variable=self.search_method, value="Depth Limited", command=self.toggle_difficulty).pack(side='left')
        ttk.Radiobutton(search_frame, text="Complete", variable=self.search_method, value="Complete", command=self.toggle_difficulty).pack(side='left')

        #Difficulty (only for Depth Limited)
        self.difficulty_frame = tk.Frame(self)
        self.difficulty_frame.pack(anchor='w', padx=20, pady=5)
        tk.Label(self.difficulty_frame, text="Difficulty (Depth):").pack(side='left')
        self.difficulty_entry = tk.Entry(self.difficulty_frame, textvariable=self.difficulty, width=5)
        self.difficulty_entry.pack(side='left')

        #First Player
        tk.Label(self, text="First Player:").pack(anchor='w', padx=10)
        first_player_frame = tk.Frame(self)
        first_player_frame.pack(anchor='w', padx=20)
        ttk.Radiobutton(first_player_frame, text="Tiger", variable=self.first_player, value="Tiger").pack(side='left')
        ttk.Radiobutton(first_player_frame, text="Dogs", variable=self.first_player, value="Dogs").pack(side='left')

        #Algorithm
        tk.Label(self, text="Algorithm:").pack(anchor='w', padx=10)
        algorithm_frame = tk.Frame(self)
        algorithm_frame.pack(anchor='w', padx=20)
        ttk.Radiobutton(algorithm_frame, text="Minimax", variable=self.algorithm, value="Minimax").pack(side='left')
        ttk.Radiobutton(algorithm_frame, text="Alpha-Beta Pruning", variable=self.algorithm, value="Alpha-Beta Pruning").pack(side='left')

        #Start button
        tk.Button(self, text="Start Game", command=self.start_game).pack(pady=20)

        self.toggle_difficulty()

    def toggle_difficulty(self):
        if self.search_method.get() == "Depth Limited":
            self.difficulty_entry.config(state='normal')
        else:
            self.difficulty_entry.config(state='disabled')

    def start_game(self):
        settings = {
            "search_method": self.search_method.get(),
            "difficulty": int(self.difficulty.get()) if self.search_method.get() == "Depth Limited" else None,
            "first_player": self.first_player.get(),
            "algorithm": self.algorithm.get()
        }
        self.start_callback(settings)
        self.destroy()
