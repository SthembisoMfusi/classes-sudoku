class sudoku:
    mod_board = {}
    candidates = {}
    def __init__(self, board) -> None:
        self.board = board
    def valid_rows(self,board, row, num):
        for j in range(9):
            if board[row][j] == num:
                return False
        return True
    def valid_cols(self,board, col, num):
        for i in range(9):
            if board[i][col] == num:
                return False
        return True
    def valid_cell(self, board, row, col, num):
        corner_row = row - row % 3
        corner_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[corner_row + i][corner_col + j] == num:
                    return False
        return True
    def naked_single(self, row, col,val):
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
        return f'Naked Single: Top {x} cell can only be a {val}'
    def naked_pairs(self,row,col,val):
        return f'Disambiguated Pair: The bottom row needs a 2 and a 6, but only one cell can be a 2. We fill in 6 and 2.'
    def naked_triple(self, row, col, val):
        pass
    def possibilities(self,board, row, col):
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
            self.mod_board[count + 1] = cells
        return self.mod_board
    def potential_candidates(self,mod_board):
       for line,cnt in enumerate(self.mod_board.values()):
            self.naked_candidates( cnt,line)
            
                          
    def naked_candidates(self,pos, group):
        naked_candidates = {1: [], 2: [], 3: [], 4: []} 
        for i, sub in enumerate(group):
            if 1 <= len(sub) <= 4:  
                matching_cells = [j for j, cell in enumerate(group) if cell == sub]
                if len(matching_cells) == len(sub):  
                    naked_candidates[len(sub)].append((sub, matching_cells))
        for size, candidates in naked_candidates.items():
            if size == 1:
                y = self.naked_single(pos, cells)
                for candidate, cells in candidates:
                   print(f"Naked single: {y} cell can only be {candidate}")
            elif size ==2:
                y = self.naked_pairs()
        return naked_candidates
        

class board:
    
    def __init__(self, file):
        self.board = []
    def read_file(self, file):
        with open(file, 'r') as j:
            content = j.read().strip().split('\n')
            for i in content:
                temp = []
                line = i.split()
                for j in line:
                    j = int(j)
                    temp.append(j)
                self.board.append(temp)
        return self.board
