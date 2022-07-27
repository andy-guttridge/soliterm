# Reminder - terminal size of 80 characters wide and 24 rows high

# Import libraries
import curses
from curses import wrapper
import numpy as numpy

class TermManager:
    """
    Sets up two curses terminal windows and stores references to these
    in top_win and bottom_win instance variables, and initialises curses color
    pairs.
    """
    def __init__(self, stdscr):
        """
        Initialise instance of TermManager. Accepts a reference to the 
        curses terminal display as an argument. Clears the screen, sets up
        top and bottomm windows and stores them as top_win and bottom_win instance
        variables. Initialises curses color pairs.
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
        self.bottom_win.addstr(0,  0, "Soliterm Bottom Window", curses.color_pair(2))
        self.top_win.addstr(18,  0, "***********", curses.color_pair(3))
        self.bottom_win.addstr(4, 0, "***********", curses.color_pair(3))
        self.top_win.refresh()
        self.bottom_win.refresh()



def main(stdscr):
    term_manager = TermManager(stdscr)
    term_manager.scr_test()

    # Infinite loop to test curses windows displaying correctly
    # otherwise, they disappear as soon as the program ends!
    while True:
        continue

# Initialises curses display and passes a reference to the terminal display
# and calls our main main function when complete, passing it a reference to
# the terminal display.
wrapper(main)