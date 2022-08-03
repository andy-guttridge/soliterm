```
import numpy as np


class GameBoard:
    """
    Holds a 2D array representing the game board.
    """
    def __init__(self):
        """
        Initialise an instance of GameBoard with a 2D array configured
        for a new game.
        Values inside the array:
        0 = empty hole
        1 = hole with a peg
        2 = unplayable 'space' at the edge of the board
        """
        self.board_arr = np.array(
            # Starting layout for final game
            # [
            #     [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            #     [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            #     [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
            # ]
            # Sparse starting version of board for testing
            # [
            #     [2, 2, 2, 2, 2, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 1, 0, 0, 1, 2, 2, 2, 2, 2],
            #     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
            #     [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            #     [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
            #     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            #     [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            #     [2, 2, 2, 2, 2, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 1, 0, 0, 1, 1, 2, 2, 2, 2, 2]
            # ]
            # One move from a win layout for testing
            [
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2]
            ]
            # Close to a win layout for testing
            # [
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            #     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            #     [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            #     [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            #     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            #     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2]
            # ]
        )


def eval_moves(g_board):
    """
    Tests whether there are still valid moves left.
    Returns True or False.
    """
    board = g_board.board_arr

    # Work our way through each cell on the board
    print("------------------ NEW RUN -------------------")
    for row, col_arr in enumerate(board):
        for column, cell in enumerate(col_arr):
            print(f'Row: {row} Column: {column} Value: {cell}', end=" :: ")

            # If the cell is empty or an unplayble space,
            # move onto the next cell.
            if cell == 0 or cell == 2:
                print('Did not test cell - move on to next')
                continue

            # If the cell has a peg, test if there is a valid move in each
            # direction in turn
            elif cell == 1:
                if row > 1:
                    if (board[row - 1, column] == 1) and \
                      (board[row - 2, column] == 0):
                        print('Found valid move up - returning True')
                        return True

                if row < (len(board) - 2):
                    if (board[row + 1, column] == 1) and \
                      (board[row + 2, column] == 0):
                        print('Found valid move down - returning True')
                        return True

                if column > 2:
                    if (board[row, column - 1] == 1) and \
                      (board[row, column - 2]) == 0:
                        print('Found valid move left - returning True')
                        return True

                if column < (len(col_arr) - 2):
                    if (board[row, column + 1] == 1) and \
                      (board[row, column + 2] == 0):
                        print('Found valid move right - returning True')
                        return True

                print('Found no valid move - moving to next cell')

    print('Outer loop ended - returning false')
    return False


game_board = GameBoard()
eval_moves(game_board)
```
