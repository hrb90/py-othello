from othello_board import OthelloBoardModel

class OthelloGame:
    def __init__(self):
        self.board = OthelloBoardModel()
        self.color = 'b'

    def none_to_o(self, x):
        if x is None:
            return 'o'
        else:
            return x

    def print_board(self):
        array = self.board.board_array
        for a in array:
            print map(self.none_to_o, a)

    def move(self, x_coord, y_coord, print_after=True):
        success = self.board.play_move(self.color, x_coord, y_coord)
        if success:
            if self.color == 'b':
                self.color = 'w'
            elif self.color == 'w':
                self.color = 'b'
            if print_after:
                self.print_board()
        else:
            print 'Illegal move!'
