class sudoku:
    mod_board = {}
    candidates = {}

    def __init__(self, board_data):
        self.board = board_data
        self.board_length = len(self.board)
        self.possibilities()

    def is_valid_placement(self, row, col, num):
        """
        Check if a number can be placed at the specified cell.

        Params:
            row (int): The row index.
            col (int): The column index.
            num (int): The number to place.

        Returns:
            bool: True if the number can be placed, False otherwise.
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


    def naked_single(self, val, pos):
        """
        Generates the naked single statement for a given cell.

        Params:
            val (int): The value that can be placed in the cell.
            pos (tuple): The position (row, col) of the cell.

        Returns:
            str: A message indicating the naked single placement.
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

    def naked_pairs(self, pos, val):
        """
        Generates the naked pair statement for the given pair of cells.

        Params:
            pos (tuple): The position (row, col) of the two cells involved in the pair.
            val (list): The two values that can only go in the given pair of cells.

        Returns:
            None: Prints a message about the disambiguated pair and updates the candidates.
        """
        row = pos[0]
        grid_row = row // 3
        x = ''
        if grid_row == 0:
            x = 'top'
        elif grid_row == 1:
            x = 'middle'
        else:
            x = 'bottom'

        # Print the disambiguated pair statement
        print(f"Disambiguated Pair: The {x} row needs a {val[0]} and a {val[1]}, but only one cell can be a {val[0]}. We fill in {val[0]} and {val[1]}.")

        # Update candidates for the cells involved in the pair
        for other_cell in [pos[0], pos[1]]:
            row, col = other_cell
            # Remove other values from these cells' candidate list
            self.mod_board[other_cell] = [val[0], val[1]]
            print(f"Updated cell {other_cell} candidates to {self.mod_board[other_cell]}")

    def naked_triple(self, pos, val):
        """
        Generates the naked triple statement for the given triple of cells.

        Params:
            pos (tuple): The position (row, col) of the three cells involved in the triple.
            val (list): The three values that can only go in the given triple of cells.

        Returns:
            None: Prints a message about the disambiguated triple and updates the candidates.
        """
        row = pos[0]
        grid_row = row // 3
        x = ''
        if grid_row == 0:
            x = 'top'
        elif grid_row == 1:
            x = 'middle'
        else:
            x = 'bottom'

        # Print the disambiguated triple statement
        print(f"Disambiguated Triple: The {x} row needs {val[0]}, {val[1]}, and {val[2]}. Only these three numbers can be placed in those three cells.")

        # Update candidates for the cells involved in the triple
        for other_cell in pos:
            row, col = other_cell
            # Remove other values from these cells' candidate list
            self.mod_board[other_cell] = val
            print(f"Updated cell {other_cell} candidates to {self.mod_board[other_cell]}")

    def possibilities(self):
        """
        Create a dictionary of the original board with all of the cells and the possible numbers that can be placed there.

        Params:
            board (list): The Sudoku board.

        Returns:
            dict: A dictionary with cell positions as keys and a list of possible values as values.
        """
        for row in range(self.board_length):
            for col in range(self.board_length):
                if self.board[row][col] == 0:  # we are looking for empty cells which are represented with a 0
                    self.mod_board[(row, col)] = [
                        num for num in range(1, 10) if self.is_valid_placement(row, col, num)
                    ]
                else:  
                    self.mod_board[(row, col)] = self.board[row][col]
        return self.mod_board

    def naked_candidates(self):
        """
        Create a list of how many candidates are in a row and how many choices they have.

        Returns:
            list: A list of naked candidates, including pairs and triples, with updates to the candidate lists.
        """
        naked_candidates = []
        naked_potentials = {2: [], 3: []}
        
        # Separating all of the combination lists by size
        for key, value in self.mod_board.items():
            if isinstance(value, list):
                if len(value) == 1:
                    naked_candidates.append((key, value))
                elif len(value) == 2:
                    naked_potentials[2].append((key, value))
                elif len(value) == 3:
                    naked_potentials[3].append((key, value))

        # Process naked singles
        for key, value in naked_candidates:
            if isinstance(value, list) and len(value) == 1:
                row, col = key
                self.place(row, col, value[0])  # Use place method to update the board
                y = self.naked_single(value[0], key)
                print(y)

                # Process naked pairs
        for size, candidates in naked_potentials.items():
            if size == 2:  # Naked pairs
                for combo in self.combinations(candidates, size):
                    # Initialize group_inds with empty sets
                    group_inds = set()

                    # Unpack each pair in combo
                    for pair in combo:
                        row, col = pair  # pair is a tuple (row, col)
                        group_inds.add((row, col))

                    # Check if the number of elements in group_inds equals size
                    if len(group_inds) == size:
                        naked_candidates.append((list(group_inds), combo))
                        # Call the naked pairs function
                        for pair in combo:
                            self.naked_pairs(pair, [pair[0], pair[1]])

            elif size == 3:  # Naked triples
                for combo in self.combinations(candidates, size):
                    # Initialize group_inds with empty sets
                    group_inds = set()

                    # Unpack each tuple in combo and update group_inds with individual (row, col)
                    for item in combo:
                        for pair in item:
                            row, col = pair
                            group_inds.add((row, col))

                    # Check if the number of elements in group_inds equals size
                    if len(group_inds) == size:
                        naked_candidates.append((list(group_inds), combo))
                        # Call the naked triple function
                        self.naked_triple(combo, [combo[0][0], combo[0][1], combo[0][2]])

        return naked_candidates



    def update_candidates(self, row, col, value, remove=True):
        """
        Update the candidates of cells in the same row, column, and subgrid
        when a value is placed or erased.

        Params:
            row (int): Row index of the cell being modified.
            col (int): Column index of the cell being modified.
            value (int): The value to place or erase.
            remove (bool): If True, remove the value from candidates; otherwise, add it back.
        """
        for i in range(self.board_length):
            # Update candidates in the row and column
            if isinstance(self.mod_board.get((row, i)), list):
                if remove:
                    self.mod_board[(row, i)].remove(value) if value in self.mod_board[(row, i)] else None
                else:
                    if self.is_valid_placement(row, i, value):
                        self.mod_board[(row, i)].append(value)

            if isinstance(self.mod_board.get((i, col)), list):
                if remove:
                    self.mod_board[(i, col)].remove(value) if value in self.mod_board[(i, col)] else None
                else:
                    if self.is_valid_placement(i, col, value):
                        self.mod_board[(i, col)].append(value)

        # Update candidates in the block
        corner_row, corner_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                cell = (corner_row + i, corner_col + j)
                if isinstance(self.mod_board.get(cell), list):
                    if remove:
                        self.mod_board[cell].remove(value) if value in self.mod_board[cell] else None
                    else:
                        if self.is_valid_placement(cell[0], cell[1], value):
                            self.mod_board[cell].append(value)

    def place(self, row, col, value):
        """
        Place a value in the board and update candidates.

        Params:
            row (int): Row index.
            col (int): Column index.
            value (int): The value to place in the cell.
        """
        self.board[row][col] = value
        self.mod_board[(row, col)] = value  # Mark the cell as solved
        self.update_candidates(row, col, value, remove=True)

    def erase(self, row, col):
        """
        Erase a value from the board and restore candidates.

        Params:
            row (int): Row index.
            col (int): Column index.
        """
        erased_value = self.board[row][col]
        self.board[row][col] = 0
        self.mod_board[(row, col)] = [
            num for num in range(1, 10) if self.is_valid_placement(row, col, num)
        ]
        self.update_candidates(row, col, erased_value, remove=False)

    def backtracking_solve(self):
        """
        Recursive backtracking solver that uses the `mod_board` candidates.
        Returns True if the board is solved, otherwise False.
        """
        for (row, col), candidates in self.mod_board.items():
            if self.board[row][col] == 0:  # Find the first empty cell
                for candidate in candidates:
                    if self.is_valid_placement(row, col, candidate):
                        self.board[row][col] = candidate  # Place the candidate
                        self.update_candidates(row, col, candidate, remove=True)

                        if self.backtracking_solve():
                            return True

                        # Backtrack
                        self.board[row][col] = 0
                        self.update_candidates(row, col, candidate, remove=False)

                return False  # Trigger backtracking
        return self.is_complete()
    def x_wing_elimination(self):
        """
        Apply the X-Wing pattern elimination to reduce candidates.
        """
        for num in range(1, 10):
            row_positions = [[] for _ in range(9)]
            col_positions = [[] for _ in range(9)]

            # Collect possible placements for the number
            for (row, col), candidates in self.mod_board.items():
                if num in candidates:
                    row_positions[row].append(col)
                    col_positions[col].append(row)

            # Find rows with identical column candidates
            for r1 in range(9):
                for r2 in range(r1 + 1, 9):
                    if row_positions[r1] == row_positions[r2] and len(row_positions[r1]) == 2:
                        cols = row_positions[r1]
                        for row in range(9):
                            if row not in (r1, r2):
                                for col in cols:
                                    if num in self.mod_board.get((row, col), []):
                                        self.mod_board[(row, col)].remove(num)
    def solve(self):
        """
        Attempt to solve the Sudoku puzzle using logical techniques
        and backtracking as a fallback.
        """
        while True:
            prev_board = [row[:] for row in self.board]

            # Apply logical solving techniques
            self.naked_candidates()
            self.x_wing_elimination()

            # If no progress is made, stop logical techniques
            if prev_board == self.board:
                break

        # Use backtracking if logical techniques are insufficient
        if not self.is_complete():
            self.backtracking_solve()
    def is_complete(self):
        """
        Check if the board is fully and correctly solved.
        """
        for row in self.board:
            if 0 in row:
                return False
        return True
    def combinations(self, lst, r):
        """
        Generate all r-length combinations of the list.

        Params:
            lst (list): The input elements to combine.
            r (int): The length of each combination.

        Yields:
            tuple: Each combination as an r-length tuple.
        """
        if r == 0:
            yield ()
        elif len(lst) < r:
            return
        else:
            for i in range(len(lst)):
                for rest in self.combinations(lst[i+1:], r-1):
                    yield (lst[i],) + rest


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



create = board('test.txt')
solver = sudoku(create.board)
solver.naked_candidates()
