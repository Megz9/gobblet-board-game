from enum import Enum
import pygame


class Color(Enum):
    LIGHT = 0
    DARK = 1


pygame.init()

WIDTH, HEIGHT = 800, 500
BOTTOM_BAR_HEIGHT =50
ROWS, COLS = 4, 4
MARGIN = 0.05 * HEIGHT
BOARD_SIZE = min(WIDTH, HEIGHT) - 2 * MARGIN
SQUARE_SIZE = BOARD_SIZE//COLS
PIECE_SIZE = SQUARE_SIZE * 0.8
BOARD_START_X = WIDTH//2 - 2*SQUARE_SIZE
LEFT_PANE_START = BOARD_START_X - 2 * MARGIN - SQUARE_SIZE
RIGHT_PANE_START = BOARD_START_X + BOARD_SIZE + 2 * MARGIN
STROKE = 4

MAX_DEPTH = 7
MAX_TIME  = 3

BUTTON_WIDTH, BUTTON_HEIGHT = 220, 45
BORDER_RADIUS = 15  # Radius for rounded corners

MID_BTN_X = WIDTH // 2 - BUTTON_WIDTH // 2
LEFT_BTN_X = MID_BTN_X - MARGIN - BUTTON_WIDTH
RIGHT_BTN_X = MID_BTN_X + MARGIN + BUTTON_WIDTH

DIFFICULITY = [
    "Easy",
    "Medium",
    "Hard"
]

FONT_SIZE = 22

FONT = pygame.font.Font("asset/mono.ttf", FONT_SIZE)

BROWN = (139, 35, 35)
BEIGE = (222, 184, 135)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
HOVER_COLOR = (234, 208, 174)
DISABLED_BUTTON = (139,115,85 , 60)
DISABLED_BUTTON_HOVER = (139,115,85 , 0)
BACKGROUND = (71, 23, 23)
FOREGROUND = (102, 36, 36)

INFINITY = 999999999999999999
