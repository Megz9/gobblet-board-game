import pygame
from gobblet.ai import MinMax
from gobblet.button import Button
from gobblet.board import Board

from gobblet.constants import *
from gobblet.piece import Piece



FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT+BOTTOM_BAR_HEIGHT))
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

def draw_both_players(board) :
    s = pygame.Surface((WIDTH, HEIGHT+BOTTOM_BAR_HEIGHT), pygame.SRCALPHA)   # per-pixel alpha
    win_text = "Draw!"
    s.fill((0, 0, 0, 128))
    WIN.blit(s, (0, 0))
    MIDDLE_BTN_HEIGHT = HEIGHT // 2 - BUTTON_HEIGHT // 2
    dropShadowText(win_text,60,MID_BTN_X + BUTTON_WIDTH/2,MIDDLE_BTN_HEIGHT - MARGIN - BUTTON_HEIGHT/2, WHITE, BLACK, 'asset/mono.ttf')
    Button.draw_hover_button(WIN, MID_BTN_X, MIDDLE_BTN_HEIGHT + MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                             "Main Menu", BEIGE, HOVER_COLOR)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Button.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT + MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
                    return 2
        pygame.display.update()
def play():
    pygame.mixer.music.load('asset/start.wav')
    pygame.mixer.music.play(1)
    board = Board(WIN)
    board.right_player = 0
    board.left_player = 0
    # Add Draw Button
    #Button.draw_button(WIN ,LEFT_PANE_START+5, HEIGHT-4,100,42,"Draw",BEIGE,BEIGE )
    #Button.draw_button(WIN ,RIGHT_PANE_START+5, HEIGHT-4,100,42,"Draw",BEIGE,BEIGE )
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Button.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Button.is_mouse_over_button(RIGHT_PANE_START - MARGIN, MARGIN, BUTTON_HEIGHT, BUTTON_HEIGHT):
                    if pause(board) == 2: return
                else: board.select() 
                # if Button.is_mouse_over_button(LEFT_PANE_START+5, HEIGHT-4,100,42):
                #     check_right_draw(board)
                # if Button.is_mouse_over_button(RIGHT_PANE_START+5, HEIGHT-4,100,42):
                #     check_left_draw(board)

                if Button.selected_mode != 2:
                    if board.turn==1:
                        if Button.is_mouse_over_button(LEFT_PANE_START+5, HEIGHT-4,100,42):
                            Button.draw_button(WIN ,LEFT_PANE_START+5, HEIGHT-4,100,42,"Draw",DISABLED_BUTTON,DISABLED_BUTTON )
                            board.left_player = 1
                            if Request_draw(board)==2: return
                            print("left player , right player",board.left_player , board.right_player)
                    if board.turn==0:
                        if Button.is_mouse_over_button(RIGHT_PANE_START+5, HEIGHT-4,100,42):
                            Button.draw_button(WIN ,RIGHT_PANE_START+5, HEIGHT-4,100,42,"Draw",DISABLED_BUTTON,DISABLED_BUTTON )
                            if Button.selected_mode==1:
                                
                                if Draw_Request_Ai(board)==2:return
                                board.draw_game()
                            else:
                                board.right_player = 1
                                if Request_draw(board)==2: return
        # pygame.draw.rect(screen, (0, 255, 0) if board.turn else (255, 0, 0), turn_rect)
        # def draw_button(win, x, y, width, height, text, button_color, border_color):
        rect = pygame.Rect(WIDTH/2-100, HEIGHT, 200, 40)
        pygame.draw.rect(WIN, FOREGROUND, rect,
                         border_radius=BORDER_RADIUS)
        
        # Add a border around the button
        pygame.draw.rect(WIN, HOVER_COLOR, rect, 3,
                         border_radius=BORDER_RADIUS)

        text_surface = FONT.render("BLACK TURN"if board.turn else "WHITE TURN", True, HOVER_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        WIN.blit(text_surface, text_rect)
        pygame.display.update()
        if board.check_win() != 2:
            if player_wins(board) == 2:
                return
        # check_draws()
        if board.turn and Button.selected_mode >= 1:
            MinMax.available_moves = []
            MinMax.minMaxPruning_IterativeDeeping_withTimeConstraints(board,Button.selected_difficulty)
            # MinMax.minimax_with_pruning(board, 0, -INFINITY,INFINITY,Button.selected_difficulty) # at 7:45
            # print("---Starting normal min max---")
            # MinMax.minimax(board, 0, Button.selected_difficulty) # at 7:45
            #MinMax.minimax(board,0,Button.selected_difficulty)
            if(MinMax.Draw_Request==1):
                print("tesssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssst")
                MinMax.Draw_Request=0
                if Request_draw(board)!=2:
                    MinMax.Tried_Draw_Once=1
                else: return
        elif board.turn == 0 and Button.selected_mode == 2:
            MinMax.available_moves = []
            MinMax.minMaxPruning_IterativeDeeping_withTimeConstraints(board,Button.selected_difficulty_two)
            # MinMax.minimax(board, 0, Button.selected_difficulty_two) # at 7:45

def Draw_Request_Ai(board):
    MinMax.No_Move=1
    print("test_finaaaaaaaaaaaaal")
    Evaluted_Board=MinMax.minimax(board,5,Button.selected_difficulty)
    MinMax.No_Move=0
    
    if (Evaluted_Board<-INFINITY+10):
        draw_both_players(board)
        return 2
    else:
        
        s = pygame.Surface((WIDTH, HEIGHT+BOTTOM_BAR_HEIGHT), pygame.SRCALPHA)   # per-pixel alpha
        win_text = "Draw Rejected!!"
        s.fill((0, 0, 0, 128))
        WIN.blit(s, (0, 0))
        MIDDLE_BTN_HEIGHT = HEIGHT // 2 - BUTTON_HEIGHT // 2
        dropShadowText(win_text,60,MID_BTN_X + BUTTON_WIDTH/2,MIDDLE_BTN_HEIGHT - MARGIN - BUTTON_HEIGHT/2, WHITE, BLACK, 'asset/mono.ttf')
        Button.draw_hover_button(WIN, MID_BTN_X, MIDDLE_BTN_HEIGHT + MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                                "Continue", BEIGE, HOVER_COLOR)
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Button.exit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT + MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
                        
                        return
            pygame.display.update()


# def check_right_draw(board) :
#     Button.draw_button(WIN ,LEFT_PANE_START+5, HEIGHT-4,100,42,"Draw",DISABLED_BUTTON,DISABLED_BUTTON )
#     if Button.is_mouse_over_button(RIGHT_PANE_START+5, HEIGHT-4,100,42) :
#         draw_both_players(board)

# def check_left_draw(board) :
#     Button.draw_button(WIN ,RIGHT_PANE_START+5, HEIGHT-4,100,42,"Draw",DISABLED_BUTTON,DISABLED_BUTTON )
#     if Button.is_mouse_over_button(LEFT_PANE_START+5, HEIGHT-4,100,42) :
#         draw_both_players(board)


def Request_draw(board):
    board.left_player = 0
    board.right_player = 0
    board.turn ^= 1
    s = pygame.Surface((WIDTH, HEIGHT+BOTTOM_BAR_HEIGHT), pygame.SRCALPHA)   # per-pixel alpha
    # notice the alpha value in the color
    s.fill((0, 0, 0, 128))
    WIN.blit(s, (0, 0))
    MIDDLE_BTN_HEIGHT = HEIGHT // 2 - BUTTON_HEIGHT // 2
    Button.draw_hover_button(WIN, MID_BTN_X, MIDDLE_BTN_HEIGHT - MARGIN - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                             "Reject Draw", BEIGE, HOVER_COLOR)
    Button.draw_hover_button(WIN, MID_BTN_X, MIDDLE_BTN_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
                             "Accept Draw", BEIGE, HOVER_COLOR)
    #if board.selected_mode ==0 :#################################################################################
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Button.exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                check = check_Draw_clicks(board)
                if check:
                    return check
        pygame.display.update()
    


def check_Draw_clicks(board):
    MIDDLE_BTN_HEIGHT = HEIGHT // 2 - BUTTON_HEIGHT // 2
    if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT - MARGIN - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
        board.turn ^=1
        board.draw_game()
        return 1
    if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
        board.left_player = 0
        board.right_player= 0
        board.draw_game()
        check = draw_both_players(board)
        if check == 2 : return check
        
        return 1








def pause(board):
    s = pygame.Surface((WIDTH, HEIGHT+BOTTOM_BAR_HEIGHT), pygame.SRCALPHA)   # per-pixel alpha
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
        board.left_player = 0
        board.right_player= 0
        board.__init__(WIN)
        board.draw_game()
        return 1
    if Button.is_mouse_over_button(MID_BTN_X, MIDDLE_BTN_HEIGHT + MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT):
        return 2
    return 0

def player_wins(board):
    s = pygame.Surface((WIDTH, HEIGHT+BOTTOM_BAR_HEIGHT), pygame.SRCALPHA)   # per-pixel alpha
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
