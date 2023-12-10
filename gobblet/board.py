import pygame
from .constants import *


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        # self.red_left = self.white_left = 12
        # self.red_kings = self.white_kings = 0

    def draw_squares(self, win):
        pygame.draw.rect(
            win, FOREGROUND, (LEFT_PANE_START, MARGIN, SQUARE_SIZE, BOARD_SIZE))

        # Draw the right sub-board
        pygame.draw.rect(
            win, FOREGROUND, (RIGHT_PANE_START, MARGIN, SQUARE_SIZE, BOARD_SIZE))
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(win, BEIGE if (row + col) % 2 == 0 else BROWN,
                                 (col * SQUARE_SIZE + BOARD_START, row * SQUARE_SIZE + MARGIN, SQUARE_SIZE, SQUARE_SIZE))
