from __future__ import annotations

import typing

import pygame

from sharedfiles.piece import Piece

if typing.TYPE_CHECKING:
    from sharedfiles.board import Board


class King(Piece):
    def __init__(self, pos, colour, board: Board):
        super().__init__(pos, colour)

        # Sets up the image, scales it and sets up the notation
        img_path = "sharedfiles/imgs/" + colour[0] + "_king.png"
        self.img = pygame.image.load(img_path)

        scale_factor = 11 / 15
        self.img = pygame.transform.scale(
            self.img,
            (board.tile_width * scale_factor, board.tile_height * scale_factor),
        )
        self.notation = "K"

    def get_possible_moves(self, board: Board):
        """Returns a list of the possible moves that the king
        can take on the current board"""

        output = []
        moves = [
            (0, -1),  # north
            (1, -1),  # north east
            (1, 0),  # east
            (1, 1),  # south east
            (0, 1),  # south
            (-1, 1),  # south west
            (-1, 0),  # west
            (-1, -1),  # north west
        ]

        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if (
                new_pos[0] < board.size
                and new_pos[0] >= 0
                and new_pos[1] < board.size
                and new_pos[1] >= 0
            ):
                output.append([board.get_square_from_pos(new_pos)])

        return output

    def can_castle(self, board: Board) -> typing.Optional[typing.List[str]]:
        castles = []

        if not self.has_moved:
            kingside_rook = board.get_piece_from_pos((board.size - 1, self.y))
            queenside_rook = board.get_piece_from_pos((0, self.y))

            if (
                queenside_rook is not None
                and not queenside_rook.has_moved
                and [board.get_piece_from_pos((i, self.y)) for i in range(1, self.x)]
                == [None for _ in range(1, self.x)]
            ):
                castles.append("queenside")

            if (
                kingside_rook is not None
                and not kingside_rook.has_moved
                and [
                    board.get_piece_from_pos((i, self.y))
                    for i in range(self.x + 1, board.size - 1)
                ]
                == [None for _ in range(self.x + 1, board.size - 1)]
            ):
                castles.append("kingside")

        return castles

    def get_valid_moves(self, board: Board):
        output = []

        for square in self.get_moves(board):
            # If moving doesn't put the king in check, allow it to move there
            if not board.is_in_check(self.colour, board_change=[self.pos, square.pos]):
                output.append(square)

        if "queenside" in self.can_castle(board):
            output.append(board.get_square_from_pos((self.x - 2, self.y)))

        if "kingside" in self.can_castle(board):
            output.append(board.get_square_from_pos((self.x + 2, self.y)))

        return output
