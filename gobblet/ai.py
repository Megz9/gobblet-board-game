import pygame

from gobblet.constants import MAX_DEPTH, Color

class MinMax:

    available_moves = []
    # def game_Rules(self,win,old_tile,new_tile):

    def minimax(board, player, depth):
        print("Entered Minimax")
        # print(depth)
        # print(player)
        pane = [board.right_stack_panel, board.left_stack_panel]
        if depth == MAX_DEPTH or board.check_win() != 2:
            print(board.check_win())
            print("Depth is max")
            print(depth)
            return MinMax.evaluate(board, player)

        list = []
        for i in range(3): # stack pane evaluation of current player
            list += MinMax.evaluate_possible_moves(pane[player][i], board, player, depth, board.game_Rules)

        for i in range(4):
            for j in range(4): # board evaluation
                list += MinMax.evaluate_possible_moves(board.board[i][j], board, player, depth, board.game_Rules_board)

        if len(list) == 0: # Leaf node
            return MinMax.evaluate(board, player)
        print(depth)
        if depth == 0:
            print("Making move")
            print("List: ", len(list))
            print("Moves List: ", len(MinMax.available_moves))
            next_move = MinMax.available_moves[list.index(max(list) if player else min(list))]
            board.move(board.win, next_move[0], next_move[1])
                
        return max(list) if player else min(list)

    def evaluate_possible_moves(tile, board, player, depth, is_valid_move):
        # print("depth", depth)
        # if len(tile.pieces_stack) != 0:
        #     # print(tile.pieces_stack[-1].color.value)
        #     print("player ", player)
        list = []
        if len(tile.pieces_stack) != 0 and tile.pieces_stack[-1].color.value == player:
            # print("Entered IFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
            for i in range(4):
                for j in range(4):
                    board.turn = 1 - player
                    board.to_board = 1
                    if is_valid_move(None, tile, board.board[i][j]):
                        print("Old tile: ", tile.pos_x, tile.pos_y)
                        print("New tile: ", board.board[i][j].pos_x, board.board[i][j].pos_y)
                        # print("Entered")
                        board.board[i][j].push_piece(tile.pop_piece())
                        if depth == 0:
                            MinMax.available_moves.append((tile, board.board[i][j]))
                        # print("depth + 1", depth + 1)
                        list.append(MinMax.minimax(board, 1 - player, depth + 1))
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

    # def allowed_move(self):
    #     pass

    #     # Consider the size of the pieces on the board
    #     player_piece_size = board.get_largest_piece_size(player)
    #     opponent_piece_size = board.get_largest_piece_size(3 - player)

    #     # Assign weights to factors based on importance
    #     player_lines_weight = 1.0
    #     opponent_lines_weight = -1.0  # Discourage the opponent from winning
    #     player_piece_size_weight = 0.5
    #     opponent_piece_size_weight = -0.5  # Discourage the opponent from having large pieces

    #     # Combine values into an overall evaluation score
    #     evaluation_score = (
    #         player_lines * player_lines_weight +
    #         opponent_lines * opponent_lines_weight +
    #         player_piece_size * player_piece_size_weight +
    #         opponent_piece_size * opponent_piece_size_weight
    #     )

    #     return evaluation_score
