"""
Tic Tac Toe Player
"""

import math
import random
from exceptions import ActionNotPossibleError
from copy import deepcopy


X = "X"
O = "O"
EMPTY = None


def initial_state():
  """
  Returns starting state of the board.
  """
  return [[EMPTY, EMPTY, EMPTY],
          [EMPTY, EMPTY, EMPTY],
          [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    player = None
    X_count = 0
    O_count = 0

    for row in board:
      X_count += row.count(X)
      O_count += row.count(O)

    if X_count == 0 & O_count == 0:
        player = X
    elif X_count > O_count:
      player = O
    else:
      player = X
    return player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    i represents the board row, j the board column, both 0, 1 or 2
    The actions are are represented as the tuple (i, j) where the piece can be placed.
    """

    possible = set()

    for i in range(3):
      for j in range(3):
        if board[i][j] == EMPTY:
          possible.add((i, j))

    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    i = action[0]
    j = action[1]

    # Check move
    if i not in [0, 1, 2] or j not in [0, 1, 2]:
      raise ActionNotPossibleError(action, board, 'Result function given an invalid board position for action: ')
    elif board[i][j] != EMPTY:
      raise ActionNotPossibleError(action, board, 'Result function tried to perform invalid action on occupaied tile: ')

    copy = deepcopy(board)
    copy[i][j] = player(board)

    return copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # Rows:
    for row in board:
      if row.count(X) == 3:
        return X
      if row.count(O) == 3:
        return O

    # Columns:
    for col in range(3):
      column = ''
      for row in range(3):
        column += str(board[row][col])

      if column == 'XXX':
        return X
      if column == 'OOO':
        return O

    # Diagonals:
    diagonal1 = ''
    diagonal2 = ''
    col = 2

    for i in range(3):
      diagonal1 += str(board[i][i])
      diagonal1 += str(board[i][col])
      col -= 1

    if diagonal1 == 'XXX' or diagonal2 == 'XXX':
      return X
    elif diagonal1 == 'OOO' or diagonal2 == 'OOO':
      return O

    # If no winners
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if a winner is found or if there is no more actions available, then the game is over
    if winner(board) or not actions(board):
      return True
    else:
      return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
      return 1
    elif winner(board) == 'O':
      return -1
    else:
      return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    'X' Player is trying to maximise the score, 'O' Player is trying to minimise it
    """

    global tries
    tries = 0

    def max_player(board, best_min = 10):
      """ Maximise score for player X.
          best_min is the best result
      """

      global tries

      # Game Over
      if terminal(board):
        return (utility(board), None)

      # Get max_value
      value = -10
      best_action = None


      # Explore the available actions
      action_set = actions(board)

      while len(action_set) > 0:
        action = random.choice(tuple(action_set))
        action_set.remove(action)

        # A-B Pruning skips calls to min_player if lower result already found:
        if best_min <= value:
          break 

        tries += 1
        min_player_result = min_player(result(board, action), value)
        if min_player_result[0] > value:
          best_action = action
          value = min_player_result[0]

      return (value, best_action)


    def min_player(board, best_max = -10):
      """ Helper function to minimise score for 'O' player """

      global tries

      # If the game is over, return board value
      if terminal(board):
        return (utility(board), None)

      # Pick the min value
      value = 10
      best_action = None

      # Get set of actions + select random
      action_set = actions(board)

      while len(action_set) > 0:
        action = random.choice(tuple(action_set))
        action_set.remove(action)

        if best_max >= value:
          break

        tries += 1
        max_player_result = max_player(result(board, action), value)
        if max_player_result[0] < value:
          best_action = action
          value = max_player_result[0]

      return (value, best_action)


    # If the board is terminal, return None:
    if terminal(board):
      return None

    if player(board) == 'X':
      print('AI is exploring possible actions...')
      best_move = max_player(board)[1]
      print('Actions explored by AI: ', tries)
      return best_move
    else:
      print('AI is exploring possible actions...')
      best_move = min_player(board)[1]
      print('Actions explored by AI: ', tries)
      return best_move