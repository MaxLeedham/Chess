import typing

import pygame

from sharedfiles.board import Board

pygame.init()

WINDOW_SIZE = (825, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess")

board = Board(WINDOW_SIZE[1], WINDOW_SIZE[1], 8)

state = "playing"
font = pygame.font.Font("freesansbold.ttf", 30)


def draw(display: pygame.surface.Surface):
    """Draw the board and update the screen"""
    display.fill((60, 60, 60))
    board.draw(display)

    add_text(f"{board.turn.title()}'s turn", (718, 50), display)
    add_text(
        f"Move {board.move_count}:",
        (718, 100),
        display,
    )
    add_text(
        "None" if board.last_move is None else board.last_move, (718, 150), display
    )

    pygame.display.update()


def add_text(text: str, cords: typing.Tuple[int, int], display) -> None:
    display_text = font.render(text, True, (255, 255, 255))
    text_rect = display_text.get_rect()
    text_rect.center = cords
    display.blit(display_text, text_rect)


if __name__ == "__main__":
    running = True

    if state == "playing":
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                # Quit the game if the user presses the close button
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # If the mouse is clicked
                    board.handle_click(mouse_x, mouse_y)

            if board.is_in_checkmate("black"):  # If black is in checkmate
                print("White wins!")
                running = False

            elif board.is_in_checkmate("white"):  # If white is in checkmate
                print("Black wins!")
                running = False

            if board.is_in_stalemate("black") or board.is_in_stalemate("white"):
                print("Draw by stalemate")
                # print("black" if board.is_in_stalemate("black") else "white")
                running = False

            # Draw the board
            draw(screen)
    else:
        pass
