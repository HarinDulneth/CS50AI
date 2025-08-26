"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for row in board:
        for cell in row:
            if cell == X or cell == O:
                count += 1
    if count == 0 or count % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        row = board[i]
        for j in range(len(row)):
            cell = row[j]
            if cell != X and cell != O:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_new = copy.deepcopy(board)
    if action in actions(board):
        board_new[action[0]][action[1]] = player(board)
        return board_new
    raise Exception


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    patterns = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    for pattern in patterns:
        a, b, c = pattern
        if (
            board[a[0]][a[1]]
            and board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]]
        ):
            return board[a[0]][a[1]]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == O or winner(board) == X or len(actions(board)) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        best_val = -math.inf
        best_move = None
        for action in actions(board):
            result_board = result(board, action)
            moveEval = alphabeta(result_board, 0, -math.inf, math.inf, False)
            if moveEval > best_val:
                best_val = moveEval
                best_move = action

    if player(board) == O:
        best_val = math.inf
        best_move = None
        for action in actions(board):
            result_board = result(board, action)
            moveEval = alphabeta(result_board, 0, -math.inf, math.inf, True)
            if moveEval < best_val:
                best_val = moveEval
                best_move = action
    return best_move


def alphabeta(board, depth, alpha, beta, maximizingPlayer):
    print(board)
    if terminal(board):
        return utility(board)

    if maximizingPlayer:
        maxEval = -math.inf
        for action in actions(board):
            result_board = result(board, action)
            eval = alphabeta(result_board, depth + 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = math.inf
        for action in actions(board):
            result_board = result(board, action)
            eval = alphabeta(result_board, depth + 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
