from __future__ import annotations

import time
import typing

from sharedfiles.pieces.bishop import Bishop
from sharedfiles.pieces.king import King
from sharedfiles.pieces.knight import Knight
from sharedfiles.pieces.kueen import Kueen
from sharedfiles.pieces.pawn import Pawn
from sharedfiles.pieces.queen import Queen
from sharedfiles.pieces.rook import Rook
from sharedfiles.square import Square

if typing.TYPE_CHECKING:
    from sharedfiles.piece import Piece


# Game state checker
class Board:
    def __init__(self, width, height, size=8, time_limit=600, increment=0):
        # Sets up the width and height of the board as well as the individual squares
        self.width = width
        self.height = height
        self.tile_width = width // size
        self.tile_height = height // size

        if size >= 8:
            self.size = size
        else:
            raise ValueError("The board must be a minimum of 8x8")

        # What piece is selected (if any)
        self.selected_piece: Piece = None

        # Which colours turn it is
        self.turn = "white"

        self.time_at_turn = time.time()
        self.white_time = time_limit
        self.black_time = time_limit
        self.white_elapsed_time = 0
        self.black_elapsed_time = 0
        self.white_time_elapsed = 0  # Cumulative elapsed time for white player
        self.black_time_elapsed = 0  # Cumulative elapsed time for black player
        self.increment = increment

        self.moves = []
        self.move_count = 0

        # What the board currently looks like
        # By default configured how a chess game starts

        self.config = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            # ["bR", "", "", "", "bK", "", "", "bR"],
            # ["", "", "", "", "bP", "", "", ""],
            # ["", "", "", "", "", "", "", ""],
            # ["", "", "", "", "", "", "", ""],
            # ["", "", "", "", "", "", "", ""],
            # ["", "", "", "", "", "", "", ""],
            # ["", "", "", "", "wP", "", "", ""],
            # ["wR", "", "", "", "wK", "", "", "wR"],
        ]

        if self.size == 10:
            self.config = [
                ["bR", "bN", "bB", "bW", "bQ", "bK", "bW", "bB", "bN", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["", "", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", "", ""],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wN", "wB", "wW", "wQ", "wK", "wW", "wB", "wN", "wR"],
                # ["bR", "", "", "", "", "bK", "", "", "", "bR"],
                # ["", "", "", "", "", "", "", "", "", ""],
                # ["", "", "", "", "", "", "", "", "", ""],
                # ["", "", "", "", "", "", "", "", "", ""],
                # ["", "", "", "", "", "", "", "", "", ""],
                # ["", "", "", "", "", "", "", "", "", ""],
                # ["", "", "", "", "", "", "", "", "", ""],
                # ["", "", "", "", "", "", "", "", "", ""],
                # ["", "", "", "", "", "", "", "", "", ""],
                # ["wR", "", "", "", "", "wK", "", "", "", "wR"],
            ]

        # Generates the squares and sets up the board
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self) -> typing.List[Square]:
        """Generates and returns the list of squares making up the board"""
        output = []
        for y in range(self.size):
            for x in range(self.size):
                output.append(Square(x, y, self.tile_width, self.tile_height, self))
        return output

    def get_square_from_pos(self, pos) -> typing.Optional[Square]:
        """Returns the square for the given position"""
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

        return None

    def get_piece_from_pos(self, pos: typing.Tuple(int, int)) -> Piece:
        """Returns the piece (if any) on a given square"""
        return self.get_square_from_pos(pos).occupying_piece

    def setup_board(self):
        """Puts the correct pieces in the squares from the self.config"""

        notations = {
            "R": Rook,
            "N": Knight,
            "B": Bishop,
            "Q": Queen,
            "K": King,
            "P": Pawn,
            "W": Kueen,
        }

        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != "":
                    square = self.get_square_from_pos((x, y))

                    if piece[1] in notations:
                        square.occupying_piece = notations[piece[1]](
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )

    def handle_click(self, mouse_x, mouse_y):
        """Code to handle when the user clicks on the board"""

        # Find the square they clicked on
        x = mouse_x // self.tile_width
        y = mouse_y // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))

        if clicked_square:
            # If you click on a piece on your turn, select it
            if self.selected_piece is None:
                if (
                    clicked_square.occupying_piece is not None
                    and clicked_square.occupying_piece.colour == self.turn
                ):
                    self.selected_piece = clicked_square.occupying_piece

            # If you have clicked on a square the selected piece can move to
            # change who's turn it is
            elif self.selected_piece.move(self, clicked_square):
                self.turn = "white" if self.turn == "black" else "black"

                if self.turn == "white":
                    self.white_time_elapsed += self.white_elapsed_time
                else:
                    self.black_time_elapsed += self.black_elapsed_time

                self.time_at_turn = time.time()

                for pawn in self.get_pawns(self.turn):
                    pawn.en_passant_possible = False

            # If you already have a piece selected but click on another of your pieces
            # select the new piece
            elif (
                clicked_square.occupying_piece is not None
                and clicked_square.occupying_piece.colour == self.turn
            ):
                self.selected_piece = clicked_square.occupying_piece

    def is_in_check(
        self,
        colour: str,
        board_change: typing.List[
            typing.Tuple[int, int], typing.Tuple[int, int]
        ] = None,
        tmp: bool = False,
    ):  # board_change = [(x1, y1), (x2, y2)]
        """Checks is a certain colour is in check or not"""

        # Makes some variables that will be used while checking
        output = False
        king_pos = None
        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None

        if board_change is not None:
            print("board_change is not None") if tmp else ""
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None

                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece

        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]

        if changing_piece is not None and changing_piece.notation == "K":
            king_pos = new_square.pos

        if king_pos is None:
            for piece in pieces:
                if piece.notation == "K" and piece.colour == colour:
                    king_pos = piece.pos

        for piece in pieces:
            if piece.colour != colour:
                # If a piece can attack the square the king is on
                print(
                    f"{piece.notation}: {[square.pos for square in piece.attacking_squares(self)]}"  # noqa: E501
                ) if tmp else ""
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True

        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece

        return output

    def is_in_checkmate(self, colour):
        """Checks if a colours king is in checkmate"""

        # Find the colours king
        for piece in [i.occupying_piece for i in self.squares]:
            if piece is not None and piece.notation == "K" and piece.colour == colour:
                king = piece

        # If the king can't move anywhere and is in check, it is in checkmate
        if king.get_valid_moves(self) == [] and self.is_in_check(colour):
            for piece in [i.occupying_piece for i in self.squares]:
                if (
                    piece is not None
                    and piece.colour == colour
                    and len(piece.get_valid_moves(self)) != 0
                ):
                    # It can move, can't be checkmate
                    return False

            return True

        return False

    def is_in_stalemate(self, colour):
        """Detects if a colour is in stalemate
        It does this by looping over every piece of that colour
        and returns False is it can move
        """
        for piece in [square.occupying_piece for square in self.squares]:
            if (
                piece is not None
                and piece.colour == colour
                and piece.get_valid_moves(self) != []
            ):
                return False

        return True

    def draw(self, display):
        """Draws the board to the screen"""

        # Highlight the selected pieces square and any squares it can move to
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                if square:
                    square.highlight = True

        # Draw all the squares on the screen
        for square in self.squares:
            square.draw(display)

    def get_pawns(
        self, colour: typing.Optional[str] = None, y: typing.Optional[int] = None
    ) -> typing.List[Pawn]:
        """Returns a list of the pawns still on the board
        If you supply a colour (not color, color is not a word) it will return the pawns
        that are only that colour
        If you supply a y value, it will only return the pawns that are on that y level
        """
        pawns = []

        for square in self.squares:
            piece = square.occupying_piece

            if (
                type(piece) == Pawn
                and (colour == piece.colour or colour is None)
                and (y == square.y or y is None)
            ):
                pawns.append(piece)

        return pawns

    def get_piece(
        self,
        notation: typing.Optional[str] = None,
        pos: typing.Optional[typing.Tuple[int, int]] = None,
        colour: typing.Optional[str] = None,
    ) -> typing.List[Piece]:
        """Gets any piece on the board that matches the criteria

        Any of the arguments that are not set will be skipped when finding the pieces

        It searches from the top left square going right across the row
        and then at the end of the row, starts searching the next row down"""

        if [notation, pos, colour] == [None, None, None]:
            raise ValueError("No criteria for searching for pieces found")

        pieces = [
            square.occupying_piece
            for square in self.squares
            if square.occupying_piece is not None
        ]

        criteria_met_pieces = []

        for piece in pieces:
            # Skip pieces that don't meet the criteria
            notation_critera = (
                (piece.notation == notation) if notation is not None else True
            )
            pos_critera = (piece.pos == pos) if pos is not None else True
            colour_critera = (piece.colour == colour) if colour is not None else True

            if notation_critera and pos_critera and colour_critera:
                criteria_met_pieces.append(piece)

        return criteria_met_pieces

    def get_all_move_notations(self) -> typing.List[str]:
        pieces = [
            square.occupying_piece
            for square in self.squares
            if square.occupying_piece is not None
            and square.occupying_piece.colour == self.turn
        ]

        moves: typing.List[str] = []

        for piece in pieces:
            for move in piece.get_valid_moves(self):
                square = self.get_square_from_pos((piece.x, piece.y))
                notation = piece.generate_move_notation(self, square, move)
                moves.append(notation)

        return moves
