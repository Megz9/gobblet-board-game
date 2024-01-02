import pygame
from gobblet.board import Board
from gobblet.constants import *
from gobblet.piece import Piece

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gobblet')

def main():
    WIN.fill(BACKGROUND)
    run = True
    clock = pygame.time.Clock()
    board = Board()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        piece = Piece(Color.LIGHT, 0)
        board.draw_stack_panels(WIN)
        board.draw_squares(WIN)
        board.draw_piece(WIN, piece, board.left_stack_panel[0])
        pygame.display.update()
    pygame.quit()


main()
