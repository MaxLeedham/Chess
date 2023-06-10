import pygame

from sharedfiles.piece import Piece


class Queen(Piece):
    def __init__(self, pos, colour, board):
        super().__init__(pos, colour)

        # Sets up the image, scales it and sets up the notation
        img_path = "sharedfiles/imgs/" + colour[0] + "_queen.png"
        self.img = pygame.image.load(img_path)

        scale_factor = 11 / 15
        self.img = pygame.transform.scale(
            self.img,
            (board.tile_width * scale_factor, board.tile_height * scale_factor),
        )
        self.notation = "Q"

    def get_possible_moves(self, board):
        """Returns a list of the possible moves the queen can take
        on the current board"""
        output = []

        moves_north = []
        for y in range(self.y)[::-1]:
            moves_north.append(board.get_square_from_pos((self.x, y)))
        output.append(moves_north)

        moves_ne = []
        for i in range(1, board.size):
            if self.x + i > board.size - 1 or self.y - i < 0:
                break
            moves_ne.append(board.get_square_from_pos((self.x + i, self.y - i)))
        output.append(moves_ne)

        moves_east = []
        for x in range(self.x + 1, board.size):
            moves_east.append(board.get_square_from_pos((x, self.y)))
        output.append(moves_east)

        moves_se = []
        for i in range(1, board.size):
            if self.x + i > board.size - 1 or self.y + i > board.size - 1:
                break
            moves_se.append(board.get_square_from_pos((self.x + i, self.y + i)))
        output.append(moves_se)

        moves_south = []
        for y in range(self.y + 1, board.size):
            moves_south.append(board.get_square_from_pos((self.x, y)))
        output.append(moves_south)

        moves_sw = []
        for i in range(1, board.size):
            if self.x - i < 0 or self.y + i > board.size - 1:
                break
            moves_sw.append(board.get_square_from_pos((self.x - i, self.y + i)))
        output.append(moves_sw)

        moves_west = []
        for x in range(self.x)[::-1]:
            moves_west.append(board.get_square_from_pos((x, self.y)))
        output.append(moves_west)

        moves_nw = []
        for i in range(1, board.size):
            if self.x - i < 0 or self.y - i < 0:
                break
            moves_nw.append(board.get_square_from_pos((self.x - i, self.y - i)))
        output.append(moves_nw)

        return output
