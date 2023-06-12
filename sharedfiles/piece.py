from __future__ import annotations

import copy
import typing

if typing.TYPE_CHECKING:
    from sharedfiles.board import Board
    from sharedfiles.square import Square


class Piece:
    def __init__(self, pos: typing.Tuple[int, int], colour: str):
        self.pos: typing.Tuple(int, int) = pos
        self.x: int = pos[0]
        self.y: int = pos[1]
        self.colour: str = colour
        self.has_moved: bool = False

    def __str__(self) -> str:
        return f"{self.notation} at position {self.pos}"

    def get_moves(self, board: Board) -> typing.List[Square]:
        output = []
        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.colour == self.colour:
                        break

                    output.append(square)
                    break

                output.append(square)
        return output

    def get_valid_moves(self, board: Board) -> typing.List[Square]:
        output = []
        for square in self.get_moves(board):
            # Checks moving the piece would not put yourself in check
            # making it an illegal move
            if not board.is_in_check(self.colour, board_change=[self.pos, square.pos]):
                output.append(square)
        return output

    def move(
        self,
        board: Board,
        square: Square,
        force: bool = False,
        skip_generation: bool = False,
    ) -> bool:
        """Moves a piece on the board. If force=True it will move even if it wouldn't
        normally be possible, for example when castling the king and rook need to go
        past each other
        """
        # un-highlight all the squares
        for i in board.squares:
            i.highlight = False

        if square in self.get_valid_moves(board) or force:
            prev_square = board.get_square_from_pos(self.pos)
            square_copy = copy.copy(square)

            board.move_count += 1
            board.moves.append(
                (self.generate_move_notation(board, prev_square, square) or "some move")
            ) if not skip_generation else ""
            print(board.moves[-1] if board.moves[-1] != "some move" else "")

            self.pos, self.x, self.y = square.pos, square.x, square.y

            # Set the square we were on before to having nothing
            # and the new one as having this piece
            prev_square.occupying_piece = None
            square.occupying_piece = self

            # Unselect the piece and mark the piece as having moved
            # important for things like castling and en-pasant
            board.selected_piece = None
            self.has_moved = True

            # Pawn promotion or en passant
            if self.notation == " ":
                if self.y == 0 or self.y == (board.size - 1):
                    # Promotes immediately to a queen
                    # as its easier than letting the user choose
                    from sharedfiles.pieces.queen import Queen

                    square.occupying_piece = Queen((self.x, self.y), self.colour, board)

                # If it has moved 2 forward, mark en pasant possible as True
                if abs(prev_square.y - square.y) == 2:
                    self.en_passant_possible = True

                # If it has taken a piece
                # If it was from en pasant, we need to remove the old piece
                # We can tell if it was by en pasant if there was no piece in the square
                # before we moved

                if (
                    abs(prev_square.x - square.x) == 1
                    and square_copy.occupying_piece is None
                ):
                    # print("Taken via en passant")
                    # It was from en pasant
                    board.get_square_from_pos(
                        (self.x, prev_square.y)
                    ).occupying_piece = None

            # Move rook if king castles
            if self.notation == "K":
                # If it has moved 2 squares
                if prev_square.x - self.x == 2:
                    # Move the rook
                    rook = board.get_piece_from_pos((0, self.y))
                    rook.move(
                        board,
                        board.get_square_from_pos((self.x + 1, self.y)),
                        force=True,
                        skip_generation=True,
                    )

                elif prev_square.x - self.x == -2:
                    rook = board.get_piece_from_pos((board.size - 1, self.y))
                    rook.move(
                        board,
                        board.get_square_from_pos((self.x - 1, self.y)),
                        force=True,
                        skip_generation=True,
                    )

            return True

        # The piece can't move there
        board.selected_piece = None
        return False

    # True for all pieces except pawn
    def attacking_squares(self, board: Board):
        return self.get_moves(board)

    def get_possible_moves(
        self, board: Board
    ) -> typing.Union[typing.List[Square], typing.List[typing.List[Square]]]:
        raise NotImplementedError(
            "Call this method on one of the piece sub-classes not on this base class"
        )

    def generate_move_notation(
        self, board: Board, prev_square: Square, new_square: Square
    ) -> str:
        """Generates the notation for a move on the board"""
        # The first thing to check for is the king castling

        move_notation: str = ""
        columns: str = "abcdefghijklmnop"

        if self.notation == " ":
            if prev_square.x != new_square.x:
                move_notation += (
                    f"{columns[prev_square.x]}x{new_square.get_coord(board)}"
                )
            else:
                move_notation += new_square.get_coord(board)
        elif (
            prev_square.occupying_piece.notation == "K"
            and abs(prev_square.x - new_square.x) == 2
        ):
            # It was a castle
            if prev_square.x - new_square.x == 2:
                move_notation += "O-O-O"
            else:
                move_notation += "O-O"
        else:
            move_notation += (
                f"{prev_square.occupying_piece.notation}{new_square.get_coord(board)}"
            )

        return move_notation
