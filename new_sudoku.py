class sudoku:
    mod_board = {}
    candidates = {}

    def __init__(self, board):
        self.board = board
        self.board_length = len(board)
        self.possibilities(board)

    def valid_rows(self, board, row, num):
        """
        Check if a number can be placed in the specified row.

        Params:
            board (list): The Sudoku board.
            row (int): The row to check.
            num (int): The number to check.

        Returns:
            bool: True if the number can be placed in the row, False otherwise.
        """
        for j in range(9):
            if board[row][j] == num:
                return False
        return True

    def valid_cols(self, board, col, num):
        """
        Check if a number can be placed in the specified column.

        Params:
            board (list): The Sudoku board.
            col (int): The column to check.
            num (int): The number to check.

        Returns:
            bool: True if the number can be placed in the column, False otherwise.
        """
        for i in range(9):
            if board[i][col] == num:
                return False
        return True

    def valid_cell(self, board, row, col, num):
        """
        Check if a number can be placed in the specified 3x3 block.

        Params:
            board (list): The Sudoku board.
            row (int): The row to check.
            col (int): The column to check.
            num (int): The number to check.

        Returns:
            bool: True if the number can be placed in the 3x3 block, False otherwise.
        """
        corner_row = row - row % 3
        corner_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[corner_row + i][corner_col + j] == num:
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

    def possibilities(self, board):
        """
        Create a dictionary of the original board with all of the cells and the possible numbers that can be placed there.

        Params:
            board (list): The Sudoku board.

        Returns:
            dict: A dictionary with cell positions as keys and a list of possible values as values.
        """
        for i in range(9):
            for j in range(9):
                temp = []
                if board[i][j] == 0:
                    for k in range(1, 10):
                        if self.valid_cell(board, i, j, k) and self.valid_rows(board, i, k) and self.valid_cols(board, j, k):
                            temp.append(k)
                    self.mod_board[(i, j)] = temp
                else:
                    self.mod_board[(i, j)] = [board[i][j]]
        return self.mod_board

    def naked_candidates(self):
        """
        Create a list of how many candidates are in a row and how many choices they have.

        Returns:
            list: A list of naked candidates, including pairs and triples, with updates to the candidate lists.
        """
        naked_candidates = []
        naked_potentials = {2: [], 3: []}
        for key, value in self.mod_board.items():  # separating all of the combination lists by size
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
                self.board[row][col] = value[0]
                y = self.naked_single(value[0], key)
                print(y)

        # Process naked pairs
        for size, candidates in naked_potentials.items():
            if size == 2:  # Naked pairs
                for combo in self.combinations(candidates, size):
                    group_inds = set([key for key, value in self.mod_board.items() if value in combo[0]])
                    for k in range(1, size):
                        group_inds = group_inds.union(set(self.mod_board[combo[k]]))
                    if len(group_inds) == size:
                        naked_candidates.append((list(group_inds), combo))
                        # Call the naked pairs function
                        for pair in combo:
                            self.naked_pairs(pair, [pair[0], pair[1]])

            elif size == 3:  # Naked triples
                for combo in self.combinations(candidates, size):
                    group_inds = set([key for key, value in self.mod_board.items() if value in combo[0]])
                    for k in range(1, size):
                        group_inds = group_inds.union(set(self.mod_board[combo[k]]))
                    if len(group_inds) == size:
                        naked_candidates.append((list(group_inds), combo))
                        # Call the naked triple function
                        self.naked_triple(combo, [combo[0][0], combo[0][1], combo[0][2]])

        return naked_candidates

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
    
    def read_file(self):
        with open(self.file, 'r') as j:
            board = []
            content = j.read().strip().split('\n')
            for i in content:
                temp = []
                line = i.split()
                for j in line:
                    j = int(j)
                    temp.append(j)
                board.append(temp)
        return board



create = board('test.txt').read_file()
solver = sudoku(create)
solver.naked_candidates()
