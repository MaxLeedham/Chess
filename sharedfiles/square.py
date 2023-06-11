from __future__ import annotations

import typing

import pygame

if typing.TYPE_CHECKING:
    from sharedfiles import board, piece


class Square:
    def __init__(self, x: int, y: int, width: int, height: int, board: board.Board):
        # Make attributes for the arguments passed into init
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Find the actual x and y positions of the square
        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)

        # Find the colours of different things
        # light or dark square, the colour of the square
        # and the colour of the square when highlighted
        self.color = "light" if (x + y) % 2 == 0 else "dark"
        self.draw_color = (220, 208, 194) if self.color == "light" else (53, 53, 53)
        self.highlight_color = (100, 249, 83) if self.color == "light" else (0, 228, 10)

        # Holds the occupying piece, if there is any, otherwise None
        self.occupying_piece: piece.Piece = None
        self.coord = self.get_coord(board)
        self.highlight = False
        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height)

    def __repr__(self):
        return f"Square at x: {self.x}, y: {self.y}"

    def get_coord(self, board: board.Board):
        """Get the formal notation of the tile"""
        columns = "abcdefghijklmnop"
        return columns[self.x] + str(board.size - (self.y))

    def draw(self, display: pygame.Surface):
        """Draws this individual tile onto the screen"""
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)

        # adds the chess piece icons
        if self.occupying_piece is not None:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)
