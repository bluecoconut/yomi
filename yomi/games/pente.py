import numpy as np

from ..base import Game


class Pente(Game):
    game_name = 'Pente'
    players = 2

    def __init__(self, size=19):
        self.board = np.zeros((size, size), dtype='int8')
        self.bags = np.zeros(2, dtype='int8')
        self.current_player = 1
        self.history = []

    def get_state_and_actions(self):  # Does not mutate data!
        actions = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i, j] == 0:
                    actions.append((i, j))
        sna = {'state': (self.board, self.bags, self.current_player), 'actions': actions}
        return tuple([sna if i == self.current_player-1 else None for i in range(self.players)])

    def execute_actions(self, actions):  # Does change state
        self.history.append(actions)
        pind = self.current_player-1
        move = actions[self.current_player-1]

        # Do the move
        if self.board[move] != 0:
            print(self.board[move], move, self.current_player)
            print(self.board)
            assert self.board[move] == 0
        eats = get_eats(self.board, self.current_player, move)

        self.bags[pind] += len(eats)
        for a, b in eats:
            self.board[a] = 0
            self.board[b] = 0

        self.board[move] = self.current_player
        player_win = check_win(self.board, self.current_player, move)
        if self.bags[pind] >= 5:
            player_win = 1

        # check if win
        if player_win == 1:
            # we have a winner
            return tuple([1.0 if i == pind else 0.0 for i in range(self.players)])

        # check if tie
        if len(self.get_state_and_actions()[pind]['actions']) == 0:
            return 0.5, 0.5
        # finalize
        self.current_player = (self.current_player) % 2+1
        return None

    def check_player_win(self, player):  # does not change state
        for j in range(3):
            win = True
            for i in range(3):
                win &= self.board[3*j+i] == player
            if win:
                return win
        for j in range(3):
            win = True
            for i in range(3):
                win &= self.board[j+i*3] == player
            if win:
                return win
        if self.board[0] == self.board[4] == self.board[8] == player:
            return True
        if self.board[2] == self.board[4] == self.board[6] == player:
            return True
        return False


edir = np.array([(i-1, j-1) for i in range(3) for j in range(3) if not(i == 1 and j == 1)])


def get_eats(board, player, move):
    eats = []
    neighbors = edir*3+np.array(move)
    check_p1 = edir*2+np.array(move)
    check_p2 = edir+np.array(move)
    for i, p in enumerate(neighbors):
        if 0 <= p[0] < board.shape[0] and 0 <= p[1] < board.shape[1]:
            if board[tuple(p)] == player:
                c1 = board[tuple(check_p1[i])]
                c2 = board[tuple(check_p2[i])]
                if c1 != 0 and c1 != player and c2 != 0 and c2 != player:
                    eats.append([tuple(check_p1[i]), tuple(check_p2[i])])
    return eats


edir2 = np.array([[-1, -1], [0, 1], [1, 0], [-1, 1]])


def check_win(board, player, move):
    for d in edir2:
        offsets = np.arange(-4, 1)
        for off in offsets:
            checks = np.array(move)+np.outer(np.arange(5)+off, d)
            valid = True
            for cp in checks:
                if cp[0] < 0 or cp[0] >= board.shape[0] or cp[1] < 0 or cp[1] >= board.shape[1]:
                    valid = False
                    break
                valid &= (board[tuple(cp)] == player)
            if valid:
                return 1
    return 0
