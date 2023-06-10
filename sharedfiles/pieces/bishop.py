import pygame

from sharedfiles.piece import Piece


class Bishop(Piece):
    def __init__(self, pos, colour, board):
        super().__init__(pos, colour)

        # Sets up the image, scales it and sets the notation
        img_path = "sharedfiles/imgs/" + colour[0] + "_bishop.png"
        self.img = pygame.image.load(img_path)

        scale_factor = 11 / 15
        self.img = pygame.transform.scale(
            self.img,
            (board.tile_width * scale_factor, board.tile_height * scale_factor),
        )
        self.notation = "B"

    def get_possible_moves(self, board):
        """Returns a list of the only moves the bishop can make
        based on the state of the board"""
        output = []

        # north east moves
        moves_ne = []
        for i in range(1, board.size):
            if self.x + i > board.size - 1 or self.y - i < 0:
                break

            moves_ne.append(board.get_square_from_pos((self.x + i, self.y - i)))

        output.append(moves_ne)

        # South east moves
        moves_se = []
        for i in range(1, board.size):
            if self.x + i > board.size - 1 or self.y + i > board.size - 1:
                break
            moves_se.append(board.get_square_from_pos((self.x + i, self.y + i)))
        output.append(moves_se)

        # South west moves
        moves_sw = []
        for i in range(1, board.size):
            if self.x - i < 0 or self.y + i > board.size - 1:
                break
            moves_sw.append(board.get_square_from_pos((self.x - i, self.y + i)))
        output.append(moves_sw)

        # Noth west moves
        moves_nw = []
        for i in range(1, board.size):
            if self.x - i < 0 or self.y - i < 0:
                break
            moves_nw.append(board.get_square_from_pos((self.x - i, self.y - i)))
        output.append(moves_nw)

        return output
