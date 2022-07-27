# Reminder - terminal size of 80 characters wide and 24 rows high

# Import libraries
import curses
from curses import wrapper
import numpy as np


class TermManager:
    """
    Sets up two curses terminal windows and contains references to these
    in top_win and bottom_win instance variables, and initialises curses color
    pairs.
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

    def scr_test(self):
        """
        Displays some srings in the top and bottom windows for testing.
        """
        self.top_win.addstr(0, 0, "Soliterm Top Window", curses.color_pair(1))
        self.bottom_win.addstr(0,  0, "Soliterm Bottom Window",
                               curses.color_pair(2))
        self.top_win.addstr(18,  0, "***********", curses.color_pair(3))
        self.bottom_win.addstr(4, 0, "***********", curses.color_pair(3))
        self.top_win.refresh()
        self.bottom_win.refresh()


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


def draw_board(game_board, term_manager):
    """
    Draws the game board in the top window.
    Arguments are references to the game_board object and
    the term_manager object.
    """
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
                                    curses.color_pair(0))
        term_manager.top_win.addstr(16, cell_pos * 3 + 25, f' {letters[num]} ',
                                    curses.color_pair(0))
        cell_pos += 1

    # Loop through each row and print out a number
    # to the left and right of each row.
    for num in range(1, 15):
        term_manager.top_win.addstr(num, 21, f' {str(num)} ',
                                    curses.color_pair(0))
        term_manager.top_win.addstr(num, 70, f' {str(num)} ',
                                    curses.color_pair(0))

    # Display the window now we've drawn to it
    term_manager.top_win.refresh()


def main(stdscr):
    term_manager = TermManager(stdscr)

    game_board = GameBoard()
    draw_board(game_board, term_manager)

    # Infinite loop to test curses windows displaying correctly
    # otherwise, they disappear as soon as the program ends!
    while True:
        continue


# Initialises curses display and passes a reference to the terminal display
# and calls our main main function when complete, passing it a reference to
# the terminal display.
wrapper(main)
