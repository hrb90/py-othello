class OthelloBoardModel:
    def __init__(self, board_array = [[None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, 'w', 'b', None, None, None],
                      [None, None, None, 'b', 'w', None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None]],
                 player_to_move = 'b',
                 current_legal_moves = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 5), (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]):
        self.board_array = board_array
        self.player_to_move = player_to_move
        self.current_legal_moves = current_legal_moves
        self.game_over = False

    '''Traces a ray starting from the given point in the direction given by
    x_dir and y_dir, until we hit a point with the given color, an unoccupied
    point, or the edge of the board.
    Returns a list of the points that should be flipped.'''
    def trace_ray(self, color, x_coord, y_coord, x_dir, y_dir):
        points_on_ray = []
        while True:
            x_coord += x_dir
            y_coord += y_dir
            if x_coord > 7 or x_coord < 0 or y_coord > 7 or y_coord < 0:
                return []
            elif self.board_array[y_coord][x_coord] is None:
                return []
            elif self.board_array[y_coord][x_coord] == color:
                return points_on_ray
            else:
                points_on_ray.append((x_coord, y_coord))
                    
    '''Checks if the move is within the bounds of the board, and not on
    a point already occupied.
    Does not check that there will be pieces flipped.'''
    def is_legal_move(self, x_coord, y_coord):
        if x_coord > 7 or x_coord < 0 or y_coord > 7 or y_coord < 0:
            return False
        elif self.board_array[y_coord][x_coord] is not None:
            return False
        else:
            return True

    '''Returns a list of the flipped points (if any) resulting from playing
    the given color at the given coordinates'''
    def get_flipped_points(self, color, x_coord, y_coord):
        flipped_points = []
        for x_dir in [-1, 0, 1]:
            for y_dir in [-1, 0, 1]:
                if x_dir != 0 or y_dir != 0:
                    flipped_points_on_ray = self.trace_ray(color, x_coord, y_coord, x_dir, y_dir)
                    flipped_points = flipped_points + flipped_points_on_ray
        return flipped_points

    '''Attempts to play the given move on the board.
    If the move is illegal, returns False.
    If the move is legal, executes the play and returns True.'''
    def play_move(self, color, x_coord, y_coord):
        if not self.is_legal_move(x_coord, y_coord):
            return False
        flipped_points = self.get_flipped_points(color, x_coord, y_coord)
        if len(flipped_points) == 0:
            return False
        else:
            self.board_array[y_coord][x_coord] = color
            for x, y in flipped_points:
                self.board_array[y][x] = color
            self.refresh_legal_moves(x_coord, y_coord)
            if self.player_to_move == 'w':
                self.player_to_move = 'b'
            elif self.player_to_move == 'b':
                self.player_to_move = 'w'
            if not self.any_legal_moves(self.player_to_move):
                self.game_over = True
            return True

    def get_color(self, x_coord, y_coord):
        return self.board_array[y_coord][x_coord]

    def refresh_legal_moves(self, x, y):
        if (x, y) in self.current_legal_moves:
            self.current_legal_moves.remove((x, y))
        for x_dir in [-1, 0, 1]:
            for y_dir in [-1, 0, 1]:
                if x_dir != 0 or y_dir != 0:
                    if (x+x_dir, y+y_dir) not in self.current_legal_moves and self.is_legal_move(x+x_dir, y+y_dir):
                        self.current_legal_moves.append((x+x_dir, y+y_dir))

    def score(self):
        score = 0
        for row in self.board_array:
            for column in row:
                if column == 'w':
                    score += 1
                elif column == 'b':
                    score -= 1
        return score

    def any_legal_moves(self, color):
        for pt in self.current_legal_moves:
            if len(self.get_flipped_points(color, pt[0], pt[1])) > 0:
                return True
        return False

    def clone(self):
        cloned_board = OthelloBoardModel(board_array=self.board_array, player_to_move=self.player_to_move, current_legal_moves=self.current_legal_moves)
        return cloned_board
