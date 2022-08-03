# Reminder - terminal size of 80 characters wide and 24 rows high

# Import libraries
import curses
from curses import wrapper
import numpy as np


class TermManager:
    """
    Sets up two curses terminal windows and contains references to these
    in top_win and bottom_win instance variables. Initialises curses color
    pairs. Stores number of pegs in the board and number of turns, and
    has a method to update these.
    """
    def __init__(self, stdscr):
        """
        Initialise instance of TermManager. Accepts a reference to the
        curses terminal display as an argument. Clears the screen, sets up
        top and bottomm windows and stores them as top_win and bottom_win
        instance variables. Initialises curses color pairs.
        """
        # Get a reference to the screen and clear it
        self.stdscr = stdscr
        stdscr.clear()

        # Define top and bottom windows
        self.top_win = curses.newwin(19, 80, 0, 0)
        self.bottom_win = curses.newwin(5, 80, 19, 0)

        # Initialise curses color_pairs
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

    def show_msg(self, row, *strs):
        """
        Displays an in game message in the bottom window.
        Arguments are starting row number and a number of strings.
        Displays each string on a new line.
        """
        i = 0
        # Clear window, loop through strings, position cursor, clear line,
        # display string
        self.bottom_win.clear()
        for string in strs:
            self.bottom_win.move(row + i, 0)
            self.bottom_win.addstr(row + i, 0, string, curses.color_pair(4))
            i += 1
        self.bottom_win.refresh()


class GameBoard:
    """
    Holds a 2D array representing the game board.
    """
    def __init__(self):
        """
        Initialise an instance of GameBoard with a 2D array configured
        for a new gamem and variables to hold number of pegs and turns.
        Values inside the array:
        0 = empty hole
        1 = hole with a peg
        2 = unplayable 'space' at the edge of the board
        """
        self.board_arr = np.array(
            # Starting layout for final game
            [
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
            ]
        )
        # Init number of pegs in the board and number of turns
        # Technique to count number of occurences of a value in an array from
        # https://thispointer.com/count-occurrences-of-a-value-in-numpy-array-in-python/
        self.num_pegs = np.count_nonzero(self.board_arr == 1)
        self.num_turns = 0

    def update_stats(self):
        """
        Updates number of pegs in board and
        increments number of turns.
        """
        # Technique to count number of occurences of a value in an array from
        # https://thispointer.com/count-occurrences-of-a-value-in-numpy-array-in-python/
        self.num_pegs = np.count_nonzero(self.board_arr == 1)
        self.num_turns += 1


def show_title(term_manager):
    """
    Displays the title screen and instructions.
    Waits for player to press a key to start.
    """
    # Define strings to display
    logo = np.array([
        r"              _________      .__  .__  __                        ",
        r"             /   _____/ ____ |  | |__|/  |_  ___________  _____  ",
        r"             \_____  \ /  _ \|  | |  \   __\/ __ \_  __ \/     \ ",
        r"             /        (  <_> )  |_|  ||  | \  ___/|  | \/  Y Y  \ ",
        r"            /_______  /\____/|____/__||__|  \___  >__|  |__|_|  / ",
        r"                    \/                          \/            \/ "
    ])

    tagline = "******************* A game of peg solitaire for the terminal"\
              " *******************"
    instructions = np.array([
        "The aim is to clear the board of pegs except for leaving one "
        "in the centre hole.",
        "Pegs can move up, down, left or right by jumping over another peg "
        "into an empty",
        "hole. The peg you jump over is removed - that's how you remove pegs.",
        " ",
        "Pegs are shown by * with a red background. "
        "Spaces are shown in blue.",
        "Enter your move with column, row and u, d, l or r for up, down, "
        "left or right.",
        " ",
        "Example: h10d to move peg in hole H10 down.",
        " ",
        "Example: n6l to move peg in hole N6 left."
    ])

    # Clear the top window and display the strings.
    term_manager.top_win.clear()
    for i in range(0, 3):
        term_manager.top_win.addstr(i, 0, logo[i], curses.color_pair(5))

    for i in range(3, len(logo)):
        term_manager.top_win.addstr(i, 0, logo[i], curses.color_pair(6))

    term_manager.top_win.addstr(6, 0, tagline, curses.color_pair(5))

    for i in range(0, len(instructions)):
        term_manager.top_win.addstr(i + 8, 0, instructions[i],
                                    curses.color_pair(4))

    term_manager.top_win.refresh()

    # Prompt player to press a key in the bottom window
    # and wait for key press.
    term_manager.show_msg(0, "Press a key to start")
    term_manager.bottom_win.getkey()


def draw_board(game_board, term_manager):
    """
    Draws the game board in the top window.
    Arguments are references to the game_board object and
    the term_manager object.
    """
    # Make sure window is clear
    term_manager.top_win.clear()

    # Counters to represent the position of each row and cell of the game board
    row_pos = 1
    cell_pos = 25

    # Iterate through each row and cell of the game board,
    # and draw the appropriate item in each position.
    # Each cell is 3 characters wide.
    for row in game_board.board_arr:
        for cell in row:
            if cell == 0:
                term_manager.top_win.addstr(row_pos,
                                            cell_pos, "   ",
                                            curses.color_pair(2))
            if cell == 1:
                term_manager.top_win.addstr(row_pos,
                                            cell_pos, " * ",
                                            curses.color_pair(1))
            if cell == 2:
                term_manager.top_win.addstr(row_pos,
                                            cell_pos, "   ",
                                            curses.color_pair(0))
            cell_pos += 3

        # Increment the row counter and reset the cell counter for another row
        row_pos += 1
        cell_pos = 25

    # Print out the cell position letters and numbers above
    # and below the board.
    cell_pos = 0

    # Loop through each column and print out a letter above
    # and below each column.
    for num in range(15):

        # Code to create a range of letters was adapted from this
        # tutorial from codingem:
        # https://www.codingem.com/python-range-of-letters/
        letters = [chr(n) for n in range(ord("A"), ord("P"))]
        term_manager.top_win.addstr(0, cell_pos * 3 + 25, f' {letters[num]} ',
                                    curses.color_pair(4))
        term_manager.top_win.addstr(16, cell_pos * 3 + 25, f' {letters[num]} ',
                                    curses.color_pair(4))
        cell_pos += 1

    # Loop through each row and print out a number
    # to the left and right of each row.
    for num in range(1, 16):
        term_manager.top_win.addstr(num, 21, f' {str(num)} ',
                                    curses.color_pair(4))
        term_manager.top_win.addstr(num, 70, f' {str(num)} ',
                                    curses.color_pair(4))

    # Print the game stats to the top window
    term_manager.top_win.addstr(0, 0, f"Pegs left: {game_board.num_pegs}",
                                curses.color_pair(4))
    term_manager.top_win.addstr(1, 0, f"Turns taken: {game_board.num_turns}",
                                curses.color_pair(4))

    # Display the window now we've drawn to it
    term_manager.top_win.refresh()


def get_move(term_manager):
    """
    Prompts the player to enter their next move,
    accepts input and returns the value entered.
    """
    term_manager.bottom_win.addnstr(0, 0, "Move format is column, row, "
                                    "direction, e.g. h10u",
                                    curses.color_pair(4))
    term_manager.bottom_win.move(1, 0)
    term_manager.bottom_win.clrtoeol()
    term_manager.bottom_win.addstr(1, 0, "Enter next move> ",
                                   curses.color_pair(4))
    curses.echo()

    player_input =\
        term_manager.bottom_win.getstr(1, 18, 4).decode(encoding="utf=8")
    curses.noecho()

    return player_input


def validate_format(move):
    """
    Validates the players move to ensure it is in the right format
    move argument is the string input by the player.

    Returns a tuple containing a bool to indicate if the move was
    in a valid format, and the row, column and direction of the move
    if it was valid.

    Row and column are integers, direction is a string.
    """
    # If move is not 3 or 4 characters, it is invalid.
    if len(move) > 4 or len(move) < 3:
        return(False, 0, 0, "0")

    # Extract column from move string and ensure lower case.
    column = move[0].lower()

    # If string is 3 characters, the row is the second character.
    # If string is 4 characters, slice out the second and third characters.
    if len(move) == 3:
        row = move[1]
    else:
        row = move[1:3]

    # The direction is always the last character.
    direction = move[-1].lower()

    # Check if the column is within the allowed range
    # and if it is convert to an integer.
    letters = [chr(n) for n in range(ord("a"), ord("p"))]
    if column not in letters:
        return(False, 0, 0, "0")
    else:
        column_num = letters.index(column)

    # Try to convert the row to an integer
    # and convert to zero indexed.
    # Catch error and return if player did not
    # enter a number.
    try:
        row_num = int(row) - 1
    except ValueError:
        return(False, 0, 0, "0")

    # Check if row is in allowed range
    if row_num not in range(0, 15):
        return(False, 0, 0, "0")

    # Check if direction is allowed
    letters = ["u", "d", "l", "r"]
    if direction not in letters:
        return(False, 0, 0, "0")

    # Everything checks out, return validated move
    return(True, row_num, column_num, direction)


def validate_move(move, game_board):
    """
    Check whether the player's move is valid within the rules.
    Returns a dictionary containing  a bool to indicate if
    move is valid, and if valid the location the player has moved
    from, where they are moving to and which peg to remove.
    """
    # Unpack the player's move
    (_, row_num, column_num, direction) = move

    # Initialise dictionary to hold details of all cells affected by move
    # In the event of an invalid move, it is returned as initialised here
    validated_dict = {
        "valid": False,
        "from": (0, 0),
        "to": (0, 0),
        "remove": (0, 0)
    }

    # Move can't be valid if the cell is an unplayable cell
    if game_board.board_arr[row_num, column_num] == 2:
        return validated_dict

    # If player wants to move down, the cell directly below
    # must have a peg and the cell below that must be empty

    if direction == "d" and row_num < (len(game_board.board_arr) - 2):
        if (game_board.board_arr[row_num + 1, column_num] == 1)\
          and (game_board.board_arr[row_num + 2, column_num] == 0):
            validated_dict = {
                "valid": True,
                "from": (row_num, column_num),
                "to": (row_num + 2, column_num),
                "remove": (row_num + 1, column_num)
            }
            return validated_dict
        else:
            return validated_dict

    # If player wants to move up, the cell directly above
    # must have a peg and the cell above that must be empty

    if direction == "u" and row_num > 1:
        if (game_board.board_arr[row_num - 1, column_num] == 1)\
          and (game_board.board_arr[row_num - 2, column_num] == 0):
            validated_dict = {
                "valid": True,
                "from": (row_num, column_num),
                "to": (row_num - 2, column_num),
                "remove": (row_num - 1, column_num)
            }
        else:
            return validated_dict

    # If player wants to move left, the cell directly to the left
    # must have a peg and the cell to the left of that must be empty
    if direction == "l" and column_num > 1:
        if (game_board.board_arr[row_num, column_num - 1] == 1)\
          and (game_board.board_arr[row_num, column_num - 2] == 0):
            validated_dict = {
                "valid": True,
                "from": (row_num, column_num),
                "to": (row_num, column_num - 2),
                "remove": (row_num, column_num - 1)
            }
        else:
            return validated_dict

    # If player wants to move right, the cell directly to the right
    # must have a peg and the cell to the right of that must be empty
    if direction == "r" and (column_num < len
                             (game_board.board_arr[row_num]) - 2):
        if (game_board.board_arr[row_num, column_num + 1] == 1)\
          and (game_board.board_arr[row_num, column_num + 2] == 0):
            validated_dict = {
                "valid": True,
                "from": (row_num, column_num),
                "to": (row_num, column_num + 2),
                "remove": (row_num, column_num + 1)
            }
        else:
            return validated_dict

    # If we haven't found a valid move by now, there can't be one
    return validated_dict


def eval_moves(game_board):
    """
    Tests whether there are still valid moves left.
    Returns True or False.
    """
    board = game_board.board_arr

    # Work our way through each cell on the board
    for row, col_arr in enumerate(board):
        for column, cell in enumerate(col_arr):

            # If the cell is empty or an unplayble space,
            # move onto the next cell
            if cell == 0 or cell == 2:
                continue

            # If the cell has a peg, test if there is a valid move in each
            # direction in turn
            elif cell == 1:
                if row > 1:
                    if (board[row - 1, column] == 1) and (board[row - 2,
                                                          column] == 0):
                        return True

                if row < (len(board) - 2):
                    if (board[row + 1, column] == 1) and (board[row + 2,
                                                          column] == 0):
                        return True

                if column > 2:
                    if (board[row, column - 1] == 1) and (board[row,
                                                          column - 2]) == 0:
                        return True

                if column < (len(col_arr) - 2):
                    if (board[row, column + 1] == 1) and (board[row,
                                                          column + 2] == 0):
                        return True

    # If we exit the loop without returning True,
    # there can be no valid moves left
    return False


def check_win(game_board):
    """
    Checks if the player has won and
    returns True or False
    """
    # If there is only one peg left and the middle position has a peg
    # player must have won.
    if game_board.num_pegs == 1 and game_board.board_arr[7, 7] == 1:
        return True
    else:
        return False


def main(stdscr):
    """
    The main game loop.
    """
    term_manager = TermManager(stdscr)
    
    #  Outer loop which encompasses the starting screen and game
    while True:

        # Show the title page
        show_title(term_manager)

        # Instantiate game_board instance and draw the board on the screen
        game_board = GameBoard()
        draw_board(game_board, term_manager)
        
        # Flag to record if the player has any moves left
        moves_left = True
        
        # Loop while the player still has possible moves
        while moves_left:

            # Flag to record if the player has entered a valid move
            valid_move = False
            
            # Loop until the player enters a valid move
            while not valid_move:

                # Get input from the player and return to start of loop if not
                # in a valid format
                next_move = get_move(term_manager)
                formatted_move = validate_format(next_move)
                if formatted_move[0] is False:
                    term_manager.show_msg(3, "Invalid format - try again")
                    continue
                
                # Check if the move is valid and return to start of loop if not
                validated_move = validate_move(formatted_move, game_board)
                if validated_move["valid"] is False:
                    term_manager.show_msg(3, "Invalid move - try again")
                    continue

                # Extract the coordinates of cell the player is moving from,
                # cell they are moving to and cell of peg to be removed
                (from_row, from_col) = validated_move["from"]
                (to_row, to_col) = validated_move["to"]
                (remove_row, remove_col) = validated_move["remove"]

                # Update cells with correct values, update stats and redraw
                # board
                game_board.board_arr[from_row, from_col] = 0
                game_board.board_arr[to_row, to_col] = 1
                game_board.board_arr[remove_row, remove_col] = 0
                game_board.update_stats()
                draw_board(game_board, term_manager)

                term_manager.show_msg(3, "Great move! Next turn")
                
                # Player has made a valid move so update flag to exit loop
                valid_move = True
            
            # Check if there are still valid moves remaining
            moves_left = eval_moves(game_board)
        
        # Player is out of moves. Check if they've won and
        # display appropriate message.
        if check_win(game_board):
            endgame_msg = "Wow, you've won! Well done!!!"
        else:
            endgame_msg = "There are no moves left - game over"

        term_manager.show_msg(0, endgame_msg, "Press a key to continue")
        term_manager.bottom_win.getkey()


# Initialises curses display and passes a reference to the terminal display
# and calls main function when complete, passing it a reference to
# the terminal display.
wrapper(main)
