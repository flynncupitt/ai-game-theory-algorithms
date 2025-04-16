import copy
from game import is_game_over, evaluate, get_valid_moves, make_move

# 1. Game State Representation: 2D list
MAX_PLAYER = 'X'
MIN_PLAYER = 'O'
EMPTY_CELL = ' '
state_counter = 0  # Initialize state counter
class AlphaBeta:

    # 4. max_value(state, depth, alpha, beta) Function with Alpha-Beta Pruning
    def max_value(self, current_state, depth, alpha, beta):
        """Maximizing player's (MAX) value function in Minimax with Alpha-Beta pruning."""
        global state_counter
        state_counter += 1

        if is_game_over(current_state) or (depth != -1 and depth == 0):
            return evaluate(current_state)

        max_eval = -float('inf')
        for move in get_valid_moves(current_state):
            next_state = self.copy_state(current_state)
            make_move(next_state, move[0], move[1], MAX_PLAYER)
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.min_value(next_state, next_depth, alpha, beta)
            max_eval = max(max_eval, eval_score)
            if max_eval >= beta: # Beta cutoff
                return max_eval
            alpha = max(alpha, max_eval)
        return max_eval

    # 5. min_value(state, depth, alpha, beta) Function with Alpha-Beta Pruning
    def min_value(self, current_state, depth, alpha, beta):
        """Minimizing player's (MIN) value function in Minimax with Alpha-Beta pruning."""
        global state_counter
        state_counter += 1

        if is_game_over(current_state) or (depth != -1 and depth == 0):
            return evaluate(current_state)

        min_eval = float('inf')
        for move in get_valid_moves(current_state):
            next_state = self.copy_state(current_state)
            make_move(next_state, move[0], move[1], MIN_PLAYER)
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.max_value(next_state, next_depth, alpha, beta)
            min_eval = min(min_eval, eval_score)
            if min_eval <= alpha: # Alpha cutoff
                return min_eval
            beta = min(beta, min_eval)
        return min_eval

    # 6. Get Best Move Function
    def find_best_move(self, current_state, depth):
        """Finds the best move for MAX player using Minimax with Alpha-Beta pruning."""
        global state_counter
        state_counter = 0
        best_move_row = -1
        best_move_col = -1
        max_eval = -float('inf')
        alpha = -float('inf') # Initialize alpha
        beta = float('inf')  # Initialize beta

        for move in get_valid_moves(current_state):
            next_state = self.copy_state(current_state)
            make_move(next_state, move[0], move[1], MAX_PLAYER)
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.min_value(next_state, next_depth, alpha, beta)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move_row = move[0]
                best_move_col = move[1]
            alpha = max(alpha, max_eval) # Update alpha in the MAX context


        print(f"States searched for this move (Alpha-Beta): {state_counter}")
        return [best_move_row, best_move_col]

    # Helper function to copy the state state (for minimax simulation)
    def copy_state(self, current_state):
        """Creates a deep copy of the game state."""
        return copy.deepcopy(current_state)