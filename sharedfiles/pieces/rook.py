import pygame

from sharedfiles.piece import Piece


class Rook(Piece):
    def __init__(self, pos, colour, board):
        super().__init__(pos, colour)

        # Sets up the image, scales it and sets the notation
        img_path = "sharedfiles/imgs/" + colour[0] + "_rook.png"
        self.img = pygame.image.load(img_path)

        scale_factor = 11 / 15
        self.img = pygame.transform.scale(
            self.img,
            (board.tile_width * scale_factor, board.tile_height * scale_factor),
        )
        self.notation = "R"

    def get_possible_moves(self, board):
        """Returns a list of all the possible moves the rook can make
        on the current board"""
        output = []

        moves_north = []
        for y in range(self.y)[::-1]:
            moves_north.append(board.get_square_from_pos((self.x, y)))
        output.append(moves_north)

        moves_east = []
        for x in range(self.x + 1, board.size):
            moves_east.append(board.get_square_from_pos((x, self.y)))
        output.append(moves_east)

        moves_south = []
        for y in range(self.y + 1, board.size):
            moves_south.append(board.get_square_from_pos((self.x, y)))
        output.append(moves_south)

        moves_west = []
        for x in range(self.x)[::-1]:
            moves_west.append(board.get_square_from_pos((x, self.y)))
        output.append(moves_west)

        return output
