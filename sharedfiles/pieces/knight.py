import pygame

from sharedfiles.piece import Piece


class Knight(Piece):
    def __init__(self, pos, colour, board):
        super().__init__(pos, colour)

        # Sets up the image, scales it and sets the notation
        img_path = "sharedfiles/imgs/" + colour[0] + "_knight.png"
        self.img = pygame.image.load(img_path)

        scale_factor = 11 / 15
        self.img = pygame.transform.scale(
            self.img,
            (board.tile_width * (scale_factor), board.tile_height * (scale_factor)),
        )
        self.notation = "N"

    def get_possible_moves(self, board):
        """Returns the moves the knight can make
        based on the current state of the board"""
        output = []

        # All of the possible moves the knight can take
        moves = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]

        for move in moves:
            # Makes sure that moving it would keep it on the board
            new_pos = (self.x + move[0], self.y + move[1])
            if (
                new_pos[0] < board.size
                and new_pos[0] >= 0
                and new_pos[1] < board.size
                and new_pos[1] >= 0
            ):
                output.append([board.get_square_from_pos(new_pos)])

        return output
