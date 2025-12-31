import random
from math import inf

class AIPlayer:
    def __init__ (self, letter, difficulty='hard'):
        self.letter = letter
        self.opponent_letter = 'O' if letter == 'X' else 'X'
        self.difficulty = difficulty

    def get_move(self, game):
        """get move"""
        if self.difficulty == 'easy':
            return random.choice(game.available_moves())
        elif self.difficulty =='medium':
            if random.random() < 0.5:
                return random.choice(game.available_moves())
            else:
                return self.minimax(game,self.letter)['position']
        else:
            if len(game.available_moves()) == 9:
                return random.choice(game.available_moves())
            return self.minimax(game, self.letter)['position']

    def minimax(self, state, player):
        """Minimax algorithm"""
        max_player = self.letter
        other_player = 'O' if player =='X' else 'X'
        if state.current_winner == other_player:
            return {
                'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player 
                        else -1 * (state.num_empty_squares() + 1)
            }
        
        elif not state.empty_squares():
            return {'position': None, 'score': 0}
        
        best = {
            'position': None,
            'score': -inf if player == max_player else inf
        }

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)

            state.board[possible_move] = ' ' 
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best

    
    def minimax_alpha_beta(self, state, player, alpha=-inf, beta=inf):
        """Minimax with alpha-beta pruning"""
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'
    
        if state.current_winner is not None:
            if state.current_winner == max_player:
                return {'position': None, 'score': 1 * (state.num_empty_squares() + 1)}
            else:
                return {'position': None, 'score': -1 * (state.num_empty_squares() + 1)}
    
        elif not state.empty_squares():
            return {'position': None, 'score': 0}
    
        best = {'position': None, 'score': -inf if player == max_player else inf}
    
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax_alpha_beta(state, other_player, alpha, beta)
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
        
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, best['score'])
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, best['score'])
        
            if beta <= alpha:  
                break
    
        return best
  