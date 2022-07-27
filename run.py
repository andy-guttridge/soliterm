# Reminder - terminal size of 80 characters wide and 24 rows high

# Import libraries
import curses
from curses import wrapper
import numpy as numpy

def setup(stdscr):
    stdscr.clear()
    top_win = curses.newwin(19, 80, 0, 0)
    bottom_win = curses.newwin(5, 80, 19, 0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)

    top_win.addstr(0, 0, "Soliterm Top Window", curses.color_pair(1))
    bottom_win.addstr(0,  0, "Soliterm Bottom Window", curses.color_pair(2))
    top_win.addstr(18,  0, "***********", curses.color_pair(3))
    bottom_win.addstr(4, 0, "***********", curses.color_pair(3))
    top_win.refresh()
    bottom_win.refresh()


def main(stdscr):
    setup(stdscr)

    # Infinite loop to test curses windows displaying correctly
    # otherwise, they disappear as soon as the program ends!
    while True:
        continue


wrapper(main)