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
        self.stdscr = stdscr
        stdscr.clear()
        self.top_win = curses.newwin(19, 80, 0, 0)
        self.bottom_win = curses.newwin(5, 80, 19, 0)

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)


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
            # Very sparse starting version of board for testing
            [
                [2, 2, 2, 2, 2, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 1, 0, 0, 1, 2, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [2, 2, 2, 2, 2, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 1, 0, 0, 1, 1, 2, 2, 2, 2, 2]
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
    #Define strings to display
    logo_1 = "              _________      .__  .__  __                        "
    logo_2 = "             /   _____/ ____ |  | |__|/  |_  ___________  _____  "
    logo_3 = "             \_____  \ /  _ \|  | |  \   __\/ __ \_  __ \/     \ "
    logo_4 = "             /        (  <_> )  |_|  ||  | \  ___/|  | \/  Y Y  \ "
    logo_5 = "            /_______  /\____/|____/__||__|  \___  >__|  |__|_|  /"
    logo_6 = "                    \/                          \/            \/ "
    tagline = "****************** A game of peg solitaire for the terminal ******************"
    instructions_1 = "The aim is to clear the board of pegs except for leaving one in the centre hole."
    instructions_2 = "Pegs can move up, down, left or right by jumping over another peg into an empty"
    instructions_3 = "hole. The peg you jump over is removed - that's how you remove pegs."
    instructions_4 = "Pegs are shown by * with a red background. Spaces are shown by a blue space."
    instructions_5 = "Enter your move with column, row and u, d, l or r for up, down, left or right."
    instructions_6 = "Example: h10d to move peg in hole H10 down."
    instructions_7 = "Example: n6l to move peg in hole N6 left."     
    
    # Clear the top window and display the strings.
    term_manager.top_win.clear()
    term_manager.top_win.addstr(0, 0, logo_1, curses.color_pair(5))
    term_manager.top_win.addstr(1, 0, logo_2, curses.color_pair(5))
    term_manager.top_win.addstr(2, 0, logo_3, curses.color_pair(5))
    term_manager.top_win.addstr(3, 0, logo_4, curses.color_pair(6))
    term_manager.top_win.addstr(4, 0, logo_5, curses.color_pair(6))
    term_manager.top_win.addstr(5, 0, logo_6, curses.color_pair(6))
    term_manager.top_win.addstr(6, 0, tagline, curses.color_pair(5))

    term_manager.top_win.addstr(8, 0, instructions_1, curses.color_pair(4))
    term_manager.top_win.addstr(9, 0, instructions_2, curses.color_pair(4))
    term_manager.top_win.addstr(10, 0, instructions_3, curses.color_pair(4))
    term_manager.top_win.addstr(11, 0, instructions_4, curses.color_pair(4))
    term_manager.top_win.addstr(13, 0, instructions_5, curses.color_pair(4))
    term_manager.top_win.addstr(15, 0, instructions_6, curses.color_pair(4))
    term_manager.top_win.addstr(17, 0, instructions_7, curses.color_pair(4))

    term_manager.top_win.refresh()
    
    # Prompt player to press a key in the bottom window
    # and wait for key press.
    term_manager.bottom_win.clear()
    term_manager.bottom_win.addstr(0, 0, "Press a key to start")
    term_manager.bottom_win.refresh()
    key = term_manager.bottom_win.getkey()


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

    #Print the game stats to the top window
    term_manager.top_win.addstr(0, 0, f"Pegs left: {game_board.num_pegs}", curses.color_pair(5))
    term_manager.top_win.addstr(1, 0, f"Turns taken: {game_board.num_turns}", curses.color_pair(5))
        
    # Display the window now we've drawn to it
    term_manager.top_win.refresh()


def get_move(term_manager):
    """
    Prompts the player to enter their next move,
    accepts input and returns the value entered.
    """
    term_manager.bottom_win.addnstr(0, 0, "Move format is column, row, direction, e.g. h10u", curses.color_pair(4))
    term_manager.bottom_win.move(1, 0)
    term_manager.bottom_win.clrtoeol()
    term_manager.bottom_win.addstr(1, 0, "Enter next move> ", curses.color_pair(4))
    curses.echo()

    player_input = term_manager.bottom_win.getstr(1, 18, 4).decode(encoding="utf=8")
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
    Returns a dictionary containing the a bool to indicate if
    move is valid, and if valid the location the player has moved
    from, where they are moving to and which peg to remove.
    """
    # Unpack the player's move
    (is_valid, row_num, column_num, direction) = move
    
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
    try:
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
    
    # Treat as invalid if move is out of bounds of the array
    except IndexError:
        return validated_dict
    
    # If player wants to move up, the cell directly above
    # must have a peg and the cell above that must be empty
    try:
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
    
    # Treat as invalid if move is out of bounds of the array
    except IndexError:
        return validated_dict

    # If player wants to move left, the cell directly to the left
    # must have a peg and the cell to the left of that must be empty
    try:
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

    # Treat as invalid if move is out of bounds of the array
    except IndexError:
        return validated_dict
    
    # If player wants to move right, the cell directly to the right
    # must have a peg and the cell to the right of that must be empty
    try:
        if direction == "r" and (column_num < len(game_board.board_arr[row_num]) - 2):
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
    
    # Treat as invalid if move is out of bounds of the array
    except IndexError:
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

            #If the cell is empty or an unplayble space, move onto the next cell
            if cell == 0 or cell == 2:
                continue

            # If the cell has a peg, test if there is a valid move in each 
            # direction in turn
            elif cell == 1:
                if row > 1:
                    if (board[row - 1, column] == 1) and (board[row - 2, column] == 0):
                        return True

                if row < (len(board) - 2):
                    if (board[row + 1, column] == 1) and (board[row + 2, column] == 0):
                        return True

                if column > 2:
                    if (board[row, column - 1] == 1) and (board[row, column - 2]) == 0:
                        return True

                if column < (len(col_arr) - 2):
                    if (board[row, column + 1] == 1) and (board[row, column + 2] == 0):
                        return True
    
    # If we exit the loop without returning True, there can be no valid moves left
    return False


def main(stdscr):
    term_manager = TermManager(stdscr)
    game_board = GameBoard()

    while True:
        show_title(term_manager)
        draw_board(game_board, term_manager)

        moves_left = True

        while moves_left:
            valid_move = False
            
            while not valid_move:
                next_move = get_move(term_manager)
                formatted_move = validate_format(next_move)
                if formatted_move[0] is False:
                    term_manager.bottom_win.move(3, 0)
                    term_manager.bottom_win.clrtoeol()
                    term_manager.bottom_win.addstr(3, 0, "Invalid format - try again", curses.color_pair(4))
                    term_manager.bottom_win.refresh()
                    continue

                validated_move = validate_move(formatted_move, game_board)

                if validated_move["valid"] is False:
                    term_manager.bottom_win.move(3, 0)
                    term_manager.bottom_win.clrtoeol()
                    term_manager.bottom_win.addstr(3, 0, "Invalid move - try again", curses.color_pair(4))
                    term_manager.bottom_win.refresh()
                    continue
                
                (from_row, from_col) = validated_move["from"]
                (to_row, to_col) = validated_move["to"]
                (remove_row, remove_col) = validated_move["remove"]

                game_board.board_arr[from_row, from_col] = 0
                game_board.board_arr[to_row, to_col] = 1
                game_board.board_arr[remove_row, remove_col] = 0
                draw_board(game_board, term_manager)
                
                term_manager.bottom_win.move(3, 0)
                term_manager.bottom_win.clrtoeol()
                term_manager.bottom_win.addstr(3, 0, "Great move! Next turn", curses.color_pair(4))
                term_manager.bottom_win.refresh()

                valid_move = True
            
            game_board.update_stats()
            moves_left = eval_moves(game_board)

        term_manager.bottom_win.move(3, 0)
        term_manager.bottom_win.clrtoeol()
        term_manager.bottom_win.addstr(0, 0, "There are no moves left - game over", curses.color_pair(4))
        term_manager.bottom_win.addstr(1, 0, "Press a key to continue", curses.color_pair(4))
        term_manager.bottom_win.refresh()
        term_manager.bottom_win.getkey()


# Initialises curses display and passes a reference to the terminal display
# and calls our main main function when complete, passing it a reference to
# the terminal display.
wrapper(main)
