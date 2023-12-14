import pygame
from gobblet.button import Button
from gobblet.board import Board
from gobblet.constants import *
from gobblet.piece import Piece

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gobblet')
clock = pygame.time.Clock()

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
    gobblet = pygame.transform.smoothscale(
            pygame.image.load("asset/gobblet.png"),
            (4 * HEIGHT // 5, 2 * HEIGHT // 5))
    size = gobblet.get_size()[0] // 2
    WIN.blit(gobblet, (WIDTH // 2 - size, MARGIN))
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Button.exit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                check_button_clicks()
                
        Button.draw_hover_button(WIN, LEFT_BTN_X, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT,
                                 "Human vs Human", BEIGE if Button.selected_mode != 0 else WHITE, HOVER_COLOR if Button.selected_mode != 0 else WHITE)
        Button.draw_hover_button(WIN, MID_BTN_X, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT,
                                 "Human vs AI", BEIGE if Button.selected_mode != 1 else WHITE, HOVER_COLOR if Button.selected_mode != 1 else WHITE)
        Button.draw_hover_button(WIN, RIGHT_BTN_X, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT,
                                 "AI vs AI", BEIGE if Button.selected_mode != 2 else WHITE, HOVER_COLOR if Button.selected_mode != 2 else WHITE)
        Button.draw_hover_button(WIN, LEFT_BTN_X, HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                                 "Easy", BEIGE if Button.selected_difficulty != 0 else WHITE, HOVER_COLOR if Button.selected_difficulty != 0 else WHITE)
        Button.draw_hover_button(WIN, MID_BTN_X, HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                                 "Medium", BEIGE if Button.selected_difficulty != 1 else WHITE, HOVER_COLOR if Button.selected_difficulty != 1 else WHITE)
        Button.draw_hover_button(WIN, RIGHT_BTN_X, HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                                 "Hard", BEIGE if Button.selected_difficulty != 2 else WHITE, HOVER_COLOR if Button.selected_difficulty != 2 else WHITE)
        Button.draw_hover_button(WIN, MID_BTN_X, HEIGHT // 2 + 2 * 4 * MARGIN // 5 + 2 * BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                                 "Play", BEIGE, HOVER_COLOR)
        Button.draw_hover_button(WIN, MID_BTN_X, HEIGHT // 2 + 3 * 4 * MARGIN // 5 + 3 * BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                                 "Exit", BEIGE, HOVER_COLOR)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def check_button_clicks():
        if Button.is_mouse_over_button(LEFT_BTN_X, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT):
            Button.selected_mode = 0
        if Button.is_mouse_over_button(MID_BTN_X, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT):
            Button.selected_mode = 1
        if Button.is_mouse_over_button(RIGHT_BTN_X, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT):
            Button.selected_mode = 2
        if Button.is_mouse_over_button(LEFT_BTN_X, HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
            Button.selected_difficulty = 0
        if Button.is_mouse_over_button(MID_BTN_X, HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
            Button.selected_difficulty = 1
        if Button.is_mouse_over_button(RIGHT_BTN_X, HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
            Button.selected_difficulty = 2
        if Button.is_mouse_over_button(MID_BTN_X, HEIGHT // 2 + 2 * 4 * MARGIN // 5 + 2*BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
            play()
        if Button.is_mouse_over_button(MID_BTN_X, HEIGHT // 2 + 3 * 4 * MARGIN // 5 + 3 * BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
            Button.exit_game()

def play():
    WIN.fill(BACKGROUND)
    board = Board(WIN)
    # test(board)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Button.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.select(WIN)
                # board.move(WIN, board.board[0][3], board.board[0][0])
        pygame.display.update()
    
main()

