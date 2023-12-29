import pygame
from gobblet.button import Button
from gobblet.piece import Piece

from gobblet.tile import Tile
from .constants import *


class Board:
    def __init__(self, win):
        win.fill(BACKGROUND)
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.left_stack_panel = [Tile(
            LEFT_PANE_START, MARGIN + (SQUARE_SIZE/2) + (SQUARE_SIZE * i)) for i in range(3)]
        self.right_stack_panel = [Tile(
            RIGHT_PANE_START, MARGIN + (SQUARE_SIZE/2) + (SQUARE_SIZE * i)) for i in range(3)]
        self.selected_piece = None
        self.selected_tile = None
        # self.red_left = self.white_left = 12
        # self.red_kings = self.white_kings = 0

        self.turn = 0 #black gobblet starts

        #to know the selected piece was from which part (board,left_pane,right_pane)
        self.to_board = None
        self.to_left_pane = None
        self.to_right_pane = None

        #rows,columns,diagonals which have 3 elements to allow gobbling it from external stack
        self.critical_case_row = []   #0 ->3 where 0 is the upper row
        self.critical_case_col = []   #0 ->3 where 0 is the leftmost col
        self.critical_case_diag = 0 
        self.critical_case_antidiag = 0  




        self.draw_stack_panels(win)
        self.draw_initial_board(win)

        for i in range(3):
            for j in range(4):
                self.left_stack_panel[i].pieces_stack.append(
                    Piece(Color.DARK, j+1))
                self.right_stack_panel[i].pieces_stack.append(
                    Piece(Color.LIGHT, j+1))
            self.draw_piece(
                win, self.left_stack_panel[i].pieces_stack[-1], self.left_stack_panel[i])
            self.draw_piece(
                win, self.right_stack_panel[i].pieces_stack[-1], self.right_stack_panel[i])
        Button.draw_hover_button(win, RIGHT_PANE_START - MARGIN, MARGIN, BUTTON_HEIGHT, BUTTON_HEIGHT,
                             "||", BEIGE, HOVER_COLOR)

    def draw_initial_board(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_SIZE + BOARD_START_X
                y = row * SQUARE_SIZE + MARGIN
                self.board[row][col] = Tile(x, y)
                pygame.draw.rect(win, BEIGE if (row + col) % 2 == 0 else BROWN,
                                 (x, y, SQUARE_SIZE, SQUARE_SIZE))

    def draw_stack_panels(self, win):

        pygame.draw.rect(
            win, FOREGROUND, (LEFT_PANE_START, MARGIN, SQUARE_SIZE, BOARD_SIZE))

        # Draw the right sub-board
        pygame.draw.rect(
            win, FOREGROUND, (RIGHT_PANE_START, MARGIN, SQUARE_SIZE, BOARD_SIZE))

    def move(self, win, old_tile, new_tile):
        new_tile.push_piece(old_tile.pop_piece())
        self.draw_piece(win, new_tile.pieces_stack[-1], new_tile)
        self.draw_tile(win, old_tile)
        self.to_right_pane = 0
        self.to_left_pane = 0
        self.to_board = 0
        self.turn ^= 1  
        self.check_win()

    def draw_tile(self, win, tile):
        pygame.draw.rect(win, win.get_at((int(tile.pos_x + STROKE + 1), int(tile.pos_y + STROKE + 1))),
                         (tile.pos_x, tile.pos_y, SQUARE_SIZE, SQUARE_SIZE))
        # If the tile is not empty (still has pieces left after removal)
        if tile.pieces_stack != []:
            # Draw the piece on top of the stack
            self.draw_piece(win, tile.pieces_stack[-1], tile)

    def draw_piece(self, win, piece, tile):

        gobblet = pygame.transform.smoothscale(
            pygame.image.load(
                'asset\dark_gobblet.png' if piece.color == Color.DARK else 'asset\light_gobblet.png'),
            (PIECE_SIZE * (0.4 + piece.size * 0.15), PIECE_SIZE * (0.4 + piece.size * 0.15)))
        size = gobblet.get_size()[0] // 2
        win.blit(gobblet, (tile.pos_x + SQUARE_SIZE/2 -
                 size, tile.pos_y + SQUARE_SIZE / 2 - size))
        # win.blit(gobblet, (tile.pos_x, tile.pos_y))

    def select(self, win):
        pos = pygame.mouse.get_pos()
        tile = self.get_tile_from_pos(pos)
        if tile != None and self.selected_tile != None:
            # Check move validity
            self.move(win, self.selected_tile, tile)
            self.selected_tile = None
        elif tile != None and tile.pieces_stack != []:
            self.selected_tile = tile
            Board.highlight_tile(win, tile)

    def highlight_tile(win, tile):
        pygame.draw.line(win, BLUE, (tile.pos_x + STROKE // 2 - 1, tile.pos_y),
                         (tile.pos_x + STROKE // 2 - 1, tile.pos_y + SQUARE_SIZE - 1), STROKE)
        pygame.draw.line(win, BLUE, (tile.pos_x, tile.pos_y + STROKE // 2 - 1),
                         (tile.pos_x + SQUARE_SIZE - 1, tile.pos_y + STROKE // 2 - 1), STROKE)
        pygame.draw.line(win, BLUE, (tile.pos_x + SQUARE_SIZE - STROKE // 2 - 1, tile.pos_y),
                         (tile.pos_x + SQUARE_SIZE - STROKE // 2 - 1, tile.pos_y + SQUARE_SIZE - 1), STROKE)
        pygame.draw.line(win, BLUE, (tile.pos_x, tile.pos_y + SQUARE_SIZE - STROKE // 2 - 1),
                         (tile.pos_x + SQUARE_SIZE - 1, tile.pos_y + SQUARE_SIZE - STROKE // 2 - 1), STROKE)

    def get_tile_from_pos(self, pos):
        mouse_x, mouse_y = pos
        if mouse_y < MARGIN or mouse_y > BOARD_SIZE + MARGIN:
            return None

        elif mouse_y > MARGIN + SQUARE_SIZE // 2 and mouse_y < MARGIN + 3.5 * SQUARE_SIZE:
            if mouse_x > RIGHT_PANE_START and mouse_x < RIGHT_PANE_START + SQUARE_SIZE:
                row = int((mouse_y - MARGIN - SQUARE_SIZE / 2) // SQUARE_SIZE)
                print(row)
                self.to_right_pane = 1
                self.to_left_pane = 0
                self.to_board = 0
                return self.right_stack_panel[row]

            if mouse_x > LEFT_PANE_START and mouse_x < LEFT_PANE_START + SQUARE_SIZE:
                row = int((mouse_y - MARGIN - SQUARE_SIZE / 2) // SQUARE_SIZE)
                print(row)
                self.to_left_pane = 1
                self.to_right_pane = 0
                self.to_board = 0
                return self.left_stack_panel[row]

        if mouse_x > BOARD_START_X and mouse_x < BOARD_START_X + BOARD_SIZE:
            row = int((mouse_y - MARGIN) // SQUARE_SIZE)
            col = int((mouse_x - BOARD_START_X) // SQUARE_SIZE)
            self.current_row = row
            self.current_col = col
            print(row, col)
            self.to_board = 1
            self.to_left_pane = 0
            self.to_right_pane = 0
            return self.board[row][col]

        return None
     

    def draw_board(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_SIZE + BOARD_START_X
                y = row * SQUARE_SIZE + MARGIN
                pygame.draw.rect(win, BEIGE if (row + col) % 2 == 0 else BROWN,
                                 (x, y, SQUARE_SIZE, SQUARE_SIZE))
                self.draw_tile(win, self.board[row][col])

    def draw_game(self, win):
        win.fill(BACKGROUND)
        self.draw_board(win)
        self.draw_stack_panels(win)
        for i in range(3):
            self.draw_tile(win, self.left_stack_panel[i])
            self.draw_tile(win, self.right_stack_panel[i])
        Button.draw_hover_button(win, RIGHT_PANE_START - MARGIN, MARGIN, BUTTON_HEIGHT, BUTTON_HEIGHT,
                             "||", BEIGE, HOVER_COLOR)

#rule for moving pieces when first selection is external stack
    def game_Rules(self,win,old_tile,new_tile):
        row = int((new_tile.pos_y - MARGIN) // SQUARE_SIZE)
        col = int((new_tile.pos_x - BOARD_START_X) // SQUARE_SIZE)
        print("row.....",row)
        print("critical_row.....",self.critical_case_row)
        #can't go from board to external stacks or go from external stack to external stack
        if(self.to_right_pane or self.to_left_pane): 
           print("can't make move")
           return 0
        elif(self.to_board):
            #go within board or from external stack to board
            if new_tile.pieces_stack == []: #empty tile
                print("going to board")
                return 1
            elif(row in self.critical_case_row or col in self.critical_case_col or self.critical_case_diag !=0 or self.critical_case_antidiag != 0): #allow gobbling from external stack in critical case (3 in same row)
                if(row in self.critical_case_row): self.critical_case_row.remove(row)
                if(col in self.critical_case_col): self.critical_case_col.remove(col)
                self.critical_case_diag = 0
                self.critical_case_antidiag = 0
                #print("new list",self.critical_case_row)
                return self.check_size(old_tile,new_tile)