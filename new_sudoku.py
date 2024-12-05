class sudoku:
    mod_board = {}
    candidates = {}
    def __init__(self, board) -> None:
        self.board = board
    def valid_rows(self,board, row, num):
        '''checks if the number can be added on the row'''
        for j in range(9):
            if board[row][j] == num:
                return False
        return True
    def valid_cols(self,board, col, num):
        '''checks if the number can be added on the coloumn'''
        for i in range(9):
            if board[i][col] == num:
                return False
        return True
    def valid_cell(self, board, row, col, num):
        '''checks if the number can be added in the 3x3 block'''
        corner_row = row - row % 3
        corner_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[corner_row + i][corner_col + j] == num:
                    return False
        return True
    def naked_single(self, row, col,val):
        '''generates the naked single statement'''
        grid_row = row // 3
        grid_col = col // 3
        x= ''
        if grid_row == 0:
            if grid_col == 0:
                x = "Top-left"
            elif grid_col == 1:
                x = "Top-center"
            else:
                x = "Top-right"
        elif grid_row == 1:
            if grid_col == 0:
                x= "Middle-left"
            elif grid_col == 1:
                x = "Middle-center"
            else:
                x = "Middle-right"
        else:
            if grid_col == 0:
                x =  "Bottom-left"
            elif grid_col == 1:
                x =  "Bottom-center"
            else:
                x = "Bottom-right"    
        return f'Naked Single: {x} cell can only be a {val}'
    def naked_pairs(self,row,val):
        '''generates the naked pair statement'''
        grid_row = row // 3
        x= ''
        if grid_row ==0:
            x = 'top'
        elif grid_row ==1:
            x = 'middle'
        else:
            x = 'bottom'
        return f'Disambiguated Pair: The {x} row needs a {val[0]} and a {val[1]}, but only one cell can be a 2. We fill in 6 and 2.'
    def naked_triple(self, row, col, val):
        '''generates the naked triple statement'''
        pass
    def possibilities(self,board, row, col):
        '''creates a dictionary of the original board with all of the cells and the possible numbers that can be put there'''
        for line,count in enumerate(board):
            cells = []
            for j in line: 
                if j !=0:
                    cells.append(j)
                temp = []           
                for i in range(9):
                    if self.valid_cell(board,row,col,i) and self.valid_rows(board, row, col, i) and self.valid_cell( board, row, col, i):
                        temp.append(i)
                cells.append(temp)
            self.mod_board[count] = cells
        return self.mod_board
    def potential_candidates(self,board,val):
        '''checks if a cell is a valid naked candidate'''
        nakeds = self.generate_naked_board()

        for row in nakeds.values():
            for i in row:
                pass
            
    def generate_naked_board(self):
        '''creates a dictionary for all rows containing their naked candidates'''
        naked_board = {}
        for i in range(9):
            naked_board[i] = self.naked_candidates(i, self.mod_board[i])
        return naked_board

    def naked_candidates(self,pos, board):
        '''creates a list of how many candidates in a row and how many choices they have'''
        naked_candidates = {1: [], 2: [], 3: [], 4: []}
        for group in self.mod_board:
            for i, sub in enumerate(group):
                if 1 <= len(sub) <= 4:  
                    matching_cells = [j for j, cell in enumerate(group) if cell == sub]
                    if len(matching_cells) == len(sub):  
                        naked_candidates[len(sub)].append((sub, matching_cells))
        for size, candidates in naked_candidates.items():
            if size == 1:
                
                for candidate, cells in candidates:
                   y = self.naked_single(pos,cells,candidate)
                   print(y)
            elif size ==2:
                y = self.naked_pairs()
        return naked_candidates
        

class board:
    def __init__(self,file):
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
print(create)
solver = sudoku(create)