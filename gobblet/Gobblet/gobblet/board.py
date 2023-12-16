import pygame

from gobblet.tile import Tile
from .constants import *


class Board:
    def __init__(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.left_stack_panel = []
        self.right_stack_panel = []
        self.selected_piece = None
        # self.red_left = self.white_left = 12
        # self.red_kings = self.white_kings = 0

    def draw_squares(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_SIZE + BOARD_START
                y = row * SQUARE_SIZE + MARGIN
                self.board[row][col] = Tile(x, y)
                pygame.draw.rect(win, BEIGE if (row + col) % 2 == 0 else BROWN,
                                 (x, y, SQUARE_SIZE, SQUARE_SIZE))

    def draw_stack_panels(self, win):
        for i in range(3):
            self.left_stack_panel.append(
                Tile(LEFT_PANE_START, MARGIN + (SQUARE_SIZE/2) + (SQUARE_SIZE * i)))
            self.right_stack_panel.append(
                Tile(RIGHT_PANE_START, MARGIN + (SQUARE_SIZE/2) + (SQUARE_SIZE * i)))

        pygame.draw.rect(
            win, FOREGROUND, (LEFT_PANE_START, MARGIN, SQUARE_SIZE, BOARD_SIZE))

        # Draw the right sub-board
        pygame.draw.rect(
            win, FOREGROUND, (RIGHT_PANE_START, MARGIN, SQUARE_SIZE, BOARD_SIZE))

    def draw_piece(self, win, piece, tile):

        gobblet = pygame.image.load(
            'asset\dark_gobblet.png' if piece.color == Color.DARK else 'asset\light_gobblet.png')
        win.blit(gobblet, (tile.pos_x, tile.pos_y))
