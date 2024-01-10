

class Tile:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.pieces_stack = []

    def push_piece(self, piece):
        self.pieces_stack.append(piece)

    def pop_piece(self):
        return self.pieces_stack.pop()
