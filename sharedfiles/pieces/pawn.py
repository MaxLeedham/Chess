import typing

import pygame

from sharedfiles.piece import Piece

if typing.TYPE_CHECKING:
    from sharedfiles.board import Board


class Pawn(Piece):
    def __init__(self, pos, colour, board):
        super().__init__(pos, colour)

        # Set up the image and scale it to be the correct size
        img_path = "sharedfiles/imgs/" + colour[0] + "_pawn.png"
        self.img = pygame.image.load(img_path)

        scale_factor = 8 / 15
        self.img = pygame.transform.scale(
            self.img,
            (
                board.tile_width * scale_factor,
                board.tile_height * scale_factor,
            ),
        )

        # Pawn notation is a space
        self.notation = " "

        self.en_passant_possible = False

    def __repr__(self):
        """Return a string with the colour and position which is more useful than
        the random hex value given by default"""
        return f"{self.colour} pawn at {self.pos}"

    def get_possible_moves(self, board: "Board"):
        """Gets all the moves the pawn can make currently"""
        output = []
        moves: typing.List[typing.Tuple[int, int]] = []

        # move forward
        if self.colour == "white":
            # Can move 1 or 2 (only if it hasn't moved before) squares forward
            moves.append((0, -1))
            if not self.has_moved:
                moves.append((0, -2))

        elif self.colour == "black":
            # Can move 1 or 2 (only if it hasn't moved before) squares forward
            moves.append((0, 1))
            if not self.has_moved:
                moves.append((0, 2))

        for move in moves:
            new_pos = (self.x, self.y + move[1])
            if new_pos[1] < board.size and new_pos[1] >= 0:
                output.append(board.get_square_from_pos(new_pos))

        return output

    def get_moves(self, board):
        output = []

        for square in self.get_possible_moves(board):
            if square.occupying_piece is not None:
                break

            output.append(square)

        # Handle capturing 1 square diagonally forward
        if self.colour == "white":
            if self.x + 1 < 8 and self.y - 1 >= 0:
                square = board.get_square_from_pos((self.x + 1, self.y - 1))
                if (
                    square.occupying_piece is not None
                    and square.occupying_piece.colour != self.colour
                ):
                    output.append(square)

            if self.x - 1 >= 0 and self.y - 1 >= 0:
                square = board.get_square_from_pos((self.x - 1, self.y - 1))
                if (
                    square.occupying_piece is not None
                    and square.occupying_piece.colour != self.colour
                ):
                    output.append(square)

        elif self.colour == "black":
            if self.x + 1 < 8 and self.y + 1 < 8:
                square = board.get_square_from_pos((self.x + 1, self.y + 1))
                if (
                    square.occupying_piece is not None
                    and square.occupying_piece.colour != self.colour
                ):
                    output.append(square)

            if self.x - 1 >= 0 and self.y + 1 < 8:
                square = board.get_square_from_pos((self.x - 1, self.y + 1))
                if (
                    square.occupying_piece is not None
                    and square.occupying_piece.colour != self.colour
                ):
                    output.append(square)

        # Handle pieces being taken by en passant
        # A (very badly made) diagram showing how this works is in the base folder
        # It will also be explained in the README

        opposite_colour = "white" if self.colour == "black" else "black"
        for pawn in board.get_pawns(opposite_colour, self.y):
            if self.x in [pawn.x - 1, pawn.x + 1] and pawn.en_passant_possible:
                # print("Pawn can take via en passant")
                y = self.y + 1 if pawn.colour == "white" else self.y - 1

                square = board.get_square_from_pos((pawn.x, y))
                # print(square)
                output.append(square)

        return output

    def attacking_squares(self, board):
        """Returns a list of only the moves that can capture a piece"""
        moves = self.get_moves(board)
        # return the diagonal moves only
        return [i for i in moves if i.x != self.x]
