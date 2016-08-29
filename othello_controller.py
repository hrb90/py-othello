from othello_ai import alphabeta, monte_carlo_eval
from othello_board import OthelloBoardModel

class OthelloPlayer:
    def __init__(self, color, automatic=True, depth=2):
        self.color = color
        self.automatic = automatic
        self.depth = depth

    def move(self, board):
        print self.color
        if self.automatic:
            alpha_beta = alphabeta(board, self.depth, self.color, -100, 100, monte_carlo_eval)
            best_move=alpha_beta[1]
            score = alpha_beta[0]
            print score
            return best_move


class OthelloController:
    def __init__(self, player_white, player_black):
        self.board = OthelloBoardModel()
        self.players = {'w': player_white, 'b': player_black}
        self.play()

    def get_color(self, x_coord, y_coord):
        return self.board.get_color(x_coord, y_coord)

    def play(self):
        if self.board.player_to_move == 'w':
            if self.players['w'].automatic:
                move = self.players['w'].move(self.board)
                self.make_move(move[0], move[1])
        else:
            if self.players['b'].automatic:
                move = self.players['b'].move(self.board)
                self.make_move(move[0], move[1])

    def make_move(self, x_coord, y_coord):
        if self.board.game_over:
            print self.board.score()
        success = self.board.play_move(self.board.player_to_move, x_coord, y_coord)
        return success
            
    def is_human_player(color):
        return not self.players[color].automatic

    def player_to_move(self):
        return self.board.player_to_move
