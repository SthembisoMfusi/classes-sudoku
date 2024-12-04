class sudoku:
    empties = {}
    def __init__(self) -> None:
        pass
    def read_file(self, file):
        board = []
        with open(file, 'r') as j:
            content = j.read().strip().split('\n')
            for i in content:
                temp = []
                line = i.split()
                for j in line:
                    j = int(j)
                    temp.append(j)
                board.append(temp)
        return board
    def valid_rows(self,board, row, col, num):
        for i in range(9):
            if board[i][col] == num:
                return False
        for j in range(9):
            if board[row][j] == num:
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
    def possibilities(self,board, row, col):
        for i in range(9):
            if self.valid_cell(board,row,col,i) and self.valid_rows(board, row, col, i):
                self.empties[(row,col)] = i
        return self.empties
    def naked_candidates(self,board):
        pass


