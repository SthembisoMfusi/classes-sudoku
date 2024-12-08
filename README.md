# Command-Line Sudoku Solver

This program solves Sudoku puzzles from an input file using various logical techniques and backtracking. It features error handling, method selection, and an optional step-by-step mode for observing the backtracking process.

## Features

* **Input from File:** Reads Sudoku puzzles from a text file.
* **Multiple Solving Methods:** Supports solving with:
    * Naked Singles, Pairs, and Triples ("naked")
    * X-Wing technique ("xwing")
    * Backtracking ("backtracking")
    * A combination of all available methods (default)
* **Error Handling:** Includes custom exceptions for invalid files and unsolvable puzzles.
* **Step-by-Step Mode:** Observe the backtracking process one step at a time (using the spacebar). 'q' allows you to escape stepping to find a final solution more quickly. Can choose to escape while already skipping from step for flexibility if certain logical deductions are easier/faster manually
* **Clear Output:** Displays the solved puzzle or indicates if it's unsolvable. Shows location changes, candidate values removed, locations changed and progress reports to user

## Requirements

* Python 3.6 or higher
* `keyboard` library (install using `pip install keyboard`)

## Usage

1. **Save the Code:** Save the provided Python code as `sudoku_solver.py` (or a similar name).
2. **Prepare the Sudoku File:** Create a text file (e.g., `puzzle.txt`) representing the Sudoku puzzle:
    *   Numbers should be space-separated.
    *   Use `0` for empty cells.
    *   Each row of the Sudoku should be on a new line.
3. **Run from the Command Line:**

    ```bash
    python sudoku_solver.py [file_path] [-m method] [-s]
    ```

    *   `file_path`:  *(Optional)* The path to your Sudoku puzzle file. If not specified, `test.txt`  will be solved by default within the same directory or creates `test.txt`. You may need to create the file for the program to run successfully. This filename may also be changed directly by passing the parameter/filename directly if a custom puzzle board is desired to solve which is located outside of your active/selected directory.    
    *   `-m method`: *(Optional)* The solving method to use:
        *   `"naked"`: Naked Singles, Pairs, Triples
        *   `"xwing"`:  X-Wing
        *   `"backtracking"`: Backtracking
        *   *(Default)* If omitted, the solver will try all applicable methods in an efficient order: naked singles/pairs/triples -> X-wing elimination -> Backtracking only when necessary. This usually provides faster overall average solve times with backtracking only required as absolutely necessary in solving puzzles.
    *   `-s`: *(Optional)* Enable step-by-step solving for backtracking and xwing methods only. Press the spacebar to advance to the next step, and `q` to fast forward/exit at any time. X-wing method provides more granular information in steps to inform solving procedure if done manually. The final solution (whether complete, or via backtracking) is always displayed at end. Naked pairs/triples methods will operate/display each applicable set individually when not in step-by-step solving mode or wait per-change if running step mode regardless, same as find naked singles.

## Example

**Solve with Backtracking:**
```bash
python sudoku_solver.py puzzle.txt