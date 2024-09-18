import math
from copy import deepcopy

B = "B"
W = "W"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """

    maze = [[EMPTY for i in range(8)] for j in range(8)]

    maze[3][3] = W
    maze[3][4] = B
    maze[4][3] = B
    maze[4][4] = W
    return maze

    # Test case
    # return [[W, W, W, W, W, W, W, W],
    #         [W, W, W, W, W, W, W, W],
    #         [W, W, W, W, W, W, W, W],
    #         [W, W, W, B, EMPTY, B, W, W],
    #         [W, W, B, B, B, B, W, W],
    #         [W, B, EMPTY, W, EMPTY, B, W, W],
    #         [W, W, EMPTY, EMPTY, W, W, W, W],
    #         [W, W, B, B, W, W, W, W]]


def actions(board, player):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = set()

    for i in range(len(board)):
        for j in range(len(board[0])):
            if player == board[i][j]:
                possible_actions.update(check_adj(board, i, j, player))


    return possible_actions


def check_adj(board, x, y, player):
    possible_actions = set()

    for i in range(-1, 2):
        for j in range(-1 ,2):
            if i == 0 and j == 0:
                continue
            coords = is_legal(board, x, y, i, j, player)
            if coords is not None:
                possible_actions.add(coords)

    return possible_actions



def is_legal(board, x, y, dx, dy, player):
    i = x + dx
    j = y + dy
    if i < 0 or i >= len(board) or j < 0 or j >= len(board):
        return None

    if player == B:
        opposite = W
    else:
        opposite = B

    while board[i][j] is opposite:
        i = i + dx
        j = j + dy
        if i < 0 or i >= len(board) or j < 0 or j >= len(board):
            return None
        if board[i][j] is EMPTY:
            return (i, j)
    return None


def result(board, action, player, blacks, whites):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]

    board[i][j] = player
    db, dw = flipCoins(board, action)
    if (player == B):
        db += 1
    else:
        dw += 1

    return (board, blacks + db, whites + dw)


def winner(board, blacks, whites):
    """
    Returns the winner of the game, if there is one.
    """

    if blacks > whites:
        return "Black"
    elif whites > blacks:
        return "White"

    return None


def utility(board):
    """
    Returns 1 if B has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == B:
        return 1
    elif winner(board) == W:
        return -1
    return 0


max_depth = 7

def minimax(board, ai, possible_actions, whites, blacks):
    """
    Returns the optimal action for the current player on the board.
    """
    if ai == B:
        best = float('-inf')
    else:
        best = float('inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    if ai == B:
        is_max = True
    else:
        is_max = False

    for action in possible_actions:
        new_board = deepcopy(board)
        new_board, new_blacks, new_whites = result(new_board, action, ai, blacks, whites)
        value = min_max(new_board, new_blacks, new_whites, not is_max, 1, float('-inf'), float('inf'))
        if is_max and value > best:
            best = value
            alpha = max(alpha, best)
            best_move = action
        elif not is_max and value < best:
            best = value
            beta = min(beta, best)
            best_move = action
        if beta <= alpha:
            break


    return best_move

    # if terminal(board):
    #     return None
    # else:
    #     if player(board) == B:
    #         value, move = max_value(board)
    #         return move
    #     else:
    #         value, move = min_value(board)
    #         return move

# min_max is separate from minimax to take advantage of the possible_options
# set which must be initialized before the call to minimax
def min_max(board, blacks, whites, is_max, depth, alpha, beta):
    if depth == max_depth or whites + blacks == 64:
        return blacks - whites

    if is_max:
        best = float('-inf')
        player = B
    else:
        best = float('inf')
        player = W

    best_move = None
    possible_actions = actions(board, player)
    if len(possible_actions) == 0:
        return blacks - whites

    for action in possible_actions:
        new_board = deepcopy(board)
        new_board, new_blacks, new_whites = result(new_board, action, player, blacks, whites)
        value = min_max(new_board, new_blacks, new_whites, not is_max, depth + 1, alpha, beta)
        if is_max and value > best:
            best = value
            alpha = max(alpha, best)
        elif not is_max and value < best:
            best = value
            beta = min(beta, best)
        if beta <= alpha:
            break

    return best


# def max_value(board, user, ai, alpha, beta):
#
#     v = float('-inf')
#     move = None
#     for action in actions(board):
#         temp = min_value(result(board, action))[0]
#         if temp > v:
#             v = temp
#             move = action
#             if v == 1:
#                 return v, move
#
#     return v, move
#
#
# def min_value(board, user, ai, alpha, beta):
#     if terminal(board):
#         return utility(board), None
#
#     v = float('inf')
#     move = None
#     for action in actions(board):
#         temp = max_value(result(board, action))[0]
#         if temp < v:
#             v = temp
#             move = action
#             if v == -1:
#                 return v, move
#
#     return v, move

def flipCoins(board, coord):
    db = 0
    dw = 0
    player = board[coord[0]][coord[1]]
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            changes = flipsHelper(board, player, coord, i, j)
            db += changes[0]
            dw += changes[1]
    return (db, dw)


def flipsHelper(board, player, coord, dx, dy):
    db = 0
    dw = 0

    if player == W:
        opposite = B
    else:
        opposite = W
    i = coord[0] + dx
    j = coord[1] + dy
    flips = set()

    if i < 0 or i >= len(board) or j < 0 or j >= len(board):
        return (db, dw)

    while board[i][j] is opposite:
        flips.add((i, j))
        i = i + dx
        j = j + dy

        if i < 0 or i >= len(board) or j < 0 or j >= len(board):
            return (db, dw)
    if board[i][j] is EMPTY:
        return (db, dw)

    for position in flips:
        board[position[0]][position[1]] = player
        if player == B:
            db += 1
            dw -= 1
        else:
            db -= 1
            dw += 1

    return (db, dw)

