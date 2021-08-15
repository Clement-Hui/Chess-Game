class Piece:
    def __init__(self, x, y, colour, moved=False, type=None):
        self.x = x
        self.y = y
        self.moved = moved

        self.colour = colour
        self.type = type




    def legal(self, x, y, taking):
        return True

    def num(self):
        """
        0:blank
        1: black bishop 2: black king
        3: black knight 4: black pawn
        5: black queen  6: black rook
        7: white bishop 8: white king
        9: white knight 10: white pawn
        11: white queen 12: white rook


        """
        if self.colour == 1:
            return self.type
        else:
            return self.type+6

    def __copy__(self):
        copy = type(self)(self.x,self.y,self.colour, self.moved, self.type)
        return copy

    def move(self, x, y):
        self.moved = True
        self.x = x
        self.y = y

class Knight(Piece):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
        self.type = 3
    
    def legal(self, x, y, taking):
        x_diff = abs(self.x - x)
        y_diff = abs(self.y - y)

        if self.x == x and self.y == y:
            return False

        if (x_diff == 2 and y_diff == 1) or (x_diff == 1 and y_diff == 2):

            return True
        else:
            return False


class Rook(Piece):
    def __init__(self, x, y, colour):
        super(Rook, self).__init__(x, y, colour)
        self.type = 6

    def legal(self, x, y, taking):
        x_diff = abs(self.x - x)
        y_diff = abs(self.y - y)

        if self.x == x and self.y == y:
            return False

        if (x_diff == 0) or (y_diff == 0):

            return True
        else:
            return False


class Bishop(Piece):
    def __init__(self, x, y, colour):
        super(Bishop, self).__init__(x, y, colour)
        self.type = 1

    def legal(self, x, y, taking):
        x_diff = abs(self.x - x)
        y_diff = abs(self.y - y)

        if self.x == x and self.y == y:
            return False

        if x_diff == y_diff:

            return True
        else:
            return False


class Queen(Piece):
    def __init__(self, x, y, colour):
        super(Queen, self).__init__(x, y, colour)
        self.type = 5

    def legal(self, x, y, taking):
        x_diff = abs(self.x - x)
        y_diff = abs(self.y - y)

        if self.x == x and self.y == y:
            return False

        if (x_diff == y_diff) or (x_diff == 0) or (y_diff == 0):

            return True
        else:
            return False


class King(Piece):
    def __init__(self, x, y, colour):
        super(King, self).__init__(x, y, colour)
        self.type = 2

    def legal(self, x, y, taking):
        x_diff = abs(self.x - x)
        y_diff = abs(self.y - y)

        if self.x == x and self.y == y:
            return False

        if x_diff <= 1 and y_diff <= 1:

            return True
        else:
            return False


class Pawn(Piece):
    def __init__(self, x, y, colour):
        super(Pawn, self).__init__(x,y,colour)
        self.type = 4
        self.passant = False

    def legal(self, x, y, taking):
        x_diff = abs(self.x - x)
        y_diff = self.y - y
        if not taking:
            if x_diff == 0 and y_diff == 1 * (self.colour-0.5)*2*-1:
                return True
            if not self.moved:
                if x_diff == 0 and y_diff == 2 * (self.colour-0.5)*2*-1:\

                    return True
        else:
            if x_diff == 1 and y_diff == 1 * (self.colour-0.5)*2*-1:

                return True

        return False

    def move(self, x, y):
        if abs(self.y-y) == 2:
            self.passant = True
        self.moved = True
        self.x = x
        self.y = y


