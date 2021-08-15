from pieces import King, Knight, Queen, Pawn, Bishop, Rook
import numpy as np
from copy import deepcopy


class ChessGame:
    def __init__(self):
        # white:0 black:1
        self.board = [
            [Rook(0, 0, 1), Pawn(0, 1, 1), None, None, None, None, Pawn(0, 6, 0), Rook(0, 7, 0)],
            [Knight(1, 0, 1), Pawn(1, 1, 1), None, None, None, None, Pawn(1, 6, 0), Knight(1, 7, 0)],
            [Bishop(2, 0, 1), Pawn(2, 1, 1), None, None, None, None, Pawn(2, 6, 0), Bishop(2, 7, 0)],
            [King(3, 0, 1), Pawn(3, 1, 1), None, None, None, None, Pawn(3, 6, 0), King(3, 7, 0)],
            [Queen(4, 0, 1), Pawn(4, 1, 1), None, None, None, None, Pawn(4, 6, 0), Queen(4, 7, 0)],
            [Bishop(5, 0, 1), Pawn(5, 1, 1), None, None, None, None, Pawn(5, 6, 0), Bishop(5, 7, 0)],
            [Knight(6, 0, 1), Pawn(6, 1, 1), None, None, None, None, Pawn(6, 6, 0), Knight(6, 7, 0)],
            [Rook(7, 0, 1), Pawn(7, 1, 1), None, None, None, None, Pawn(7, 6, 0), Rook(7, 7, 0)],
        ]
        self.turn = 0

    def legal_moves(self, pseudo=False):
        pseudo_legal_moves = []
        legal_moves = []
        for i in range(8):
            for j in range(8):
                selected_piece = self.board[i][j]
                if selected_piece is not None:
                    if selected_piece.colour != self.turn:
                        continue
                    for x in range(8):
                        for y in range(8):
                            selected_move = self.board[x][y]
                            if selected_piece == selected_move:
                                continue
                            if selected_move is not None:
                                if selected_move.colour == self.turn:
                                    continue

                            if not pseudo:
                                # castling
                                if isinstance(selected_piece, King):
                                    # rules: king not moved, King not in check, not pass through check, rook not moved

                                    # Queen side
                                    if selected_move is not None:
                                        if selected_piece.moved == False and isinstance(selected_move,
                                                                                        Rook) and selected_move.moved == False and x == 7:
                                            # check if intersecting
                                            if self.board[i + 1][j] != None or self.board[i + 2][j] != None or \
                                                    self.board[i + 3][j] != None:
                                                continue
                                            # check if in check
                                            if self.is_check((i, j), (i + 1, j)) or self.is_check((i, j), (
                                            i + 2, j)) or self.in_check():
                                                continue

                                            legal_moves.append(((i, j), (i + 2, j)))


                                    # King side
                                    if selected_move is not None:
                                        if selected_piece.moved == False and isinstance(selected_move,
                                                                                        Rook) and selected_move.moved == False and x == 0:
                                            # check if intersecting
                                            if self.board[i - 1][j] != None or self.board[i - 2][j] != None:
                                                continue
                                            # check if in check
                                            if self.is_check((i, j), (i - 1, j)) or self.is_check((i, j), (i-2,j)) or self.in_check():
                                                continue

                                            legal_moves.append(((i, j), (i - 2, j)))

                            if selected_piece.legal(x, y, self.board[x][y] is not None):

                                intersecting = False
                                if isinstance(selected_piece, (Bishop)):
                                    dist = abs(x - i)
                                    sign = int((x - i) / abs(x - i))
                                    if i - x == j - y:
                                        if sign == 1:
                                            for a in range(sign, dist):
                                                if self.board[i + a][j + a] != None:
                                                    intersecting = True
                                        else:
                                            for a in range(dist * sign + 1, 0):
                                                if self.board[i + a][j + a] != None:
                                                    intersecting = True
                                    else:
                                        if sign == 1:
                                            for a in range(sign, dist):
                                                if self.board[i + a][j - a] != None:
                                                    intersecting = True
                                        else:
                                            for a in range(dist * sign + 1, 0):
                                                if self.board[i + a][j - a] != None:
                                                    intersecting = True

                                if isinstance(selected_piece, (Rook)):
                                    dist = max(abs(x - i), abs(y - j))
                                    sign = int((x - i + y - j) / dist)
                                    if i == x:
                                        if sign == 1:
                                            for a in range(sign, dist * sign):
                                                if self.board[i][j + a] != None:
                                                    intersecting = True
                                        else:
                                            for a in range(dist * sign + 1, 0):
                                                if self.board[i][j + a] != None:
                                                    intersecting = True
                                    else:
                                        if sign == 1:
                                            for a in range(sign, dist * sign):
                                                if self.board[i + a][j] != None:
                                                    intersecting = True
                                        else:
                                            for a in range(dist * sign + 1, 0):
                                                if self.board[i + a][j] != None:
                                                    intersecting = True

                                if isinstance(selected_piece, Queen):
                                    dist = (x - i)
                                    dist_h = max(abs(x - i), abs(y - j))

                                    if i == x:
                                        sign = int((x - i + y - j) / dist_h)
                                        if sign == 1:
                                            for a in range(sign, dist_h * sign):
                                                if self.board[i][j + a] != None:
                                                    intersecting = True
                                        else:
                                            for a in range(dist_h * sign + 1, 0):
                                                if self.board[i][j + a] != None:
                                                    intersecting = True
                                    elif j == y:
                                        sign = int((x - i + y - j) / dist_h)
                                        if sign == 1:
                                            for a in range(sign, dist_h * sign):
                                                if self.board[i + a][j] != None:
                                                    intersecting = True
                                        else:
                                            for a in range(dist_h * sign + 1, 0):
                                                if self.board[i + a][j] != None:
                                                    intersecting = True
                                    elif i - x == j - y:
                                        sign = int((x - i) / abs(x - i))
                                        if sign == 1:
                                            for a in range(sign, dist):
                                                if self.board[i + a][j + a] != None:
                                                    intersecting = True
                                        else:
                                            for a in range(dist + 1, 0):
                                                if self.board[i + a][j + a] != None:
                                                    intersecting = True
                                    else:
                                        sign = int((x - i) / abs(x - i))
                                        if sign == 1:
                                            for a in range(sign, dist):
                                                if self.board[i + a][j - a] != None:
                                                    intersecting = True
                                        else:
                                            for a in range(dist + 1, 0):
                                                if self.board[i + a][j - a] != None:
                                                    intersecting = True
                                if type(selected_piece) == Pawn:
                                    if y - j == 2:
                                        if self.board[i][j + 1] != None:
                                            intersecting = True



                                if not intersecting:
                                    pseudo_legal_moves.append(((i, j), (x, y)))

                            if type(self.board[i][j]) == Pawn:
                                if type(self.board[x][y]) == Pawn and abs(x-i) == 1 and y==j:
                                    if self.board[x][y].passant:
                                        pseudo_legal_moves.append(((i,j),(x,int(y+(self.turn-0.5)*2))))
        if pseudo:
            return pseudo_legal_moves
        else:

            for from_, to_ in pseudo_legal_moves:
                if not self.is_check(from_, to_):
                    legal_moves.append((from_, to_))
            return legal_moves

    def to_arr(self):
        game_board = []
        for i in range(8):
            arr = []
            for j in range(8):
                arr.append(self.board[i][j].num() if self.board[i][j] is not None else 0)
            game_board.append(arr)

        return game_board

    def move_piece(self, from_piece, to_piece):

        if type(self.board[from_piece[0]][from_piece[1]]) == Pawn:
            # en passant
            if abs(to_piece[0]-from_piece[0]) == 1:
                if type(self.board[to_piece[0]][from_piece[1]]) == Pawn:
                    if self.board[to_piece[0]][from_piece[1]].passant:
                        if self.board[to_piece[0]][to_piece[1]] == None:
                            piece = self.board[from_piece[0]][from_piece[1]]

                            piece.move(to_piece[0], to_piece[1])
                            self.board[to_piece[0]][to_piece[1]] = piece
                            self.board[from_piece[0]][from_piece[1]] = None
                            self.board[to_piece[0]][from_piece[1]] = None
                            self.turn = int((self.turn - 0.5) * -1 + 0.5)
                            return

            #promotion
            colour = self.board[from_piece[0]][from_piece[1]].colour
            if (to_piece[1] == 0 and colour == 0) or (to_piece[1] == 7 and colour == 1):

                self.board[to_piece[0]][to_piece[1]] = Queen(to_piece[0], to_piece[1], colour)
                self.board[from_piece[0]][from_piece[1]] = None
                self.turn = int((self.turn - 0.5) * -1 + 0.5)
                return





        for i in range(8):
            for j in range(8):
                if type(self.board[i][j]) == Pawn:
                    self.board[i][j].passant = False
        if from_piece == (3, (self.turn-1)*-1 * 7) and to_piece == (5, (self.turn-1)*-1 * 7):
            # queen side castle
            index = int((self.turn-1)*-1*7)
            king = self.board[3][index]
            king.move(to_piece[0], to_piece[1])
            self.board[to_piece[0]][to_piece[1]] = king
            self.board[3][index] = None
            rook = self.board[7][index]
            rook.move(4, index)
            self.board[4][index] = rook
            self.board[7][index] = None

            self.turn = int((self.turn - 0.5) * -1 + 0.5)
            return
        if from_piece == (3, (self.turn-1)*-1 * 7) and to_piece == (1, (self.turn-1)*-1 * 7):
            # king side castle
            index = int((self.turn-1)*-1*7)
            king = self.board[3][index]
            king.move(to_piece[0], to_piece[1])
            self.board[to_piece[0]][to_piece[1]] = king
            self.board[3][index] = None
            rook = self.board[0][index]
            rook.move(2, index)
            self.board[2][index] = rook
            self.board[0][index] = None

            self.turn = int((self.turn - 0.5) * -1 + 0.5)
            return
        piece = self.board[from_piece[0]][from_piece[1]]

        piece.move(to_piece[0], to_piece[1])
        self.board[to_piece[0]][to_piece[1]] = piece
        self.board[from_piece[0]][from_piece[1]] = None
        self.turn = int((self.turn - 0.5) * -1 + 0.5)

    def temp_move_piece(self, from_piece, to_piece):
        board_copy = deepcopy(self.board)
        if from_piece == (3, self.turn * 7) and to_piece == (5, self.turn * 7):
            # queen side castle
            king = self.board[3][self.turn * 7]
            king.move(to_piece[0], to_piece[1])
            self.board[to_piece[0]][to_piece[1]] = king
            self.board[3][self.turn * 7] = None
            rook = self.board[7][self.turn * 7]
            rook.move(4, self.turn * 7)
            self.board[4][self.turn*7] = rook
            self.board[7][self.turn * 7] = None

        if from_piece == (3, (self.turn - 1) * -1 * 7) and to_piece == (1, (self.turn - 1) * -1 * 7):
            # king side castle
            index = int((self.turn - 1) * -1 * 7)
            king = self.board[3][index]
            king.move(to_piece[0], to_piece[1])
            self.board[to_piece[0]][to_piece[1]] = king
            self.board[3][index] = None
            rook = self.board[0][index]
            rook.move(2, index)
            self.board[2][index] = rook
            self.board[0][index] = None
        else:


            piece = self.board[from_piece[0]][from_piece[1]]

            piece.move(to_piece[0], to_piece[1])
            self.board[to_piece[0]][to_piece[1]] = piece
            self.board[from_piece[0]][from_piece[1]] = None

        self.turn = int((self.turn - 0.5) * -1 + 0.5)

        return board_copy

    def is_check(self, from_piece, to_piece):
        board_copy = self.temp_move_piece(from_piece, to_piece)

        legal_moves = self.legal_moves(pseudo=True)

        for (i, j), (x, y) in legal_moves:
            if type(self.board[x][y]) == King:
                self.board = deepcopy(board_copy)
                self.turn = int((self.turn - 0.5) * -1 + 0.5)
                return True
        self.turn = int((self.turn - 0.5) * -1 + 0.5)
        self.board = board_copy
        return False

    def in_check(self):

        self.turn = int((self.turn - 0.5) * -1 + 0.5)
        legal_moves = self.legal_moves(pseudo=True)
        self.turn = int((self.turn - 0.5) * -1 + 0.5)
        for (i, j), (x, y) in legal_moves:
            if type(self.board[x][y]) == King:
                return True

        return False

    def check_win(self):
        check = self.in_check()
        legal_moves = self.legal_moves()
        if legal_moves == [] and check == False:
            return "Stalemate"
        if legal_moves == [] and check == True:
            return (self.turn-0.5)*-1+0.5
        else:
            return None

    def get_piece(self, coord):
        piece = self.board[coord[0]][coord[1]]
        if piece is not None:
            return self.board[coord[0]][coord[1]].copy()
        else:
            return None
