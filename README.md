# Soliterm
## A game of peg solitaire to play in the terminal
Soliterm is a game of [Peg Solitaire](https://en.wikipedia.org/wiki/Peg_solitaire) - also known as Solo Noble - that runs in the terminal and developed in Python.
The objective of Soliterm is to empty the game board, except for a single peg in the central hole and using only valid moves.
A peg may move orthogonally over an adjacent peg into a hole two positions away - the peg that has just been 'jumped' over is then removed.

This implementation was inspired by the one in 'The Turing Criterion - Machine Intelligent Programes for the 16K ZX81' (Charlton, Harrison, Jones and Hartnell, 1982), and has 124 holes as opposed to 33 in the traditional English version.

<p align="center">
    <img src="readme_assets/zx81-1.png" alt="Machine Intelligent Programmes for the 16K ZX81 book cover" align="center">
    <img src="readme_assets/zx81-2.png" alt="Machine Intelligent Programmes for the 16K ZX81 Solitaire screen shot" align="center" height="345">
</p>

## Table of contents
*To complete*

## Objectives
The objectives of the application are:

1. To provide the user with an entertaining game of Solitaire in a terminal environment.
2. To provide clear instructions to the user.
3. To present a clear representation of a Peg Solitaire board in a terminal.
4. To successfully validate the user's entry of their next intended move, and provide feedback if the user enters a move in an invalid format or if the desired move is not possible within the rules of the game.
5. To provide the user with feedback on how many pegs they have left in the board.
6. To provide the user with feedback on how many moves they have made.
7. To inform the user if there are no valid moves left.

## Features
*To complete*

### Existing features
*To complete*

### Future features
*To complete*

## Libraries used
- The Python [curses](https://docs.python.org/3/library/curses.html#module-curses) module was used to access the C ncurses library directly using Python. This allows more advanced manipulation of the text displayed in the terminal than would otherwise be possible. The aim was to provide the player with a static game board, and to consistently position the data on the number of pegs left, the number of moves made and the area where the player is prompted for their input in the terminal window. Without using a library such as ncurses, the terminal would quickly fill with text, which would scroll off the screen, and the game board would have to be continually redrawn at the current cursor position. Soliterm also takes advantaged of the fact that ncurses also allows the use of basic colour where supported by the terminal.
- The [NumPy](https://www.w3schools.com/python/numpy/default.asp) library is used for the array representing the game board. This was chosen because NumPy arrays are usually quicker than standard Python lists, and allows simple creation and manipulation of a 2D array, which is a convenient data structure for representing the Solitare board.

## Data model
*To complete*

- Game board data model
- TermManager class

## Testing
*To complete*
- A test function called `debug_output_move()` was used to output a string containing the outcome of the validation (`True` or `False`), row, column and direction of the player's move to the terminal while testing the `validate_format()` function.
- To enable testing of the `validate_move()` function, the starting configuration of the array representing the game board was temporarily amended to contain lots of empty cells, to quickly test the output of the function in different scenarios. When play testing revealed bugs in the `validate_move()` and `eval_moves()` functions, screenshots of the state of the board when the bugs occurred were taken. The data for the fully initialised layout of the board was commented out and replaced by a layout manually amended to match the screenshots to enable repeated testing of the state of the board when the bugs were detected.
- While use of the curses library allows considerable flexibility in formatting output to the terminal, the output of `print` statements is disabled, complicating the debugging process. This was particularly challenging when debugging the `eval_moves()` function. Use of the Python [logging](https://docs.python.org/3/library/logging.html) API to output values to a log file was considered, however a simple approach was chosen. The `GameBoard` class and the `eval_moves()` functions were copied into a `debug.py` file which didn't use curses, allowing a game board to be initialised and the output of `eval_moves()` to be printed to the terminal. This enabled the bug to be identified and fixed quite quickly.

### Validator testing
*To complete*

### Bugs
#### Resolved bugs
- The `curses getstr()` function which is used to prompt and accept input from the player was returning a bytes object instead of a string, which caused a type error in the validate_format() function. This was resolved with the help of [Stack Overflow](https://stackoverflow.com/questions/21505871/curses-window-getstr) question, which noted that the `decode` method needs to be used to convert the input to a string in Python 3.
- The `validate_format()` function was incorrectly parsing the row number and returning only the first digit, e.g. 'a35d' would be returned as row 0, column 3 (should be 34 if zero indexed), down. This was caused by incorrect use of the Python string slicing syntax - the range for the slice was specified as 1:2, but should have been 1:3 so as to include the third character of the string.
- The `validate_move()` function tests the player's move to check whether it is valid according to the rules of the game, and returns information about all the cells that are affected by the move. If the player tries to move a piece off the edge of the board this can lead to the function trying to access an index outside the bounds of the game_board array. This caused an `IndexError` exception, and the programme to crash. `try`/`except` blocks were added to catch these errors and treat them as any other invalid move.
    **However - did we remove these after fixing the 'wrap-around' bug?**

- The `eval_moves` function tests whether there are any valid moves left on the board, and returns `True` or `False`. A False outcome means there are no moves left, and the game is over. After the function was implemented, the game loop continued even when there were no valid moves left. This was challenging to debug. An issue with the `eval_moves` function returing an erroneous `True` value was suspected, a bug was found in the `main()` function. `main()` contains a boolean variable called `valid_move` which is initially set to `False`. A `while` loop continues until the player is deemed to have entered a valid move and this flag is set to `True`. The bug was caused by neglecting to set `valid_move` to `True` after a valid turn, causing an infinite loop asking the play to continue to enter their moves.
- However, after this was fixed continued play testing revealed that `eval_moves()` was indeed returning erroneous `True` values in some circumstances. The function was tested in the `debug.py` file as noted above. Examination of the output led to the conclusion that negative array indices were causing the function to reference the end of the  `board_arr` array in the `GameBoard` class. This meant that valid moves were being detected for cells on the edge of the board with certain configurations of cells on the opposite side. This was fixed with some additional nested `if` statements in `eval_moves()`.
- Fixing this bug in `eval_moves()` then led to the realisation that a similar bug existed in `validate_move()`, meaning the player could move to the opposite side of the board in some circumstances. This was fixed by adding an additional condition to the `if` statements in `validate_move()` to ensure a move is only flagged as valid if a suitable distance from the edge of the board. **Did this eliminate the need for the try/except blocks?**

#### Unresolved bugs
*To complete*

## Deployment
*To complete*

## Credits
### Code
*To complete*
- The deployment terminal was provided by Code Institute.
- The official [Python documentation](https://docs.python.org/3/howto/curses.html) on the curses library was referenced to understand how to use curses
- Code from [this tutorial](https://www.codingem.com/python-range-of-letters/) from codingem was adapated to create a range of letters
- This [Stack Overflow](https://stackoverflow.com/questions/21505871/curses-window-getstr) question helped to resolve a bug caused by the getstr() function returning a value of a type other than a string
- This tutorial from [thispointer.com](https://thispointer.com/count-occurrences-of-a-value-in-numpy-array-in-python/) was referenced to learn how to count the number of occurences of a value in an array

### Content
*To complete*