import numpy as np
import math
from ..base import Agent


class BruteForceTicTacToe(Agent):
    agent_type = 'Proper Agent'

    def __init__(self, name='advanced'):
        self.name = name

    def get_move(self, sna):
        if not sna:
            return None
        state = sna['state']
        actions = sna['actions']
        board = state[0]
        player = state[1]
        choice = min([i for i in get_possible_moves(board)],key=lambda x: get_loss_and_tie_percents(board, x, player))
        return choice

    def __repr__(self):
        return self.agent_type + ":" + self.name

def get_possible_moves(board):
    return [i for i in range(len(board)) if board[i] == '']

def check_player_win(state, player):
    for j in range(3):
        win = True
        for i in range(3):
            win &= state[3*j+i] == player
        if win:
            return win
    for j in range(3):
        win = True
        for i in range(3):
            win &= state[j+i*3] == player
        if win:
            return win
    if state[0]==state[4]==state[8]==player:
        return True
    if state[2]==state[4]==state[6]==player:
        return True
    return False

def memoize(func):
    cache = {}
    def new_func(*args):
        try:
            return cache[str(args)]
        except:
            result = func(*args)
            cache[str(args)] = result
            return result
    return new_func

@memoize
def stats_down_path(board, move, player):
    board = board[:]
    board[move[0]] = move[1]
    moves = get_possible_moves(board)
    n = len(moves)
    if check_player_win(board,player):
        return (math.factorial(n), 0, 0)
    if check_player_win(board,1-player):
        return (0, math.factorial(n), 0)
    if len(moves) == 0:
        return (0, 0, 1)
    results = []
    for m in moves:
        results.append(stats_down_path(board,(m,1-move[1]),player))
    return tuple(np.array(results).sum(axis=0))

def get_loss_and_tie_percents(board, move, player):
    res = stats_down_path(board,(move,player),player)
    return (res[1]/sum(res), res[2]/sum(res))
