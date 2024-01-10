import pygame

from gobblet.constants import MAX_DEPTH, Color

class MinMax:

    available_moves = []
    # def game_Rules(self,win,old_tile,new_tile):

    def minimax(board, depth):
        pane = [board.right_stack_panel, board.left_stack_panel]
        if depth == MAX_DEPTH or board.check_win() != 2:
            return MinMax.evaluate(board)

        list = []
        for i in range(3): # stack pane evaluation of current player
            list += MinMax.evaluate_possible_moves(pane[board.turn][i], board, board.turn, depth)

        for i in range(4):
            for j in range(4): # board evaluation
                list += MinMax.evaluate_possible_moves(board.board[i][j], board, board.turn, depth)

        if len(list) == 0: # Leaf node
            return MinMax.evaluate(board)

        if depth == 0:
            next_move = MinMax.available_moves[list.index(max(list) if board.turn else min(list))]
            board.move(next_move[0], next_move[1])
        return max(list) if board.turn else min(list)



    def evaluate_possible_moves(tile, board, player, depth):
        list = []
        if len(tile.pieces_stack) != 0 and tile.pieces_stack[-1].color.value == player:
            for i in range(4):
                for j in range(4):
                    board.to_board = 1
                    if board.game_Rules(tile, board.board[i][j]):
                        board.board[i][j].push_piece(tile.pop_piece())
                        if depth == 0:
                            MinMax.available_moves.append((tile, board.board[i][j]))
                        board.turn = 1-player
                        list.append(MinMax.minimax(board, depth + 1))
                        board.turn = player
                        tile.push_piece(board.board[i][j].pop_piece())
        return list
    
    # f[player] * (w - b)
    def evaluate(board, player):
        count = 0
        for i in range(4):
            count += MinMax.evaluate_tile(board.board[i][i], player) + \
                MinMax.evaluate_tile(board.board[i][3 - i], player)
            for j in range(4):
                count += MinMax.evaluate_tile(board.board[i][j], player) + \
                    MinMax.evaluate_tile(board.board[j][i], player)
        return count

    def evaluate_tile(tile, player):
        f = [1, -1]
        white_count = 0
        black_count = 0
        count = 0
        if len(tile.pieces_stack) == 0:
            count += 1
        elif tile.pieces_stack[-1].color == Color.LIGHT:
            white_count += (tile.pieces_stack[-1].size + 1)
        else:
            black_count += (tile.pieces_stack[-1].size + 1)

        return f[player] * (white_count - black_count) + count

