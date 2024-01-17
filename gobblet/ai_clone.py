import pygame

from gobblet.constants import INFINITY, MAX_DEPTH, Color

class MinMax2:

    available_moves = []
    # def game_Rules(self,win,old_tile,new_tile):

    def minimax(board, depth):
        pane = [board.right_stack_panel, board.left_stack_panel]
        # backup = MinMax2.backup(board)
        isLeaf = board.check_win() != 2
        if depth == MAX_DEPTH or isLeaf:
            return MinMax2.evaluate(board,depth)
        # MinMax2.restore(backup, board)
        list = []
        for i in range(3): # stack pane evaluation of current player
            list += MinMax2.evaluate_possible_moves(pane[board.turn][i], board, board.turn, depth)

        for i in range(4):
            for j in range(4): # board evaluation
                list += MinMax2.evaluate_possible_moves(board.board[i][j], board, board.turn, depth)

        if len(list) == 0: # Leaf node
            return MinMax2.evaluate(board,depth)

        if depth == 0:
            print(list)
            print(max(list) if board.turn else min(list))
            print(list.index(max(list) if board.turn else min(list)))
            next_move = MinMax2.available_moves[list.index(max(list) if board.turn else min(list))]
            board.move(next_move[0], next_move[1])
        return max(list) if board.turn else min(list)



    def evaluate_possible_moves(tile, board, player, depth):
        list = []
        if len(tile.pieces_stack) != 0 and tile.pieces_stack[-1].color.value == player:
            for i in range(4):
                for j in range(4):
                    board.to_board = 1
                    backup = MinMax2.backup(board)
                    if board.game_Rules(tile, board.board[i][j]):
                        board.board[i][j].push_piece(tile.pop_piece())
                        if depth == 0:
                            # print(i,"      ",j)
                            MinMax2.available_moves.append((tile, board.board[i][j]))
                        board.turn = 1-player
                        list.append(MinMax2.minimax(board, depth + 1))
                        # board.turn = player
                        tile.push_piece(board.board[i][j].pop_piece())
                    MinMax2.restore(backup, board)
        return list
    
    def evaluate(board,depth):
        # backup = MinMax2.backup(board)
        winner = board.check_win()
        # MinMax2.restore(backup, board)
        if winner == 1: return -INFINITY+depth
        elif winner == -1: return INFINITY-depth
        elif winner == 0: return 0
        n_human, n_ai, s_human, s_ai = 0, 0, 0, 0
        rows_ai, cols_ai, diag_ai, rows_human, cols_human, diag_human = [0, 0, 0, 0], [0, 0, 0, 0], [0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0]
        left_diagonal_count, right_diagonal_count = 0, 0
        count = []
        for i in range(4):
            row_count, col_count = 0, 0
            left_diagonal_count += MinMax2.evaluate_tile(board.board[i][i], i, i)
            right_diagonal_count += MinMax2.evaluate_tile(board.board[i][3 - i], i, i)
            for j in range(4):
                row_count += MinMax2.evaluate_tile(board.board[i][j], i, j)
                col_count += MinMax2.evaluate_tile(board.board[j][i], i, j)
                if len(board.board[i][j].pieces_stack) !=0:
                    if board.board[i][j].pieces_stack[-1].color == Color.LIGHT:
                        n_human += 1
                        s_human += board.board[i][j].pieces_stack[-1].size
                        rows_human[i] += 1
                        cols_human[j] += 1
                        if i == j: diag_human[0] += 1
                        if i == 3 - j: diag_human[1] += 1
                    else:
                        n_ai += 1
                        s_ai += board.board[i][j].pieces_stack[-1].size
                        rows_ai[i] += 1
                        cols_ai[j] += 1
                        if i == j: diag_ai[0] += 1
                        if i == 3 - j: diag_ai[1] += 1
            count.extend([row_count, col_count])
        count.extend([left_diagonal_count, right_diagonal_count])
        
        w_ai = rows_ai.count(3) + cols_ai.count(3) + diag_ai.count(3)
        c_ai = 10 - rows_ai.count(0) + cols_ai.count(0) + diag_ai.count(0)

        w_human = rows_human.count(3) + cols_human.count(3) + diag_human.count(3)
        c_human = 10 - rows_human.count(0) + cols_human.count(0) + diag_human.count(0)

        critical_val = max(count) if board.turn ^ (MAX_DEPTH % 2) else min(count)
        return 10 * (n_ai - n_human) + 100 * (w_ai - w_human) + 5 * (c_ai - c_human) + (s_ai - s_human) + 1.5 * critical_val


    def evaluate_tile(tile, i, j):
        if len(tile.pieces_stack) == 0: return 0
        # if len(tile.pieces_stack) == 0: return 3 if i == j or i == (3 - j) else 2
        val = (3 if i == j or i == (3 - j) else 2) * (16 + tile.pieces_stack[-1].size)
        return val if tile.pieces_stack[-1].color == Color.DARK else -val


    def backup(board):
        return [board.critical_case_row.copy(),
                board.critical_case_col.copy(),
                board.critical_case_diag,
                board.critical_case_antidiag,
                board.white_prev_moves.copy(),
                board.black_prev_moves.copy(),
                board.white_tuple_array_counter,
                board.black_tuple_array_counter,
                board.turn,
                board.repetition_draw]

    def restore(list, board):
        board.critical_case_row = list[0]
        board.critical_case_col = list[1]
        board.critical_case_diag = list[2]
        board.critical_case_antidiag = list[3]
        board.white_prev_moves = list[4]
        board.black_prev_moves = list[5]
        board.white_tuple_array_counter = list[6]
        board.black_tuple_array_counter = list[7]
        board.turn = list[8]
        board.repetition_draw = list[9]
        
        
        # [[], [], 0, 0, [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)], [(4, 512.0, 25.0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)], 0, 1, 1, False
        # [[], [], 0, 0, [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)], [(4, 512.0, 25.0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)], 0, 1, 1, False