import copy
from game import evaluate, find_tiger

class AlphaBeta:
    def __init__(self, game):
        self.game = game
    
    # This function was originally AI generated, with manual changes made to the directions and returned data types
    # Returns a dictionary of valid moves for the player where key is current position and value is a list of possible moves
    def get_valid_moves(self, state, player):
        valid_moves = {}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        # ^^^^ Up, Down, Left, Right, TL, TR, BL, BR

        for row in range(len(state)):
            for col in range(len(state[row])):
                if player == 'tiger' and state[row][col] == 'tiger':
                    piece_moves = []
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < len(state) and 0 <= new_col < len(state[row]) and state[new_row][new_col] is None:
                            piece_moves.append([new_row, new_col])
                    if piece_moves:
                        valid_moves[(row, col)] = piece_moves
                elif player == 'dog' and state[row][col] == 'dog':
                    piece_moves = []
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < len(state) and 0 <= new_col < len(state[row]) and state[new_row][new_col] is None:
                            piece_moves.append([new_row, new_col])

                    if piece_moves:
                        valid_moves[(row, col)] = piece_moves

        return valid_moves
    
    
    ### Minimax algorithm functions with alpha-beta pruning ###

    def max_value(self, state, depth, alpha, beta):

        if abs(evaluate(state)) == 10 or (depth != -1 and depth == 0):
            return evaluate(state)
       
        max_eval = -float('inf')
        key = find_tiger(state)

        for move in self.get_valid_moves(state, 'tiger').get(key, []):

            next_state = self.copy_state(state)
            self.game.make_move(next_state, move[0], move[1], 'tiger')
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.min_value(next_state, next_depth, alpha, beta)
            max_eval = max(max_eval, eval_score)

            if max_eval >= beta:
                return max_eval
            alpha = max(alpha, max_eval)

        return max_eval

    def min_value(self, state, depth, alpha, beta):

        if abs(evaluate(state)) == 10 or (depth != -1 and depth == 0):
            return evaluate(state)

        min_eval = float('inf')
        for dog_pos, possible_moves in self.get_valid_moves(state, 'dog').items():
            for move in possible_moves:
                next_state = self.copy_state(state)
                self.game.make_move(next_state, move[0], move[1], 'dog', (dog_pos))
                next_depth = depth - 1 if depth != -1 else depth
                eval_score = self.max_value(next_state, next_depth, alpha, beta)
                min_eval = min(min_eval, eval_score)
                if min_eval <= alpha:
                    return min_eval
                beta = min(beta, min_eval)
        return min_eval

    def find_best_move(self, depth):
        best_move_row = -1
        best_move_col = -1
        max_eval = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        key = find_tiger(self.game.board)
        
        for move in self.get_valid_moves(self.game.board, 'tiger').get(key, []):
            next_state = self.copy_state(self.game.board)
            self.game.make_move(next_state, move[0], move[1], 'tiger')
            next_depth = depth - 1 if depth != -1 else depth
            eval_score = self.min_value(next_state, next_depth, alpha, beta)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move_row = move[0]
                best_move_col = move[1]
             
            alpha = max(alpha, max_eval)
        return [best_move_row, best_move_col]

    def copy_state(self, current_state):
        return copy.deepcopy(current_state)