import copy

class sudoku:
    def __init__(self, board_data):
        self.board = board_data
        self.board_length = len(self.board)
        self.mod_board = {}  # Initialize mod_board
        self.backtracking_mod_board = {}  # Initialize backtracking_mod_board
        self.possibilities()  # Calculate initial possibilities

    def copy_possibilities(self):
        """
        Creates a copy of the possibilities for backtracking.
        """
        self.backtracking_mod_board = copy.deepcopy(self.mod_board)
    def display_grid(self):
        for i in self.board:
            print((" ".join(map(str, i)) + "\n"))
    def is_valid_placement(self, row, col, num):
        """
        Check if a number can be placed at the specified cell.
        """
        if num in self.board[row]:
            return False

        if num in [self.board[i][col] for i in range(self.board_length)]:
            return False

        corner_row, corner_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if self.board[corner_row + i][corner_col + j] == num:
                    return False

        return True

    def naked_single_message(self, val, pos):
        """
        Generates the naked single statement for a given cell.
        """
        row, col = pos
        grid_row = row // 3
        grid_col = col // 3
        x = ''
        if grid_row == 0:
            if grid_col == 0:
                x = "Top-left"
            elif grid_col == 1:
                x = "Top-center"
            else:
                x = "Top-right"
        elif grid_row == 1:
            if grid_col == 0:
                x = "Middle-left"
            elif grid_col == 1:
                x = "Middle-center"
            else:
                x = "Middle-right"
        else:
            if grid_col == 0:
                x = "Bottom-left"
            elif grid_col == 1:
                x = "Bottom-center"
            else:
                x = "Bottom-right"
        return f'Naked Single: {x} cell can only be a {val}'

    def naked_pairs_message(self, pos, val):
        """
        Generates the message for a naked pair.
        """
        row, col = pos
        grid_row = row // 3
        x = ''
        if grid_row == 0:
            x = 'top'
        elif grid_row == 1:
            x = 'middle'
        else:
            x = 'bottom'

        return f"Disambiguated Pair: The {x} row needs a {val[0]} and a {val[1]}, but only one cell can be a {val[0]}. We fill in {val[0]} and {val[1]}."

    def naked_triple_message(self, pos, val):
        """
        Generates the message for a naked triple.
        """
        row, _ = pos[0]  # Get the row from the first cell in the triple
        grid_row = row // 3
        x = ''
        if grid_row == 0:
            x = 'top'
        elif grid_row == 1:
            x = 'middle'
        else:
            x = 'bottom'

        return f"Disambiguated Triple: The {x} row needs {val[0]}, {val[1]}, and {val[2]}. Only these three numbers can be placed in those three cells."

    def possibilities(self):
        """
        Create a dictionary of possible numbers for each empty cell.
        """
        for row in range(self.board_length):
            for col in range(self.board_length):
                if self.board[row][col] == 0:
                    self.mod_board[(row, col)] = [
                        num for num in range(1, 10) if self.is_valid_placement(row, col, num)
                    ]
                else:
                    self.mod_board[(row, col)] = self.board[row][col]

    def find_naked_singles(self):
        """Identifies and places naked singles."""
        change_made = False
        for (row, col), candidates in self.mod_board.items():
            if isinstance(candidates, list) and len(candidates) == 1:
                value = candidates[0]
                self.place(row, col, value)
                self.display_grid()
                print(self.naked_single_message(value, (row, col)))
                change_made = True
        return change_made

    def find_naked_pairs_triples(self, size):
        """Identifies and processes naked pairs (size=2) or triples (size=3)."""
        change_made = False
        for group_type in ["row", "col", "block"]:
            for i in range(9):
                # Collect cells with 'size' number of candidates in the group
                if group_type == "row":
                    cells = [(i, j) for j in range(9) if isinstance(self.mod_board.get((i, j)), list) and len(self.mod_board[(i, j)]) == size]
                elif group_type == "col":
                    cells = [(j, i) for j in range(9) if isinstance(self.mod_board.get((j, i)), list) and len(self.mod_board[(j, i)]) == size]
                else:  # block
                    row_start = (i // 3) * 3
                    col_start = (i % 3) * 3
                    cells = [(row_start + r, col_start + c) for r in range(3) for c in range(3) if isinstance(self.mod_board.get((row_start + r, col_start + c)), list) and len(self.mod_board[(row_start + r, col_start + c)]) == size]

                # Generate combinations of cells
                for combination in self.combinations(cells, size):
                    values = set()
                    for cell in combination:
                        values.update(self.mod_board[cell])

                    if len(values) == size:
                        # Naked pair/triple found
                        if self.process_naked_group(combination, list(values), group_type, i):
                            change_made = True
        return change_made

    def process_naked_group(self, combination, values, group_type, index):
        """Processes a found naked pair or triple and updates candidates."""
        change_made = False

        # Iterate over cells in the same group (row, column, or block)
        if group_type == "row":
            for col in range(9):
                cell = (index, col)
                if cell not in combination and isinstance(self.mod_board.get(cell), list):
                    for value in values:
                        if value in self.mod_board[cell]:
                            self.mod_board[cell].remove(value)
                            change_made = True
        elif group_type == "col":
            for row in range(9):
                cell = (row, index)
                if cell not in combination and isinstance(self.mod_board.get(cell), list):
                    for value in values:
                        if value in self.mod_board[cell]:
                            self.mod_board[cell].remove(value)
                            change_made = True
        else:  # block
            row_start = (index // 3) * 3
            col_start = (index % 3) * 3
            for r in range(3):
                for c in range(3):
                    cell = (row_start + r, col_start + c)
                    if cell not in combination and isinstance(self.mod_board.get(cell), list):
                        for value in values:
                            if value in self.mod_board[cell]:
                                self.mod_board[cell].remove(value)
                                change_made = True

        if change_made:
            if len(values) == 2:
                self.display_grid()
                print(self.naked_pairs_message(combination[0], values))
            elif len(values) == 3:
                self.display_grid()
                print(self.naked_triple_message(combination, values))

        return change_made

    def naked_candidates(self):
        """
        Applies naked singles, pairs, and triples techniques repeatedly.
        """
        while True:
            made_changes = self.find_naked_singles()
            made_changes |= self.find_naked_pairs_triples(2)
            made_changes |= self.find_naked_pairs_triples(3)
            if not made_changes:
                break

    def place(self, row, col, value):
        """Place a value and update candidates (forward checking)."""
        self.board[row][col] = value
        self.mod_board[(row, col)] = value
        self.forward_check(row, col, value, remove=True)

    def erase(self, row, col):
        """Erase a value and update candidates (forward checking)."""
        erased_value = self.board[row][col]
        self.board[row][col] = 0
        self.mod_board[(row, col)] = [
            num for num in range(1, 10) if self.is_valid_placement(row, col, num)
        ]
        self.forward_check(row, col, erased_value, remove=False)

    def forward_check(self, row, col, value, remove):
        """Update candidates of related cells (used for forward checking)."""
        for i in range(self.board_length):
            # Update row and column
            if isinstance(self.mod_board.get((row, i)), list):
                if remove:
                    if value in self.mod_board[(row, i)]:
                        self.mod_board[(row, i)].remove(value)
                elif self.is_valid_placement(row, i, value):
                    self.mod_board[(row, i)].append(value)

            if isinstance(self.mod_board.get((i, col)), list):
                if remove:
                    if value in self.mod_board[(i, col)]:
                        self.mod_board[(i, col)].remove(value)
                elif self.is_valid_placement(i, col, value):
                    self.mod_board[(i, col)].append(value)

        # Update block
        corner_row, corner_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                cell = (corner_row + i, corner_col + j)
                if isinstance(self.mod_board.get(cell), list):
                    if remove:
                        if value in self.mod_board[cell]:
                            self.mod_board[cell].remove(value)
                    elif self.is_valid_placement(cell[0], cell[1], value):
                        self.mod_board[cell].append(value)

    def forward_check_backtracking(self, row, col, value, remove):
        """
        Update candidates of related cells in backtracking_mod_board.
        """
        for i in range(self.board_length):
            # Update row and column
            if isinstance(self.backtracking_mod_board.get((row, i)), list):
                if remove:
                    if value in self.backtracking_mod_board[(row, i)]:
                        self.backtracking_mod_board[(row, i)].remove(value)
                elif self.is_valid_placement(row, i, value):
                    self.backtracking_mod_board[(row, i)].append(value)

            if isinstance(self.backtracking_mod_board.get((i, col)), list):
                if remove:
                    if value in self.backtracking_mod_board[(i, col)]:
                        self.backtracking_mod_board[(i, col)].remove(value)
                elif self.is_valid_placement(i, col, value):
                    self.backtracking_mod_board[(i, col)].append(value)

        # Update block
        corner_row, corner_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                cell = (corner_row + i, corner_col + j)
                if isinstance(self.backtracking_mod_board.get(cell), list):
                    if remove:
                        if value in self.backtracking_mod_board[cell]:
                            self.backtracking_mod_board[cell].remove(value)
                    elif self.is_valid_placement(cell[0], cell[1], value):
                        self.backtracking_mod_board[cell].append(value)

    def backtracking_solve(self):
        """
        Recursive backtracking solver with MRV heuristic.
        """
        self.copy_possibilities()  # Create a copy for backtracking

        def solve_recursive():
            # Find cell with fewest candidates (MRV)
            min_candidates = 10
            best_cell = None
            for (row, col), candidates in self.backtracking_mod_board.items():
                if self.board[row][col] == 0:
                    num_candidates = len(candidates)
                    if num_candidates < min_candidates:
                        min_candidates = num_candidates
                        best_cell = (row, col)

            if best_cell is None:  # No empty cell found
                return self.is_complete()

            row, col = best_cell
            for candidate in self.backtracking_mod_board[best_cell]:
                if self.is_valid_placement(row, col, candidate):
                    self.place(row, col, candidate)

                    # Forward checking for backtracking
                    self.forward_check_backtracking(row, col, candidate, remove=True)

                    if solve_recursive():
                        return True

                    # Backtrack
                    self.erase(row, col)

                    # Restore candidates
                    self.forward_check_backtracking(row, col, candidate, remove=False)

            return False

        return solve_recursive()

    def x_wing_elimination(self):
        """
        Apply the X-Wing pattern elimination to reduce candidates.
        """
        for num in range(1, 10):
            row_positions = [[] for _ in range(9)]
            col_positions = [[] for _ in range(9)]

            # Collect possible placements for the number
            for (row, col), candidates in self.mod_board.items():
                if isinstance(candidates, list) and num in candidates:
                    row_positions[row].append(col)
                    col_positions[col].append(row)

            # Find rows with identical column candidates
            for r1 in range(9):
                for r2 in range(r1 + 1, 9):
                    if row_positions[r1] == row_positions[r2] and len(row_positions[r1]) == 2:
                        cols = row_positions[r1]

                        # Eliminate the candidate from other cells in the same columns
                        for row in range(9):
                            if row not in (r1, r2):
                                for col in cols:
                                    if isinstance(self.mod_board.get((row, col)), list) and num in self.mod_board.get((row, col), []):
                                        self.mod_board[(row, col)].remove(num)

    def is_complete(self):
        """
        Check if the board is fully and correctly solved.
        """
        for row in self.board:
            if 0 in row:
                return False

        # Check rows
        for row in self.board:
            if len(set(row)) != 9:
                return False

        # Check columns
        for col in range(9):
            if len(set(self.board[row][col] for row in range(9))) != 9:
                return False

        # Check 3x3 blocks
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block = [self.board[row][col] for row in range(i, i + 3) for col in range(j, j + 3)]
                if len(set(block)) != 9:
                    return False

        return True

    def combinations(self, lst, r):
        """
        Generate all r-length combinations of the list (without itertools).
        """
        n = len(lst)
        if r > n:
            return
        if r == 0:
            yield ()
            return
        if r == n:
            yield tuple(lst)
            return

        for comb in self.combinations(lst[1:], r - 1):
            yield (lst[0],) + comb
        for comb in self.combinations(lst[1:], r):
            yield comb

    def solve(self):
        """
        Attempt to solve the Sudoku puzzle using logical techniques
        and backtracking as a fallback.
        """
        while True:
            prev_board = [row[:] for row in self.board]

            # Apply logical solving techniques
            print("Using naked candidates to solve...")
            self.naked_candidates()
            if not self.is_complete():
                print("Using x wing to solve...")
                self.x_wing_elimination()

            # If no progress is made, stop logical techniques
            if prev_board == self.board or self.is_complete():
                break

        # Use backtracking if logical techniques are insufficient
        if not self.is_complete():
            print("Using backtracking to solve...")
            if self.backtracking_solve():
                print("Sudoku solved!")
            else:
                print("Sudoku unsolvable!")
        else:
            print("Sudoku solved using logical techniques!")

        # Print the solved board (or the partially solved board)
        self.display_grid()

class board:
    def __init__(self, file):
        self.file = file
        self.board = self.read_file()

    def read_file(self):
        with open(self.file, 'r') as f:
            board = []
            content = f.read().strip().split('\n')
            for i in content:
                temp = []
                line = i.split()
                for j in line:
                    j = int(j)
                    temp.append(j)
                board.append(temp)
        return board

# Example usage:
create = board('test.txt')  # Replace 'test.txt' with your Sudoku file
solver = sudoku(create.board)
solver.solve()