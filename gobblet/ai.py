import pygame

from gobblet.constants import INFINITY, MAX_DEPTH, Color

class MinMax:

    available_moves = []
    # def game_Rules(self,win,old_tile,new_tile):

    def minimax(board, depth):
        pane = [board.right_stack_panel, board.left_stack_panel]
        if depth == MAX_DEPTH or board.check_win() != 2:
            return MinMax.evaluate(board,depth)

        list = []
        for i in range(3): # stack pane evaluation of current player
            list += MinMax.evaluate_possible_moves(pane[board.turn][i], board, board.turn, depth)

        for i in range(4):
            for j in range(4): # board evaluation
                list += MinMax.evaluate_possible_moves(board.board[i][j], board, board.turn, depth)

        if len(list) == 0: # Leaf node
            return MinMax.evaluate(board,depth)

        if depth == 0:
            print(list)
            print(max(list) if board.turn else min(list))
            print(list.index(max(list) if board.turn else min(list)))
            next_move = MinMax.available_moves[list.index(max(list) if board.turn else min(list))]
            board.move(next_move[0], next_move[1])
        return max(list) if board.turn else min(list)



    def evaluate_possible_moves(tile, board, player, depth):
        list = []
        if len(tile.pieces_stack) != 0 and tile.pieces_stack[-1].color.value == player:
            for i in range(4):
                for j in range(4):
                    board.to_board = 1
                    if depth==0 :print(board.game_Rules(tile, board.board[i][j],True))
                    if board.game_Rules(tile, board.board[i][j],True):
                        board.board[i][j].push_piece(tile.pop_piece())
                        if depth == 0:
                            print(i,"      ",j)
                            MinMax.available_moves.append((tile, board.board[i][j]))
                        board.turn = 1-player
                        list.append(MinMax.minimax(board, depth + 1))
                        board.turn = player
                        tile.push_piece(board.board[i][j].pop_piece())
        return list
    
    def evaluate(board,depth):
        if board.check_win() == 1:
            return -INFINITY+depth
        elif board.check_win() == -1:
            return INFINITY-depth
        n_human, n_ai, s_human, s_ai = 0, 0, 0, 0
        rows_ai, cols_ai, diag_ai, rows_human, cols_human, diag_human = [0, 0, 0, 0], [0, 0, 0, 0], [0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0]
        left_diagonal_count, right_diagonal_count = 0, 0
        count = []
        for i in range(4):
            row_count, col_count = 0, 0
            left_diagonal_count += MinMax.evaluate_tile(board.board[i][i], i, i)
            right_diagonal_count += MinMax.evaluate_tile(board.board[i][3 - i], i, i)
            for j in range(4):
                row_count += MinMax.evaluate_tile(board.board[i][j], i, j)
                col_count += MinMax.evaluate_tile(board.board[j][i], i, j)
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

        critical_val = max(count) if not board.turn else min(count)

        return 10 * (n_ai - n_human) + 100 * (w_ai - w_human) + 5 * (c_ai - c_human) + (s_ai - s_human) + 2 * critical_val
            

    def evaluate_tile(tile, i, j):
        if len(tile.pieces_stack) == 0:
            return 3 if i == j or i == (3 - j) else 2
        val = (3 if i == j or i == (3 - j) else 2) * (16 + tile.pieces_stack[-1].size)
        return val if tile.pieces_stack[-1].color == Color.DARK else -val

