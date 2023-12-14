import pygame
from gobblet.board import Board
from gobblet.constants import *
from gobblet.piece import Piece

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gobblet')


def test(board):
    board.board[0][0].push_piece(Piece(Color.DARK, 1))
    board.board[0][1].push_piece(Piece(Color.DARK, 2))
    board.board[0][2].push_piece(Piece(Color.DARK, 3))
    board.board[0][3].push_piece(Piece(Color.DARK, 4))
    board.draw_piece(WIN, Piece(Color.DARK, 1), board.board[0][0])
    board.draw_piece(WIN, Piece(Color.DARK, 2), board.board[0][1])
    board.draw_piece(WIN, Piece(Color.DARK, 3), board.board[0][2])
    board.draw_piece(WIN, Piece(Color.DARK, 4), board.board[0][3])

def main():
    WIN.fill(BACKGROUND)
    run = True
    clock = pygame.time.Clock()
    board = Board(WIN)
    # test(board)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.select(WIN)
                # board.move(WIN, board.board[0][3], board.board[0][0])
        pygame.display.update()
    pygame.quit()


main()


