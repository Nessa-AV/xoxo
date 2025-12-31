import random
from math import inf

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.player = "X"

    def print_board(self):
        """Display the game board with colors"""
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            colored_row = []
            for spot in row:
                if spot == 'X':
                    colored_row.append('\033[92mX\033[0m')
                elif spot == 'O':
                    colored_row.append('\033[91mO\033[0m')
                else:
                    colored_row.append(' ')
            print('| '+' | '.join(colored_row)+' |' )


    @staticmethod
    def print_board_nums():
        """display cell numbers"""
        number_board = [[str(i+1) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| '+' | '.join(row) +' |')

    def available_moves(self):
        """Returns a list of available movis"""
        return[i for i,spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        """Are thare any empty squares?"""
        return ' ' in self.board

    def num_empty_squares(self):
        """Mmber of empty squares"""
        return self.board.count(' ')

    def make_move(self, square, letter):
        """make a move"""
        if self.board[square] == ' ':
            self.board[square] =letter
            if self.winner(square,letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        """check for win"""
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
    
        col_ind = square % 3
        column = [self.board[col_ind+i*3]for i in range(3)]
        if all ([spot == letter for spot in column]):
            return True
    
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all ([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
            
        return False
    
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
                
    def reset(self):
        """Reset the game to initial state"""
        self.__init__()
 