import copy
import sys

from game import evaluate, find_tiger
# from game import is_game_over, evaluate, get_valid_moves, make_move
class AlphaBeta:
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
                    # if row == 1 and col == 2:
                    #     print("valid moves exit")
                    #     sys.exit(0)
                    # print("###Dog found at:", row, col)
                    # Check adjacent cells for valid moves for each dog
                    piece_moves = []
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        # print("Potential dog move:", new_row, new_col)
                        if not (0 <= new_row < len(state) and 0 <= new_col < len(state[row])):
                            # print(f"Dog move out of bounds: ({new_row}, {new_col})")
                            continue
                        if state[new_row][new_col] is not None:
                            # print(f"Dog move blocked by piece at: ({new_row}, {new_col}): {state[new_row][new_col]}")
                            continue
                        # print("Valid dog move:", new_row, new_col)
                        piece_moves.append([new_row, new_col])
                    if piece_moves:
                        valid_moves[(row, col)] = piece_moves

        return valid_moves
    
    # 4. max_value(state, depth) Function
    def max_value(self, state, depth, alpha, beta):
        # print("doing max at depth:", depth)
        """Maximizing player's (MAX) value function in Minimax."""
        if abs(evaluate(state)) == 10 or (depth != -1 and depth == 0):
            # print("END MAX SEARCH:", evaluate(state), "depth:", depth)
            return evaluate(state)
       
        max_eval = -float('inf')
        key = find_tiger(state)
        # print("Max Checking moves", len(self.get_valid_moves(self.game.board, 'tiger').get(key, [])))
        for move in self.get_valid_moves(state, 'tiger').get(key, []):
            next_state = self.copy_state(state)
            self.game.make_move(next_state, move[0], move[1], 'tiger') #tiger is max player
            #depth handling not ideal maybe should change
            next_depth = depth - 1 if depth != -1 else depth
            # print("FROM MAX next depth:", next_depth)
            eval_score = self.min_value(next_state, next_depth, alpha, beta)
            # print("Max eval score:", eval_score)
            max_eval = max(max_eval, eval_score)
            if max_eval >= beta: # Beta cutoff
                return max_eval
            alpha = max(alpha, max_eval)
        return max_eval

    # Best move always returns -1, -1, needs to be fixed
    def min_value(self, state, depth, alpha, beta):
        """Minimizing player's (MIN) value function in Minimax."""
        # print("doing min at depth:", depth)
        if abs(evaluate(state)) == 10 or (depth != -1 and depth == 0):
            # print("END MIN SEARCH:", evaluate(state), "depth:", depth)
            return evaluate(state)
        # check_win_conditions(self.game)
        # if (depth != -1 and depth == 0):
        #     print("Depth limit reached but isn't -1")
        #     return

        min_eval = float('inf')
        for dog_pos, possible_moves in self.get_valid_moves(state, 'dog').items():
            # if dog_pos == (0,3):
            #     sys.exit(0)
            # print("Dog position:", dog_pos)
            # print("Possible moves for dog:", possible_moves)
            for move in possible_moves:
                next_state = self.copy_state(state)
                self.game.make_move(next_state, move[0], move[1], 'dog', (dog_pos))
                next_depth = depth - 1 if depth != -1 else depth
                # print("next depth:", next_depth)
                eval_score = self.max_value(next_state, next_depth, alpha, beta) # MAX's response to MIN's move
                min_eval = min(min_eval, eval_score)
                if min_eval <= alpha: # Alpha cutoff
                    return min_eval
                beta = min(beta, min_eval)
        return min_eval

    # 6. Get Best Move Function
    def find_best_move(self, depth): #will only be called by tiger player
        """Finds the best move for MAX player using Minimax."""
        best_move_row = -1
        best_move_col = -1
        max_eval = -float('inf')
        alpha = -float('inf') # Initialize alpha
        beta = float('inf')  # Initialize beta
        key = find_tiger(self.game.board)
        # count = 0
        for move in self.get_valid_moves(self.game.board, 'tiger').get(key, []):
            # if count == 1:
            #     sys.exit(0)
            # print("Checking tiger move:", move)
            # count+=1
            next_state = self.copy_state(self.game.board)
            self.game.make_move(next_state, move[0], move[1], 'tiger')
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.min_value(next_state, next_depth, alpha, beta) # MIN's response to MAX's move
            # print("Eval score for move:", move, "is", eval_score)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move_row = move[0]
                best_move_col = move[1]
             
            alpha = max(alpha, max_eval)
        return [best_move_row, best_move_col]

    # Helper function to copy the state state (for minimax simulation)
    def copy_state(self, current_state):
        return copy.deepcopy(current_state)