import pygame
from gobblet.button import Button
from gobblet.piece import Piece

from gobblet.tile import Tile
from .constants import *


class Board:
    def __init__(self, win):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.left_stack_panel = [Tile(
            LEFT_PANE_START, MARGIN + (SQUARE_SIZE/2) + (SQUARE_SIZE * i)) for i in range(3)]
        self.right_stack_panel = [Tile(
            RIGHT_PANE_START, MARGIN + (SQUARE_SIZE/2) + (SQUARE_SIZE * i)) for i in range(3)]
        self.selected_piece = None
        self.selected_tile = None
        self.win = win
        #to know the selected piece was from which part (board,left_pane,right_pane)
        self.to_board = None
        self.to_left_pane = None
        self.to_right_pane = None
        
        self.turn = 0 #black gobblet starts

        self.repetition_draw = False  #Flag to indicate DRAW when repeating moves

        #rows,columns,diagonals which have 3 elements to allow gobbling it from external stack
        self.critical_case_row = []   #0 ->3 where 0 is the upper row
        self.critical_case_col = []   #0 ->3 where 0 is the leftmost col
        self.critical_case_diag = 0 
        self.critical_case_antidiag = 0  


        #row and column value which is selected
        self.current_row = None
        self.current_col = None

        #array of (size,pos_x,pos_y)
        self.white_prev_moves = [(0, 0, 0) for _ in range(6)]
        self.black_prev_moves = [(0, 0, 0) for _ in range(6)]
        self.white_tuple_array_counter = 0
        self.black_tuple_array_counter = 0
        self.white_repetition =0
        self.black_repetition =0

        self.draw_stack_panels()
        self.draw_initial_board()

        for i in range(3):
            for j in range(4):
                self.left_stack_panel[i].pieces_stack.append(
                    Piece(Color.DARK, j+1))
                self.right_stack_panel[i].pieces_stack.append(
                    Piece(Color.LIGHT, j+1))
            self.draw_piece(
                self.left_stack_panel[i].pieces_stack[-1], self.left_stack_panel[i])
            self.draw_piece(
                self.right_stack_panel[i].pieces_stack[-1], self.right_stack_panel[i])
        Button.draw_hover_button(win, RIGHT_PANE_START - MARGIN, MARGIN, BUTTON_HEIGHT, BUTTON_HEIGHT,
                             "||", BEIGE, HOVER_COLOR)

    def check_repetition(self,size,pos_x,pos_y,turn):
        if(turn):
            self.white_prev_moves[self.white_tuple_array_counter] = (size,pos_x,pos_y)
            self.white_tuple_array_counter = (self.white_tuple_array_counter + 1) % 6
        elif(not turn):
            self.black_prev_moves[self.black_tuple_array_counter] = (size,pos_x,pos_y)
            self.black_tuple_array_counter = (self.black_tuple_array_counter + 1) % 6
        # print("white prev:",self.white_prev_moves)
        # print("black prev:",self.black_prev_moves)
        if self.white_prev_moves[0] !=(0,0,0) and ((self.white_prev_moves[0]==self.white_prev_moves[2]==self.white_prev_moves[4]) and(self.white_prev_moves[1]==self.white_prev_moves[3]==self.white_prev_moves[5])):
            self.white_repetition = 1
        if self.white_prev_moves[0] !=(0,0,0) and ((self.black_prev_moves[0]==self.black_prev_moves[2]==self.black_prev_moves[4]) and(self.black_prev_moves[1]==self.black_prev_moves[3]==self.black_prev_moves[5])):
            self.black_repetition = 1
        if(self.white_repetition == self.black_repetition == 1):
            print("----Draw----")
            self.repetition_draw = True

    def check_moves_for_selected_piece(self,tile):
        # self.check_stuck_due_to_size()
        # for row in  self.board:
        #     for cell in row:
        #         if not self.check_size(tile,cell):
        #             return True
        for i in range(4):
            for j in range(4):
                if self.check_size(tile,self.board[i][j]):
                    return True
        print("no Moveeees")
        return False
    
    def draw_initial_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_SIZE + BOARD_START_X
                y = row * SQUARE_SIZE + MARGIN
                self.board[row][col] = Tile(x, y)
                pygame.draw.rect(self.win, BEIGE if (row + col) % 2 == 0 else BROWN,
                                 (x, y, SQUARE_SIZE, SQUARE_SIZE))

    def draw_stack_panels(self):

        pygame.draw.rect(
            self.win, FOREGROUND, (LEFT_PANE_START, MARGIN, SQUARE_SIZE, BOARD_SIZE))

        # Draw the right sub-board
        pygame.draw.rect(
            self.win, FOREGROUND, (RIGHT_PANE_START, MARGIN, SQUARE_SIZE, BOARD_SIZE))

    def move(self, old_tile, new_tile):
        new_tile.push_piece(old_tile.pop_piece())
        self.draw_piece(new_tile.pieces_stack[-1], new_tile)
        self.draw_tile(old_tile)
        self.to_right_pane = 0
        self.to_left_pane = 0
        self.to_board = 0
        self.turn ^= 1  
        self.check_win()
        self.check_repetition(new_tile.pieces_stack[-1].size,new_tile.pos_x,new_tile.pos_y,not self.turn)
        


    def draw_tile(self, tile):
        pygame.draw.rect(self.win, self.win.get_at((int(tile.pos_x + STROKE + 1), int(tile.pos_y + STROKE + 1))),
                         (tile.pos_x, tile.pos_y, SQUARE_SIZE, SQUARE_SIZE))
        # If the tile is not empty (still has pieces left after removal)
        if tile.pieces_stack != []:
            # Draw the piece on top of the stack
            self.draw_piece(tile.pieces_stack[-1], tile)

    def draw_piece(self, piece, tile):

        gobblet = pygame.transform.smoothscale(
            pygame.image.load(
                'asset\dark_gobblet.png' if piece.color == Color.DARK else 'asset\light_gobblet.png'),
            (PIECE_SIZE * (0.4 + piece.size * 0.15), PIECE_SIZE * (0.4 + piece.size * 0.15)))
        size = gobblet.get_size()[0] // 2
        self.win.blit(gobblet, (tile.pos_x + SQUARE_SIZE/2 -
                 size, tile.pos_y + SQUARE_SIZE / 2 - size))
        # win.blit(gobblet, (tile.pos_x, tile.pos_y))

    def select(self):
        #tile new , self.selected_tile = old
        pos = pygame.mouse.get_pos()
        tile = self.get_tile_from_pos(pos)
        if tile != None and self.selected_tile != None:
            # Check move validity
            # check game rules
            if self.game_Rules(self.selected_tile,tile,False):
                self.move(self.selected_tile, tile)
                self.selected_tile = None

        elif tile != None and tile.pieces_stack != [] and (tile.pieces_stack[-1].color.value == self.turn):
            self.check_moves_for_selected_piece(tile)
            self.selected_tile = tile
            # self.first_sel = self.to_left_pane or self.to_right_pane
            # print(self.first_sel)  
            self.highlight_tile(tile)
        
    
    #rule for moving pieces when first selection is external stack
    def game_Rules(self,old_tile,new_tile,in_test):
        # print("Entered game rules")
        row = int((new_tile.pos_y - MARGIN) // SQUARE_SIZE)
        col = int((new_tile.pos_x - BOARD_START_X) // SQUARE_SIZE)
        # print("row.....",row)
        # print("critical_row.....",self.critical_case_row)
        #can't go from board to external stacks or go from external stack to external stack
        if(self.to_right_pane or self.to_left_pane): 
        #    print("can't make move")
           return 0
        elif(self.to_board):
            #go within board or from external stack to board
            if self.tile_inside_board(old_tile):
                # print("board game rules")
                return self.check_size(old_tile,new_tile)
            elif new_tile.pieces_stack == []: #empty tile
                # print("going to board")
                return 1
            elif(row in self.critical_case_row or col in self.critical_case_col or self.critical_case_diag !=0 or self.critical_case_antidiag != 0): #allow gobbling from external stack in critical case (3 in same row)
                if not in_test:
                    if(row in self.critical_case_row): self.critical_case_row.remove(row)
                    if(col in self.critical_case_col): self.critical_case_col.remove(col)
                    self.critical_case_diag = 0
                    self.critical_case_antidiag = 0
                # print("new list",self.critical_case_row)
                return self.check_size(old_tile,new_tile)
    
    
    def tile_inside_board(self, tile):
        if tile.pos_y > MARGIN and tile.pos_y < BOARD_SIZE + MARGIN and tile.pos_x > BOARD_START_X and tile.pos_x < BOARD_START_X + BOARD_SIZE:
            return True
        return False
            
                
    #rule for moving pieces within board
    # def game_Rules_board(self,old_tile,new_tile):
    #     # print("Entered game rules board")
    #     # row = int((new_tile.pos_y - MARGIN) // SQUARE_SIZE)
    #     # print("row.....",row)
    #     # print("critical_row.....",self.critical_case_row)
    #     #can't go from board to external stacks or go from external stack to external stack
    #     if(self.to_right_pane or self.to_left_pane): 
    #        print("can't make move")
    #        return 0
    #     elif(self.to_board):
    #         #go within board or from external stack to board
    #         print("board game rules")
    #         return self.check_size(old_tile,new_tile)
            
             
 
    def is_row_aligned(self,color):
    # Check if any row is fully occupied by the player 
        for row_index,row in enumerate(self.board): #enumerate is to add an index to an iteratable
            positions = [row_index for row_index, cell in enumerate(row) if (cell.pieces_stack!=[] and cell.pieces_stack[-1].color == color)]
            if len(positions) == 3 :
                if(not row_index in self.critical_case_row):
                    self.critical_case_row.append(row_index)
                    # print("the row is: ",row_index)
            elif len(positions) == 4:
                return True
            

        return False
    def is_column_aligned(self,color):
        # Check if any col is fully occupied by the player 
        for col_index,col in enumerate(zip(*self.board)): #enumerate is to add an index to an iteratable
            positions = [col_index for col_index, cell in enumerate(col) if (cell.pieces_stack!=[] and cell.pieces_stack[-1].color == color)]
            if len(positions) == 3 :
                if(not col_index in self.critical_case_col):
                    self.critical_case_col.append(col_index)
                    # print("the column is: ",col_index)
            elif len(positions) == 4:
                return True
            
        return False


    def is_diagonal_aligned(self, color):
        # Check if any diagonal is fully occupied by the player 
        # Main diagonal
        main_diagonal_positions = [i for i in range(4) if (self.board[i][i].pieces_stack != [] and self.board[i][i].pieces_stack[-1].color == color)]
        if len(main_diagonal_positions) == 3:
            self.critical_case_diag = 1
        elif len(main_diagonal_positions) == 4:
            return True

        # Antidiagonal
        antidiagonal_positions = [i for i in range(4) if (self.board[i][3 - i].pieces_stack != [] and self.board[i][3 - i].pieces_stack[-1].color == color)]
        if len(antidiagonal_positions) == 3:
            self.critical_case_antidiag = 1
        elif len(antidiagonal_positions) == 4:
            return True

        return False


    # def is_diagonal_aligned(self, color):
    #     # Check if any diagonal is fully occupied by the player 
    #     # Main diagonal
    #     if all((self.board[i][i].pieces_stack!=[] and self.board[i][i].pieces_stack[-1].color == color) for i in range(4)):
    #         return True
    #     # Antidiagonal
    #     if all((self.board[i][3-i].pieces_stack!=[] and self.board[i][3 - i].pieces_stack[-1].color == color) for i in range(4)):
    #         return True
    #     return False

    def check_alignment(self,color):
        # Check for alignment in rows, columns, or diagonals for a player 
        return (self.is_row_aligned(color) or self.is_column_aligned(color) or self.is_diagonal_aligned(color) )
    
    def check_win(self):
        dark =  self.check_alignment(Color.DARK)
        light =  self.check_alignment(Color.LIGHT)
        if((light and dark) or self.repetition_draw):
            print(self.repetition_draw)
            return 0
            print("----DRAW----")
        elif(light and not dark):
            return 1
            print("--Light wins--: ",light)
        elif(dark and not light):
            return -1
            print("--Dark wins--: ",dark)
        else:
            return 2

    def check_size(self,old_tile,new_tile):
        if(new_tile.pieces_stack!=[] and old_tile.pieces_stack!=[]):
            if(old_tile.pieces_stack[-1].size<=new_tile.pieces_stack[-1].size):
                return 0
        return 1
            

    def highlight_tile(self, tile):
        pygame.draw.line(self.win, BLUE, (tile.pos_x + STROKE // 2 - 1, tile.pos_y), (tile.pos_x + STROKE // 2 - 1, tile.pos_y + SQUARE_SIZE - 1), STROKE)
        pygame.draw.line(self.win, BLUE, (tile.pos_x, tile.pos_y + STROKE // 2 - 1), (tile.pos_x + SQUARE_SIZE - 1, tile.pos_y + STROKE // 2 - 1), STROKE)
        pygame.draw.line(self.win, BLUE, (tile.pos_x + SQUARE_SIZE - STROKE // 2 - 1, tile.pos_y), (tile.pos_x + SQUARE_SIZE - STROKE // 2 - 1, tile.pos_y + SQUARE_SIZE - 1), STROKE)
        pygame.draw.line(self.win, BLUE, (tile.pos_x, tile.pos_y + SQUARE_SIZE - STROKE // 2 - 1), (tile.pos_x + SQUARE_SIZE - 1, tile.pos_y + SQUARE_SIZE - STROKE // 2 - 1), STROKE)

    def get_tile_from_pos(self, pos):
        mouse_x, mouse_y = pos
        if mouse_y < MARGIN or mouse_y > BOARD_SIZE + MARGIN:
            return None

        elif mouse_y > MARGIN + SQUARE_SIZE // 2 and mouse_y < MARGIN + 3.5 * SQUARE_SIZE:
            if mouse_x > RIGHT_PANE_START and mouse_x < RIGHT_PANE_START + SQUARE_SIZE:
                row = int((mouse_y - MARGIN - SQUARE_SIZE / 2) // SQUARE_SIZE)
                # print(row)
                self.to_right_pane = 1
                self.to_left_pane = 0
                self.to_board = 0
                return self.right_stack_panel[row]

            if mouse_x > LEFT_PANE_START and mouse_x < LEFT_PANE_START + SQUARE_SIZE:
                row = int((mouse_y - MARGIN - SQUARE_SIZE / 2) // SQUARE_SIZE)
                # print(row)
                self.to_left_pane = 1
                self.to_right_pane = 0
                self.to_board = 0
                return self.left_stack_panel[row]

        if mouse_x > BOARD_START_X and mouse_x < BOARD_START_X + BOARD_SIZE:
            row = int((mouse_y - MARGIN) // SQUARE_SIZE)
            col = int((mouse_x - BOARD_START_X) // SQUARE_SIZE)
            self.current_row = row
            self.current_col = col
            # print(row, col)
            self.to_board = 1
            self.to_left_pane = 0
            self.to_right_pane = 0
            return self.board[row][col]

        return None


    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_SIZE + BOARD_START_X
                y = row * SQUARE_SIZE + MARGIN
                pygame.draw.rect(self.win, BEIGE if (row + col) % 2 == 0 else BROWN,
                                 (x, y, SQUARE_SIZE, SQUARE_SIZE))
                self.draw_tile(self.board[row][col])

    def draw_game(self):
        self.win.fill(BACKGROUND)
        self.draw_board()
        self.draw_stack_panels()
        for i in range(3):
            self.draw_tile(self.left_stack_panel[i])
            self.draw_tile(self.right_stack_panel[i])
        Button.draw_hover_button(self.win, RIGHT_PANE_START - MARGIN, MARGIN, BUTTON_HEIGHT, BUTTON_HEIGHT,
                             "||", BEIGE, HOVER_COLOR)



    # def evaluate(self, color):
    #     player_wins = self.check_win() #white returns 1, Dark return -1,draw return 0

    #     if player_wins==1: #light
    #         return float('inf')  # Positive infinity for a winning state
    #     elif player_wins == -1: #dark
    #         return float('-inf')  # Negative infinity for a losing state
    #     elif player_wins == 0:
    #         return float('-9999') #draw

    #     # Evaluate based on the number of potential winning lines for the player
    #     player_lines = self.count_potential_lines(color)
    #     opponent_lines = self.count_potential_lines((color+1)%2)
 
