import os
import pygame as pg
import time
from game import ChessGame


screen_size = 800
grid_size = int(screen_size / 8)

white_colour = (238, 238, 210)
black_colour = (118, 150, 86)
selected_colour = (246, 248, 121)
legal_move_colour = (150,150,150,255)
pg.init()
game_running = True
chess_piece_scaling = 0.8
radius = 0.15*grid_size

game_window = pg.display.set_mode((screen_size, screen_size))
pg.display.set_caption("Chess")


# loading game sprites
class ChessPieceSprite(pg.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

b_bishop = pg.image.load("sprites/b_bishop.png").convert_alpha()
b_king = pg.image.load("sprites/b_king.png").convert_alpha()
b_knight = pg.image.load("sprites/b_knight.png").convert_alpha()
b_pawn = pg.image.load("sprites/b_pawn.png").convert_alpha()
b_queen = pg.image.load("sprites/b_queen.png").convert_alpha()
b_rook = pg.image.load("sprites/b_rook.png").convert_alpha()
w_bishop = pg.image.load("sprites/w_bishop.png").convert_alpha()
w_king = pg.image.load("sprites/w_king.png").convert_alpha()
w_knight = pg.image.load("sprites/w_knight.png").convert_alpha()
w_pawn = pg.image.load("sprites/w_pawn.png").convert_alpha()
w_queen = pg.image.load("sprites/w_queen.png").convert_alpha()
w_rook = pg.image.load("sprites/w_rook.png").convert_alpha()

image_sprites = [b_bishop,b_king,b_knight,b_pawn,b_queen,b_rook,w_bishop,w_king,w_knight,w_pawn,w_queen,w_rook]
"""
0:blank
1: black bishop 2: black king   
3: black knight 4: black pawn  
5: black queen  6: black rook   
7: white bishop 8: white king
9: white knight 10: white pawn
11: white queen 12: white rook



m = [
    [6, 3, 1, 5, 2, 1, 3, 6],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [10, 10, 10, 10, 10, 10, 10, 10],
    [12, 9, 7, 11, 8, 7, 9, 12]
]
# rotating the board 90 degrees
game_board = [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]
"""

game = ChessGame()

grid = []
for i in range(8):
    for j in range(8):
        rect = pg.Rect(i * grid_size, j * grid_size, grid_size, grid_size)
        grid.append((rect,i,j))

selected_piece = None
previous_selected_piece = selected_piece
game_board = game.to_arr()
legal_moves = game.legal_moves()
win = None
while game_running:



    game_window.fill(white_colour)


    selected_piece_legals = []
    for piece, to in legal_moves:
        if piece == selected_piece:
            selected_piece_legals.append(to)

    for i in range(8):
        for j in range(8):

            rect = pg.Rect(i * grid_size, j * grid_size, grid_size, grid_size)
            if j % 2 == i % 2:
                pg.draw.rect(game_window, white_colour, rect)
            else:
                pg.draw.rect(game_window, black_colour, rect)

            if selected_piece is not None:
                if i == selected_piece[0] and j == selected_piece[1]:
                    pg.draw.rect(game_window, selected_colour, rect)

            piece_no = game_board[i][j]
            if piece_no != 0:


                image = image_sprites[piece_no - 1]
                image = pg.transform.smoothscale(image, (int(image.get_size()[0] / 128 * grid_size * chess_piece_scaling),
                                                         int(image.get_size()[1] / 128 * grid_size * chess_piece_scaling)))
                piece = ChessPieceSprite((i * grid_size + grid_size / 2, j * grid_size + grid_size / 2), image)

                piece.draw(game_window)

            if selected_piece is not None:
                if (i,j) in selected_piece_legals:

                    pg.draw.circle(game_window, legal_move_colour,(i*grid_size+grid_size/2,j*grid_size+grid_size/2), radius)

            if win != None:
                if win == "Stalemate":
                    pg.font.init()
                    font = pg.font.SysFont("Ariel", 90)
                    textsurface = font.render("Stalemate", False, (0, 0, 0), (255, 255, 255))
                    game_window.blit(textsurface, (
                    screen_size / 2 - textsurface.get_size()[0] / 2, screen_size / 2 - textsurface.get_size()[1] / 2))
                if win == 0:
                    pg.font.init()
                    font = pg.font.SysFont("Ariel", 90)
                    textsurface = font.render("White won", False, (0, 0, 0), (255, 255, 255))
                    game_window.blit(textsurface, (
                    screen_size / 2 - textsurface.get_size()[0] / 2, screen_size / 2 - textsurface.get_size()[1] / 2))
                if win == 1:
                    pg.font.init()
                    font = pg.font.SysFont("Ariel", 90)
                    textsurface = font.render("Black won", False, (0, 0, 0), (255, 255, 255))
                    game_window.blit(textsurface, (screen_size / 2-textsurface.get_size()[0]/2, screen_size / 2-textsurface.get_size()[1]/2))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_running = False

        if event.type == pg.MOUSEBUTTONDOWN and win == None:
            legal_moves = game.legal_moves()
            pos = pg.mouse.get_pos()
            x,y = [(i, j) for s, i, j in grid if s.collidepoint(pos)][0]

            if selected_piece is None:
                selected_piece = (x,y)

            else:
                s_x,s_y = selected_piece
                legal_moves = game.legal_moves()
                if (selected_piece,(x,y)) in legal_moves:
                    game.move_piece(selected_piece,(x,y))
                    win = game.check_win()


                    game_board = game.to_arr()


                selected_piece = None


    pg.display.update()

pg.quit()
