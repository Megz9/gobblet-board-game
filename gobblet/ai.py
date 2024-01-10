import pygame
class MinMax:
    def allowed_move(self):
        pass

    
        

        # Consider the size of the pieces on the board
        player_piece_size = board.get_largest_piece_size(player)
        opponent_piece_size = board.get_largest_piece_size(3 - player)

        # Assign weights to factors based on importance
        player_lines_weight = 1.0
        opponent_lines_weight = -1.0  # Discourage the opponent from winning
        player_piece_size_weight = 0.5
        opponent_piece_size_weight = -0.5  # Discourage the opponent from having large pieces

        # Combine values into an overall evaluation score
        evaluation_score = (
            player_lines * player_lines_weight +
            opponent_lines * opponent_lines_weight +
            player_piece_size * player_piece_size_weight +
            opponent_piece_size * opponent_piece_size_weight
        )

        return evaluation_score
