import copy

from game import evaluate, get_tiger_pos
# from game import is_game_over, evaluate, get_valid_moves, make_move
class Minimax:
    def __init__(self, game):
        """Initialize the Minimax algorithm with the game GUI."""
        self.game = game

    def get_valid_moves(self, state, player):
        """Returns a dictionary of valid moves for each piece of the current player."""
        valid_moves = {}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Up, Down, Left, Right, TL, TR, BL, BR

        for row in range(len(state)):
            for col in range(len(state[row])):
                if player == 'tiger' and state[row][col] == 'tiger':
                    # Check adjacent cells for valid moves for tiger
                    piece_moves = []
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < len(state) and 0 <= new_col < len(state[row]) and state[new_row][new_col] is None:
                            piece_moves.append([new_row, new_col])
                    if piece_moves:
                        valid_moves[(row, col)] = piece_moves
                elif player == 'dog' and state[row][col] == 'dog':
                    # Check adjacent cells for valid moves for each dog
                    piece_moves = []
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < len(state) and 0 <= new_col < len(state[row]) and state[new_row][new_col] is None:
                            piece_moves.append([new_row, new_col])
                    if piece_moves:
                        valid_moves[(row, col)] = piece_moves

        return valid_moves
    
    # 4. max_value(state, depth) Function
    def max_value(self, state, depth):
        """Maximizing player's (MAX) value function in Minimax."""
        if abs(evaluate(state)) == 10 or (depth != -1 and depth == 0):
            return evaluate(state)
       
        max_eval = -float('inf')
        key = get_tiger_pos()

        for move in self.get_valid_moves(self.game.board, 'tiger').get(key, []):

            #DO NEXT: loop through valid tiger moves and do minimax
            # Check if the move is valid
            if move[0] < 0 or move[0] >= len(self.game.board) or move[1] < 0 or move[1] >= len(self.game.board):
                continue

            # Check if the target cell is empty
            if self.game.board[move[0]][move[1]] is not None:
                continue
     
            next_state = self.copy_state(state)
            self.game.make_move(next_state, move[0], move[1], 'tiger') #tiger is max player
            #depth handling not ideal maybe should change
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.min_value(next_state, next_depth)
            print("Max eval score:", eval_score)
            max_eval = max(max_eval, eval_score)
        return max_eval

    # Best move always returns -1, -1, needs to be fixed
    def min_value(self, state, depth):
        """Minimizing player's (MIN) value function in Minimax."""
        if abs(evaluate(state)) == 10 or (depth != -1 and depth == 0):
            return evaluate(state)
        # check_win_conditions(self.game)
        # if (depth != -1 and depth == 0):
        #     print("Depth limit reached but isn't -1")
        #     return

        min_eval = float('inf')
        for dog_pos, possible_moves in self.get_valid_moves(state, 'dog').items():
            for move in possible_moves:
                # Check if the move is valid
                if move[0] < 0 or move[0] >= len(state) or move[1] < 0 or move[1] >= len(state):
                    continue

                # Check if the target cell is empty
                if state[move[0]][move[1]] is not None:
                    continue

                next_state = self.copy_state(state)
                self.game.make_move(next_state, move[0], move[1], 'dog', (dog_pos))
                next_depth = depth - 1 if depth != -1 else depth
                eval_score = self.max_value(next_state, next_depth)
                min_eval = min(min_eval, eval_score)
                print("Returning min eval score:", eval_score)
        return min_eval

    # 6. Get Best Move Function
    def find_best_move(self, depth): #will only be called by tiger player
        """Finds the best move for MAX player using Minimax."""
        best_move_row = -1
        best_move_col = -1
        max_eval = -float('inf')
        key = get_tiger_pos()

        for move in self.get_valid_moves(self.game.board, 'tiger').get(key, []):

            # Check if the move is valid
            if move[0] < 0 or move[0] >= len(self.game.board) or move[1] < 0 or move[1] >= len(self.game.board):
                continue

            # Check if the target cell is empty
            if self.game.board[move[0]][move[1]] is not None:
                continue

            next_state = self.copy_state(self.game.board)
            self.game.make_move(next_state, move[0], move[1], 'tiger')
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.min_value(next_state, next_depth) # MIN's response to MAX's move

            if eval_score > max_eval:
                max_eval = eval_score
                best_move_row = move[0]
                best_move_col = move[1]

        return [best_move_row, best_move_col]

    # Helper function to copy the state state (for minimax simulation)
    def copy_state(self, current_state):
        return copy.deepcopy(current_state)