import time
import typing

import pygame

from sharedfiles.board import Board

time_limit = 600  # 10 minutes
board_size = 8

pygame.init()

WINDOW_SIZE = (825, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess")

board = Board(WINDOW_SIZE[1], WINDOW_SIZE[1], board_size, time_limit)

state = "playing"
font = pygame.font.Font("freesansbold.ttf", 30)

start_time = time.time()
elapsed_time = time.time() - start_time


def format_time(seconds: float):
    minutes = int(seconds // 60)
    secs = seconds % 60

    return f"{minutes}:{round(secs, 1)}"


def draw(display: pygame.surface.Surface):
    """Draw the board and update the screen"""
    display.fill((60, 60, 60))
    board.draw(display)

    add_text(f"{board.turn.title()}'s turn", (718, 50), display)
    add_text(
        f"Move {len(board.moves)}:",
        (718, 100),
        display,
    )
    add_text("None" if len(board.moves) == 0 else board.moves[-1], (718, 150), display)

    add_text("Blacks Time:", (712.5, 350), display)
    add_text(format_time(board.black_time), (712.5, 395), display)

    add_text("Whites Time:", (712.5, 450), display)
    add_text(format_time(board.white_time), (712.5, 495), display)

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
            elapsed_time = (
                time.time() - start_time
            )  # number of seconds since the program started
            time_left = time_limit - elapsed_time

            if board.turn == "white":
                board.white_elapsed_time = time.time() - board.time_at_turn
                board.white_time = time_limit - (
                    board.white_time_elapsed + board.white_elapsed_time
                )
            else:
                board.black_elapsed_time = time.time() - board.time_at_turn
                board.black_time = time_limit - (
                    board.black_time_elapsed + board.black_elapsed_time
                )

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
                break

            elif board.is_in_checkmate("white"):  # If white is in checkmate
                print("Black wins!")
                running = False
                break

            if board.is_in_stalemate("black") or board.is_in_stalemate("white"):
                print("Draw by stalemate")
                # print("black" if board.is_in_stalemate("black") else "white")
                running = False
                break

            if board.white_time <= 0:
                print(f"Black wins on time with {format_time(board.black_time)} left")
                running = False
                break

            elif board.black_time <= 0:
                print(f"White wins on time with {format_time(board.white_time)} left")
                running = False
                break

            # Draw the board
            draw(screen)
        print(f"moves: {board.moves}")
    else:
        pass
