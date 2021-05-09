from tttg_menu_printer import mp_print_menu


class TTTGame:
    def __init__(self):
        self.N = 3
        self.CIRCLE = 1
        self.EMPTY = 0
        self.CROSS = 2
        self.board = [[self.EMPTY for i in range(self.N)] for i in range(self.N)]
        self.AI_row = 0
        self.AI_col = 0

    def clear_board(self):
        for i in range(self.N):
            for j in range(self.N):
                self.board[i][j] = self.EMPTY

    def draw_border(self):
        boarder = " " * 14
        for i in range(self.N):
            if i == self.N - 1:
                boarder += "---"
            else:
                boarder += "----"
        boarder += " \n"
        return boarder

    def make_move(self, row, col, seed):
        self.board[row][col] = seed

    def is_cell_empty(self, row, col):
        return self.board[row][col] == self.EMPTY

    def ai_move(self):
        found = False
        for i in range(self.N):
            for j in range(self.N):
                if self.board[i][j] == self.EMPTY:
                    self.board[i][j] = self.CROSS
                    self.AI_row = i
                    self.AI_col = j
                    found = True
                    break
            if found:
                break

    def get_ai_row(self):
        return self.AI_row

    def get_ai_col(self):
        return self.AI_col

    def print_board(self, ):
        tab = " " * 15
        # Draw columns
        for i in range(self.N):
            tab += str(i + 1) + "   "
        tab += "\n"

        tab += self.draw_border()
        row_char = 'A'

        for i in range(self.N):
            tab += "           " + row_char
            tab += " | "
            for j in range(self.N):
                if self.board[i][j] == self.CROSS:
                    tab += "X" + " | "
                elif self.board[i][j] == self.EMPTY:
                    tab += " " + " | "
                else:
                    tab += "O" + " | "
            tab += "\n"
            row_char = chr(ord(row_char) + 1)  # increase row char from A -> B -> C

        self.draw_border()
        tab += ""
        return tab

    def check_for_win(self, row, col, seed):
        # Return true if a row of 'seed' was played.
        for i in range(self.N):
            if self.board[row][i] == seed:
                if i == self.N - 1:
                    return True
            else:
                break
        # Return true if a column of 'seed' was played.
        for i in range(self.N):
            if self.board[i][col] == seed:
                if i == self.N - 1:
                    return True
            else:
                break

        # Return true if diagonal/anti-diagonal of 'seed' was played.
        win = True
        for i in range(self.N):
            for j in range(self.N):
                if i == j:
                    if self.board[i][j] == seed:
                        if i == self.N - 1:
                            return True
                        else:
                            win = False
                            break
            if not win:
                break

        win = True
        for i in range(self.N):
            for j in range(self.N):
                if i + j == 2:
                    if self.board[i][j] == seed:
                        if i == self.N - 1:
                            return True
                    else:
                        win = False
                        break
            if not win:
                break

        return win

    def is_valid_move(self, move):
        if len(move) != 2:
            return False
        if move[0] != 'a' and move[0] != 'b' and move[0] != 'c':
            return False
        if int(move[1]) > 3 or int(move[1]) < 1:
            return False
        # calculate row from the unicode equivalent of the row char used
        # Find the distance the desired row (move[0]) from the first row (A)
        # values are either 0, 1, or 2.
        if not self.is_cell_empty(ord(move[0]) - ord('a'), int(move[1]) - 1):
            return False

        return True

    @staticmethod
    def is_draw(move_num):
        return move_num == 6

    @staticmethod
    def print_menu(client_start):
        return mp_print_menu(client_start)
