import copy
from game import is_game_over, evaluate, get_valid_moves, make_move
class Minimax:
    MAX_PLAYER = 'X'
    MIN_PLAYER = 'O'
    EMPTY_CELL = ' '
    # 4. max_value(state, depth) Function
    def max_value(self, current_state, depth):
        """Maximizing player's (MAX) value function in Minimax."""
        if is_game_over(current_state) or (depth != -1 and depth == 0):
            return evaluate(current_state)

        max_eval = -float('inf')
        for move in get_valid_moves(current_state):
            next_state = self.copy_state(current_state)
            make_move(next_state, move[0], move[1], self.MAX_PLAYER)
            #depth handling not ideal maybe should change
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.min_value(next_state, next_depth)
            max_eval = max(max_eval, eval_score)
        return max_eval

    # 5. min_value(state, depth) Function
    def min_value(self, current_state, depth):
        """Minimizing player's (MIN) value function in Minimax."""
        if is_game_over(current_state) or (depth != -1 and depth == 0):
            return evaluate(current_state)

        min_eval = float('inf')
        for move in get_valid_moves(current_state):
            next_state = self.copy_state(current_state)
            make_move(next_state, move[0], move[1], self.MIN_PLAYER)
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.max_value(next_state, next_depth)
            min_eval = min(min_eval, eval_score)
        return min_eval

    # 6. Get Best Move Function
    def find_best_move(self, current_state, depth):
        """Finds the best move for MAX player using Minimax."""
        best_move_row = -1
        best_move_col = -1
        max_eval = -float('inf')

        for move in get_valid_moves(current_state):
            next_state = self.copy_state(current_state)
            make_move(next_state, move[0], move[1], self.MAX_PLAYER)
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.min_value(next_state, next_depth) # MIN's response to MAX's move

            if eval_score > max_eval:
                max_eval = eval_score
                best_move_row = move[0]
                best_move_col = move[1]

        return [best_move_row, best_move_col]

    # Helper function to copy the state state (for minimax simulation)
    def copy_state(self, current_state):
        """Creates a deep copy of the game state."""
        return copy.deepcopy(current_state)