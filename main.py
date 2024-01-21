import pygame
from gobblet.ai import MinMax
from gobblet.button import Button
from gobblet.board import Board
from gobblet.board_test import Board_Test
from gobblet.constants import *
from gobblet.piece import Piece

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gobblet')
clock = pygame.time.Clock()


# def test(board):
#     board.board[0][0].push_piece(Piece(Color.DARK, 1))
#     board.board[0][1].push_piece(Piece(Color.DARK, 2))
#     board.board[0][2].push_piece(Piece(Color.DARK, 3))
#     board.board[0][3].push_piece(Piece(Color.DARK, 4))
#     board.draw_piece(WIN, Piece(Color.DARK, 1), board.board[0][0])
#     board.draw_piece(WIN, Piece(Color.DARK, 2), board.board[0][1])
#     board.draw_piece(WIN, Piece(Color.DARK, 3), board.board[0][2])
#     board.draw_piece(WIN, Piece(Color.DARK, 4), board.board[0][3])


def main():
    gobblet = pygame.transform.smoothscale(
        pygame.image.load("asset/gobblet.png"),
        (4 * HEIGHT // 5, 2 * HEIGHT // 5))
    size = gobblet.get_size()[0] // 2
    run = True

    while run:
        WIN.fill(BACKGROUND)
        WIN.blit(gobblet, (WIDTH // 2 - size, MARGIN))
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
        if Button.selected_mode == 0 :
             Button.draw_hover_button(WIN, MID_BTN_X - 0.125 * BUTTON_WIDTH, HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH * 1.25, BUTTON_HEIGHT,
                                     f"Difficulty: {DIFFICULITY[Button.selected_difficulty]}", DISABLED_BUTTON, DISABLED_BUTTON_HOVER)
        elif Button.selected_mode == 1:
            Button.draw_hover_button(WIN, MID_BTN_X - 0.125 * BUTTON_WIDTH, HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH * 1.25, BUTTON_HEIGHT,
                                     f"Difficulty: {DIFFICULITY[Button.selected_difficulty]}", BEIGE, HOVER_COLOR)
        elif Button.selected_mode == 2:
            Button.draw_hover_button(WIN, MID_BTN_X - 0.125 * BUTTON_WIDTH - 0.5 * (MARGIN + BUTTON_WIDTH * 1.25), HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH * 1.25, BUTTON_HEIGHT,
                                     f"Difficulty: {DIFFICULITY[Button.selected_difficulty]}", BEIGE, HOVER_COLOR)
            Button.draw_hover_button(WIN, MID_BTN_X - 0.125 * BUTTON_WIDTH + 0.5 * (MARGIN + BUTTON_WIDTH * 1.25), HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH * 1.25, BUTTON_HEIGHT,
                                     f"Difficulty: {DIFFICULITY[Button.selected_difficulty_two]}", BEIGE, HOVER_COLOR)
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
    if Button.selected_mode == 1 and Button.is_mouse_over_button(MID_BTN_X - 0.125 * BUTTON_WIDTH, HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH * 1.25, BUTTON_HEIGHT):
        Button.selected_difficulty = (Button.selected_difficulty + 1) % 3
    elif Button.selected_mode == 2 and Button.is_mouse_over_button(MID_BTN_X - 0.125 * BUTTON_WIDTH - 0.5 * (MARGIN + BUTTON_WIDTH * 1.25), HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH * 1.25, BUTTON_HEIGHT):
        Button.selected_difficulty = (Button.selected_difficulty + 1) % 3
    elif Button.selected_mode == 2 and Button.is_mouse_over_button(MID_BTN_X - 0.125 * BUTTON_WIDTH + 0.5 * (MARGIN + BUTTON_WIDTH * 1.25), HEIGHT // 2 + 4 * MARGIN // 5 + BUTTON_HEIGHT, BUTTON_WIDTH * 1.25, BUTTON_HEIGHT):
        Button.selected_difficulty_two = (
            Button.selected_difficulty_two + 1) % 3
    if Button.is_mouse_over_button(MID_BTN_X, HEIGHT // 2 + 2 * 4 * MARGIN // 5 + 2 * BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
        play()
    if Button.is_mouse_over_button(MID_BTN_X, HEIGHT // 2 + 3 * 4 * MARGIN // 5 + 3 * BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
        Button.exit_game()


def play():
    pygame.mixer.music.load('asset/start.wav')
    pygame.mixer.music.play(1)
    board = Board(WIN)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Button.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Button.is_mouse_over_button(RIGHT_PANE_START - MARGIN, MARGIN, BUTTON_HEIGHT, BUTTON_HEIGHT):
                    if pause(board) == 2: return
                else: board.select()
        pygame.display.update()
        if board.check_win() != 2:
            if player_wins(board) == 2:
                return
        if board.turn and Button.selected_mode >= 1:
            MinMax.available_moves = []
            MinMax.minimax(board, 0, Button.selected_difficulty) # at 7:45
        elif board.turn == 0 and Button.selected_mode == 2:
            MinMax.available_moves = []
            MinMax.minimax(board, 0, Button.selected_difficulty_two) # at 7:45


def pause(board):
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)   # per-pixel alpha
    # notice the alpha value in the color
    s.fill((0, 0, 0, 128))
    WIN.blit(s, (0, 0))
    MIDDLE_BTN_HEIGHT = HEIGHT // 2 - BUTTON_HEIGHT // 2
    Button.draw_hover_button(WIN, MID_BTN_X, MIDDLE_BTN_HEIGHT - MARGIN - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                             "Resume", BEIGE, HOVER_COLOR)
    Button.draw_hover_button(WIN, MID_BTN_X, MIDDLE_BTN_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                             "Restart", BEIGE, HOVER_COLOR)
    Button.draw_hover_button(WIN, MID_BTN_X, MIDDLE_BTN_HEIGHT + MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                             "Main Menu", BEIGE, HOVER_COLOR)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Button.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                check = check_pause_clicks(board)
                if check:
                    return check
        pygame.display.update()


def check_pause_clicks(board):
    MIDDLE_BTN_HEIGHT = HEIGHT // 2 - BUTTON_HEIGHT // 2
    if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT - MARGIN - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
        board.draw_game()
        return 1
    if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
        board.__init__(WIN)
        board.draw_game()
        return 1
    if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT + MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
        return 2
    return 0

def player_wins(board):
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)   # per-pixel alpha
    # notice the alpha value in the color
    if(board.check_win() == -1): win_text = "Black Wins"
    elif(board.check_win() == 1): win_text = "White Wins"
    elif(board.check_win() == 0): win_text = "Draw"

    s.fill((0, 0, 0, 128))
    WIN.blit(s, (0, 0))
    MIDDLE_BTN_HEIGHT = HEIGHT // 2 - BUTTON_HEIGHT // 2
    # font = pygame.font.Font('asset/mono.ttf', 60)
    # text_surface = font.render(win_text, True, WHITE)
    # text_rect = text_surface.get_rect(center=(MID_BTN_X + BUTTON_WIDTH/2, MIDDLE_BTN_HEIGHT - MARGIN - BUTTON_HEIGHT/2))
    dropShadowText(win_text,60,MID_BTN_X + BUTTON_WIDTH/2,MIDDLE_BTN_HEIGHT - MARGIN - BUTTON_HEIGHT/2, WHITE, BLACK, 'asset/mono.ttf')
    # WIN.blit(text_surface, text_rect)
    # Button.draw_hover_button(WIN, MID_BTN_X, MIDDLE_BTN_HEIGHT - MARGIN - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
    #                          "Resume", BEIGE, HOVER_COLOR)
    Button.draw_hover_button(WIN, MID_BTN_X, MIDDLE_BTN_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                             "Restart", BEIGE, HOVER_COLOR)
    Button.draw_hover_button(WIN, MID_BTN_X, MIDDLE_BTN_HEIGHT + MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                             "Main Menu", BEIGE, HOVER_COLOR)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Button.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                check = check_win_clicks(board)
                if check:
                    return check
        pygame.display.update()


def check_win_clicks(board):
    MIDDLE_BTN_HEIGHT = HEIGHT // 2 - BUTTON_HEIGHT // 2
    # if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT - MARGIN - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
    #     board.draw_game()
    #     return 1
    if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
        board.__init__(WIN)
        return 1
    if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT + MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
        return 2
    return 0


def dropShadowText(text, size, x, y, colour=(255,255,255), drop_colour=(128,128,128), font=None):
    # how much 'shadow distance' is best?
    dropshadow_offset = 1 + (size // 15)
    text_font = pygame.font.Font(font, size)
    # make the drop-shadow
    text_surface = text_font.render(text, True, drop_colour)
    # text_surface = font.render(win_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x+dropshadow_offset, y+dropshadow_offset))
    # screen.blit(text_bitmap, (x+dropshadow_offset, y+dropshadow_offset) )
    WIN.blit(text_surface, text_rect)
    # make the overlay text
    text_surface = text_font.render(text, True, colour)
    text_rect = text_surface.get_rect(center=(x,y))
    WIN.blit(text_surface, text_rect)
    # screen.blit(text_bitmap, (x, y) )


main()
