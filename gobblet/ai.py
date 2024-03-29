import pygame

from gobblet.constants import INFINITY, MAX_DEPTH, Color,MAX_TIME



class MinMax:
    Draw_Request=0
    Tried_Draw_Once=0
    No_Move=0
    available_moves = []
    start_time=0
    iterative_depth=MAX_DEPTH
    rootlist=[]

    
    def minimax(board, depth, difficulty):
        pane = [board.right_stack_panel, board.left_stack_panel]
        isLeaf = board.check_win() != 2
        if depth == MAX_DEPTH or isLeaf:
            if difficulty == 0: return MinMax.evaluate_easy(board,depth)
            if difficulty == 1: return MinMax.evaluate_medium(board,depth)
            if difficulty == 2: return MinMax.evaluate_hard(board,depth)
        list = []
        for i in range(3): # stack pane evaluation of current player
            list += MinMax.evaluate_possible_moves(pane[board.turn][i], board, board.turn, depth, difficulty)

        for i in range(4):
            for j in range(4): # board evaluation
                list += MinMax.evaluate_possible_moves(board.board[i][j], board, board.turn, depth, difficulty)

        if len(list) == 0: # Leaf node
            if difficulty == 0: return MinMax.evaluate_easy(board,depth)
            if difficulty == 1: return MinMax.evaluate_medium(board,depth)
            if difficulty == 2: return MinMax.evaluate_hard(board,depth)

        if depth == 0:
            print(list)
            print(max(list) if board.turn else min(list))
            print(list.index(max(list) if board.turn else min(list)))
            if board.turn and (max(list)<-INFINITY+10) and MinMax.Tried_Draw_Once==0 :
                #condition to check double draaw request
                MinMax.Draw_Request=1
                return
            MinMax.Tried_Draw_Once=0
            next_move = MinMax.available_moves[list.index(max(list) if board.turn else min(list))]
            if MinMax.No_Move==0:

                board.move(next_move[0], next_move[1])
        return max(list) if board.turn else min(list)

    def evaluate_possible_moves(tile, board, player, depth, difficulty):
        list = []
        if len(tile.pieces_stack) != 0 and tile.pieces_stack[-1].color.value == player:
            for i in range(4):
                for j in range(4):
                    board.to_board = 1
                    backup = MinMax.backup(board)
                    if board.game_Rules(tile, board.board[i][j]):
                        board.board[i][j].push_piece(tile.pop_piece())
                        if depth == 0:
                            # print(i,"      ",j)
                            MinMax.available_moves.append((tile, board.board[i][j]))
                        board.turn = 1-player
                        list.append(MinMax.minimax(board, depth + 1, difficulty))
                        # board.turn = player
                        tile.push_piece(board.board[i][j].pop_piece())
                    MinMax.restore(backup, board)
        return list
    
    def evaluate_hard(board, depth):
        winner = board.check_win()
        if winner == 1: return -INFINITY + depth
        elif winner == -1: return INFINITY - depth
        elif winner == 0: return 0
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

        critical_val = max(count) if board.turn ^ (MAX_DEPTH % 2) else min(count)
        return 10 * (n_ai - n_human) + 100 * (w_ai - w_human) + 5 * (c_ai - c_human) + (s_ai - s_human) + critical_val


    def evaluate_medium(board, depth):
        winner = board.check_win()
        if winner == 1: return -INFINITY + depth
        elif winner == -1: return INFINITY - depth
        elif winner == 0: return 0
        n_human, n_ai, s_human, s_ai = 0, 0, 0, 0
        rows_ai, cols_ai, diag_ai, rows_human, cols_human, diag_human = [0, 0, 0, 0], [0, 0, 0, 0], [0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0]
        for i in range(4):
            for j in range(4):
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
        
        w_ai = rows_ai.count(3) + cols_ai.count(3) + diag_ai.count(3)
        c_ai = 10 - rows_ai.count(0) + cols_ai.count(0) + diag_ai.count(0)

        w_human = rows_human.count(3) + cols_human.count(3) + diag_human.count(3)
        c_human = 10 - rows_human.count(0) + cols_human.count(0) + diag_human.count(0)

        return 10 * (n_ai - n_human) + 100 * (w_ai - w_human) + 5 * (c_ai - c_human) + (s_ai - s_human)

    def evaluate_easy(board, depth):
        winner = board.check_win()
        if winner == 1: return -INFINITY + depth
        elif winner == -1: return INFINITY - depth
        elif winner == 0: return 0
        n_human, n_ai = 0, 0
        for i in range(4):
            for j in range(4):
                if len(board.board[i][j].pieces_stack) !=0:
                    if board.board[i][j].pieces_stack[-1].color == Color.LIGHT: n_human += 1
                    else: n_ai += 1
        return 10 * (n_ai - n_human)

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
    
    ####################################################
    #minmax with iterative deeping and timing constraint
    def minMaxPruning_IterativeDeeping_withTimeConstraints(board,difficulty):
        MinMax.start_time = pygame.time.get_ticks()
        MinMax.iterative_depth=1
        current_best_move =None
        for i in range(1,MAX_DEPTH+1,1):
            
            if (((pygame.time.get_ticks()-MinMax.start_time)/1000 )<MAX_TIME):
                current_eval = MinMax.minimax_with_pruning_itr(board, 0,-INFINITY,INFINITY,difficulty)
                
                if current_eval != None:
                    Previous_Eval=current_eval
                    print("aaaaaaaaaa:",i,"time:",(pygame.time.get_ticks()-MinMax.start_time)/1000 )
                    

                    current_best_move = MinMax.available_moves[MinMax.rootlist.index(max(MinMax.rootlist) if board.turn else min(MinMax.rootlist))]
        
                    MinMax.iterative_depth+=1
                else:
                    break
        
        if board.turn and (Previous_Eval<-INFINITY+10) and MinMax.Tried_Draw_Once==0 :
            #condition to check double draaw request
            MinMax.Draw_Request=1
            return
        MinMax.Tried_Draw_Once=0
        if MinMax.No_Move==0:
            board.move(current_best_move[0], current_best_move[1])

        
    def minimax_with_pruning_itr(board, depth,alpha,beta,difficulty):
        # MinMax.counter +=1
        pane = [board.right_stack_panel, board.left_stack_panel]
        if (((pygame.time.get_ticks()-MinMax.start_time)/1000)>MAX_TIME):
            print(f"curr time:{((pygame.time.get_ticks()-MinMax.start_time)/1000)},max time{MAX_TIME}")
            return None
        isLeaf = board.check_win() != 2
        if depth == MinMax.iterative_depth or isLeaf:
            if difficulty == 0: return MinMax.evaluate_easy(board,depth)
            if difficulty == 1: return MinMax.evaluate_medium(board,depth)
            if difficulty == 2: return MinMax.evaluate_hard(board,depth)

        list = []
        for i in range(3): # stack pane evaluation of current player
            current_list, to_be_pruned = MinMax.evaluate_possible_moves_pruning_itr(pane[board.turn][i], board, board.turn, depth,alpha,beta,difficulty)
            if current_list == None:
                return None
            list += current_list
            if to_be_pruned ==True and depth != 0:
                return max(list) if board.turn else min(list)
                # return current_list               
            # elif  to_be_pruned ==False: 
            #     list += current_list
            

        for i in range(4):
            for j in range(4): # board evaluation
                current_list, to_be_pruned = MinMax.evaluate_possible_moves_pruning_itr(board.board[i][j], board, board.turn, depth,alpha,beta,difficulty)
                if current_list == None:
                    return None
                list+=current_list
                if to_be_pruned ==True and depth != 0:
                    return max(list) if board.turn else min(list)
                    # return current_list               
                # elif  to_be_pruned ==False: 
                #     list += current_list
                


        if len(list) == 0: # Leaf node
            if difficulty == 0: return MinMax.evaluate_easy(board,depth)
            if difficulty == 1: return MinMax.evaluate_medium(board,depth)
            if difficulty == 2: return MinMax.evaluate_hard(board,depth)

        if depth == 0:
            MinMax.rootlist=list
            print(list)
            print(max(list) if board.turn else min(list))
            print(list.index(max(list) if board.turn else min(list)))
            # max_index = max(range(len(MinMax.available_moves)), key=lambda i: MinMax.available_moves[i][2])
            # min_index = min(range(len(MinMax.available_moves)), key=lambda i: MinMax.available_moves[i][2])
            # next_move = MinMax.available_moves[list.index(max(list) if board.turn else min(list))]
            # next_move = MinMax.available_moves[max_index] if board.turn else MinMax.available_moves[min_index]
            # for move in MinMax.available_moves:
            #     print("in func",move[2],end=" ") 
            # print(f"in func max,min:{max_index},{min_index}")

            # board.move(next_move[0], next_move[1])
        return max(list) if board.turn else min(list)
                

    def evaluate_possible_moves_pruning_itr(tile, board, player, depth, alpha, beta,difficulty):
        if (((pygame.time.get_ticks()-MinMax.start_time)/1000)>MAX_TIME):
            return None,True
        list = []
        if len(tile.pieces_stack) != 0 and tile.pieces_stack[-1].color.value == player:
            for i in range(4):
                for j in range(4):
                    board.to_board = 1
                    backup = MinMax.backup(board)

                    if board.game_Rules(tile, board.board[i][j]):
                        board.board[i][j].push_piece(tile.pop_piece())
                        if depth == 0:
                            # if not(val ==None):
                                MinMax.available_moves.append((tile, board.board[i][j]))
                            # else:
                                # print ("val: ",val)
                        board.turn = 1-player
                        val  =  MinMax.minimax_with_pruning_itr(board, depth + 1,alpha,beta,difficulty)
                        tile.push_piece(board.board[i][j].pop_piece())
                        board.turn = player

                        # print("depth: ",depth,"player: ",player," ,val: ",val,",alpha: " ,alpha,",beta: ",beta)
                        if val==None:
                            MinMax.restore(backup, board)
                            return None,True
                        if player:
                            alpha = val if (val >alpha) else alpha
                        else:
                            beta = val if (val <beta) else beta

                        if alpha >= beta:
                            MinMax.restore(backup, board)
                            list.append(val)
                            return list, True
                        list.append(val)
                    MinMax.restore(backup, board)

        return list, False


    ####################
    #minmax with pruning
    def minimax_with_pruning(board, depth,alpha,beta,difficulty):
        # MinMax.counter +=1
        pane = [board.right_stack_panel, board.left_stack_panel]
        isLeaf = board.check_win() != 2
        if depth == MinMax.iterative_depth or isLeaf:
            if difficulty == 0: return MinMax.evaluate_easy(board,depth)
            if difficulty == 1: return MinMax.evaluate_medium(board,depth)
            if difficulty == 2: return MinMax.evaluate_hard(board,depth)
        list = []
        for i in range(3): # stack pane evaluation of current player
            current_list, to_be_pruned = MinMax.evaluate_possible_moves_pruning(pane[board.turn][i], board, board.turn, depth,alpha,beta,difficulty)
            if to_be_pruned ==True and depth != 0:
                return current_list               
            elif  to_be_pruned ==False: 
                list += current_list
            

        for i in range(4):
            for j in range(4): # board evaluation
                current_list, to_be_pruned = MinMax.evaluate_possible_moves_pruning(board.board[i][j], board, board.turn, depth,alpha,beta,difficulty)
                if to_be_pruned ==True and depth != 0:
                    return current_list               
                elif  to_be_pruned ==False: 
                    list += current_list
                


        if len(list) == 0: # Leaf node
            if difficulty == 0: return MinMax.evaluate_easy(board,depth)
            if difficulty == 1: return MinMax.evaluate_medium(board,depth)
            if difficulty == 2: return MinMax.evaluate_hard(board,depth)

        if depth == 0:
            # print(list)
            # print(list.index(max(list) if board.turn else min(list)))
            MinMax.rootlist=list
            max_index = max(range(len(MinMax.available_moves)), key=lambda i: MinMax.available_moves[i][2])
            min_index = min(range(len(MinMax.available_moves)), key=lambda i: MinMax.available_moves[i][2])
            # next_move = MinMax.available_moves[list.index(max(list) if board.turn else min(list))]
            next_move = MinMax.available_moves[max_index] if board.turn else MinMax.available_moves[min_index]
            # board.move(next_move[0], next_move[1])
        return max(list) if board.turn else min(list)


    def evaluate_possible_moves_pruning(tile, board, player, depth, alpha, beta,difficulty):
        list = []
        if len(tile.pieces_stack) != 0 and tile.pieces_stack[-1].color.value == player:
            for i in range(4):
                for j in range(4):
                    board.to_board = 1
                    if board.game_Rules(tile, board.board[i][j]):
                        board.board[i][j].push_piece(tile.pop_piece())
                        
                        # val = MinMax.evaluate_k(board)
                        board.turn = 1-player
                        val  =  MinMax.minimax_with_pruning(board, depth + 1,alpha,beta,difficulty)
                        if depth == 0:
                            MinMax.available_moves.append((tile, board.board[i][j],val))
                        # print("depth: ",depth,"player: ",player," ,val: ",val,",alpha: " ,alpha,",beta: ",beta)
                        if player:
                            alpha = val if (val >alpha) else alpha
                        else:
                            beta = val if (val <beta) else beta
                        
                        board.turn = player
                        tile.push_piece(board.board[i][j].pop_piece())
                        if alpha >= beta:
                            return val, True
                            # return list, True
                        # print("list: ",list)
                        # print("available_moves: ",MinMax.available_moves)
                        list.append(val)

        return list, False

