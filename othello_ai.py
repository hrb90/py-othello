import random
from copy import deepcopy
from othello_board import OthelloBoardModel

def evaluation_function(board):
    return board.score()


def monte_carlo_eval(board, n_runs = 100):
    total_score = 0.0
    for i in range(n_runs):
        total_score += monte_carlo_run(board)
    avg_score = total_score/n_runs
    return avg_score


def monte_carlo_run(board):
    new_board = deepcopy(board)
    while not new_board.game_over:
        moves = new_board.current_legal_moves
        random.shuffle(moves)
        for move in moves:
            success = new_board.play_move(new_board.player_to_move, move[0], move[1])
            if success:
                break
    return new_board.score()


def minimax(board, depth, color, evaluate):
    if depth==0 or board.game_over:
        return (evaluate(board), None)

    if color=='w':
        # Maximize
        best_value = -100
        best_move = None
        for move in board.current_legal_moves:
            new_board = deepcopy(board)
            if new_board.play_move(color, move[0], move[1]):
                v = minimax(new_board, depth-1, 'b', evaluate)[0]
                if v > best_value:
                    best_value = v
                    best_move = move
        return (best_value, best_move)
    elif color=='b':
        # Minimize
        best_value = 100
        best_move = None
        for move in board.current_legal_moves:
            new_board = deepcopy(board)
            if new_board.play_move(color, move[0], move[1]):
                v = minimax(new_board, depth-1, 'w', evaluate)[0]
                if v < best_value:
                    best_value = v
                    best_move = move
        return (best_value, best_move)
    else:
        raise Exception    

def alphabeta(board, depth, color, alpha, beta, evaluate):
    if depth==0 or board.game_over:
        return (evaluate(board), None)
    
    if color=='w':
        best_value = -100
        best_move = None
        for move in board.current_legal_moves:
            new_board = deepcopy(board)
            if new_board.play_move(color, move[0], move[1]):
                v = alphabeta(new_board, depth-1, 'b', alpha, beta, evaluate)[0]
                if v > best_value:
                    best_value = v
                    best_move = move
                if v > alpha:
                    alpha = v
            if beta <= alpha:
                break
        return (best_value, best_move)

    elif color=='b':
        best_value = 100
        best_move = None
        for move in board.current_legal_moves:
            new_board = deepcopy(board)
            if new_board.play_move(color, move[0], move[1]):
                v = alphabeta(new_board, depth-1, 'w', alpha, beta, evaluate)[0]
                if v < best_value:
                    best_value = v
                    best_move = move
                if v < beta:
                    beta = v
            if beta <= alpha:
                break
        return (best_value, best_move)
    else:
        raise Exception