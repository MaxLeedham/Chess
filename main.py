import random
import time
import typing

import pygame

from database import db
from menuItem import InputBox, MenuItem, add_text
from sharedfiles.board import Board
from users import User

time_limit = 600  # 10 minutes
board_size = 8

pygame.init()

WINDOW_SIZE = (825, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess")

state = "main menu"
players: typing.List[User] = []

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

    add_text(
        f"{white_user.username if board.turn == 'white' else black_user.username}'s turn",  # noqa: E501
        (718, 50),
        display,
    )
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


def validate_login(username: str, password: str) -> bool:
    data = db.select(
        "SELECT userID, username, rating FROM users WHERE username = ? and password = ?",  # noqa: E501
        (username, password),
    )

    # The same account can't be logged in twice
    if len(players) == 1:  # noqa: SIM102
        if len(data) == 1:
            if data[0][0] == players[0].user_id:
                return False

    if len(data) == 1:
        players.append(User(data[0][0], data[0][1], rating=data[0][2]))

    print(players)

    return len(data) == 1


results: typing.List = []  # "" for draw or winner, reason

if __name__ == "__main__":
    while True:
        if state == "playing":
            if len(players) < 2:
                players.append(User(None, None, None, True))

                if len(players) == 1:
                    players.append(User(None, None, None, True))

            if random.randint(0, 1) == 0:  # noqa: S311
                white_user = players[0]
                players[0].playing_as = "white"

                black_user = players[1]
                players[1].playing_as = "black"
            else:
                white_user = players[1]
                players[1].playing_as = "white"

                black_user = players[0]
                players[0].playing_as = "black"

            board = Board(WINDOW_SIZE[1], WINDOW_SIZE[1], board_size, time_limit)
            running = True
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

                resign_button = MenuItem(
                    (725, 300), 30, "Resign", (255, 255, 255), screen
                )
                pygame.display.update()

                mouse_x, mouse_y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    # Quit the game if the user presses the close button
                    if event.type == pygame.QUIT:
                        running = False
                        state = "main menu"

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # If the mouse is clicked
                        board.handle_click(mouse_x, mouse_y)

                        if resign_button.has_been_clicked(mouse_x, mouse_y):
                            results = [
                                "white" if board.turn == "black" else "black",
                                f"{white_user.username if board.turn == 'white' else black_user.username} resigned",  # noqa: E501
                            ]

                            running = False
                            state = "results"

                            print(
                                f"{white_user.username.title() if board.turn == 'black' else black_user.username.title()} wins by the other player resigning"  # noqa: E501
                            )

                if board.is_in_checkmate("black"):  # If black is in checkmate
                    print(f"{white_user.username.title()} wins!")
                    running = False
                    state = "results"

                    results = [
                        "white",
                        f"{white_user.username} put {black_user.username} in checkmate",
                    ]

                elif board.is_in_checkmate("white"):  # If white is in checkmate
                    print(f"{black_user.username.title()} wins!")
                    running = False
                    state = "results"

                    results = [
                        "black",
                        f"{black_user.username} put {white_user.username} in checkmate",
                    ]

                elif board.is_in_stalemate("black") or board.is_in_stalemate("white"):
                    print("Draw by stalemate")
                    # print("black" if board.is_in_stalemate("black") else "white")
                    running = False
                    state = "results"

                    results = [
                        "",
                        "Stalemate",
                    ]

                if board.white_time <= 0:
                    print(
                        f"{black_user.username.title()} wins on time with {format_time(board.black_time)} left"  # noqa: E501
                    )
                    running = False
                    state = "results"

                    results = [
                        "black",
                        f"{white_user.username} ran out of time",
                    ]

                elif board.black_time <= 0:
                    print(
                        f"{white_user.username.title()} wins on time with {format_time(board.white_time)} left"  # noqa: E501
                    )
                    running = False
                    state = "results"

                    results = [
                        "white",
                        f"{black_user.username} ran out of time",
                    ]

                # Draw the board
                draw(screen)

            print(f"moves: {board.moves}")
        elif state == "main menu":
            running = True
            while running:
                screen.fill((60, 60, 60))

                add_text("Chess", ((WINDOW_SIZE[0] + 1) / 2, 20), screen, 50)

                play_button = MenuItem(
                    ((WINDOW_SIZE[0] + 1) / 2, 100),
                    30,
                    "Play game",
                    (255, 255, 255),
                    screen,
                )

                settings_button = MenuItem(
                    ((WINDOW_SIZE[0] + 1) / 2, 175),
                    30,
                    "Settings",
                    (255, 255, 255),
                    screen,
                )

                register_button = MenuItem(
                    ((WINDOW_SIZE[0] + 1) / 2, 250),
                    30,
                    "Register",
                    (255, 255, 255),
                    screen,
                )

                login_button = MenuItem(
                    ((WINDOW_SIZE[0] + 1) / 2, 325),
                    30,
                    "Login",
                    (255, 255, 255) if len(players) != 2 else (150, 150, 150),
                    screen,
                )

                logout_button = MenuItem(
                    ((WINDOW_SIZE[0] + 1) / 2, 400),
                    30,
                    "Logout",
                    (255, 255, 255) if len(players) != 0 else (150, 150, 150),
                    screen,
                )

                leaderboard_button = MenuItem(
                    ((WINDOW_SIZE[0] + 1) / 2, 475),
                    30,
                    "Leaderboard",
                    (255, 255, 255),
                    screen,
                )

                exit_button = MenuItem(
                    ((WINDOW_SIZE[0] + 1) / 2, 550), 30, "Exit", (255, 255, 255), screen
                )

                pygame.display.update()

                mouse_x, mouse_y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    # Quit the game if the user presses the close button
                    if event.type == pygame.QUIT:
                        running = False
                        state = None

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # If the mouse is clicked
                        if play_button.has_been_clicked(mouse_x, mouse_y):
                            state = "playing"
                            running = False

                        if settings_button.has_been_clicked(mouse_x, mouse_y):
                            state = "settings"
                            running = False

                        if register_button.has_been_clicked(mouse_x, mouse_y):
                            state = "register"
                            running = False

                        if login_button.has_been_clicked(mouse_x, mouse_y):
                            state = "login"
                            running = False

                        if logout_button.has_been_clicked(mouse_x, mouse_y):
                            state = "logout"
                            running = False

                        if leaderboard_button.has_been_clicked(mouse_x, mouse_y):
                            state = "leaderboard"
                            running = False

                        if exit_button.has_been_clicked(mouse_x, mouse_y):
                            state = None
                            running = False

        elif state == "settings":
            running = True
            while running:
                screen.fill((60, 60, 60))

                add_text("Settings", ((WINDOW_SIZE[0] + 1) / 2, 20), screen, 40)

                back_button = MenuItem(
                    (15, 10),
                    15,
                    "Back",
                    (255, 255, 255),
                    screen,
                )

                add_text("Time controls:", (WINDOW_SIZE[0] * 0.15, 150), screen)

                time_1_min_button = MenuItem(
                    (WINDOW_SIZE[0] * 0.1, 195),
                    30,
                    "1 minute",
                    (255, 255, 255) if time_limit != 60 else (150, 150, 150),
                    screen,
                )

                time_5_mins = MenuItem(
                    (WINDOW_SIZE[0] * 0.3, 195),
                    30,
                    "5 minutes",
                    (255, 255, 255) if time_limit != 300 else (150, 150, 150),
                    screen,
                )

                time_10_mins_button = MenuItem(
                    (WINDOW_SIZE[0] * 0.5, 195),
                    30,
                    "10 minutes",
                    (255, 255, 255) if time_limit != 600 else (150, 150, 150),
                    screen,
                )

                time_30_mins_button = MenuItem(
                    (WINDOW_SIZE[0] * 0.7, 195),
                    30,
                    "30 minutes",
                    (255, 255, 255) if time_limit != 1800 else (150, 150, 150),
                    screen,
                )

                time_1_hour_button = MenuItem(
                    (WINDOW_SIZE[0] * 0.9, 195),
                    30,
                    "1 hour",
                    (255, 255, 255) if time_limit != 3600 else (150, 150, 150),
                    screen,
                )

                add_text("Board size:", (WINDOW_SIZE[0] * 0.15, 350), screen)

                board_8x8 = MenuItem(
                    (WINDOW_SIZE[0] * 0.15, 395),
                    30,
                    "8x8",
                    (255, 255, 255) if board_size != 8 else (150, 150, 150),
                    screen,
                )

                board_10x10 = MenuItem(
                    (WINDOW_SIZE[0] * 0.35, 395),
                    30,
                    "10x10",
                    (255, 255, 255) if board_size != 10 else (150, 150, 150),
                    screen,
                )

                pygame.display.update()

                mouse_x, mouse_y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    # Quit the game if the user presses the close button
                    if event.type == pygame.QUIT:
                        running = False
                        state = None

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # If the mouse is clicked
                        if back_button.has_been_clicked(mouse_x, mouse_y):
                            state = "main menu"
                            running = False
                        if time_1_min_button.has_been_clicked(mouse_x, mouse_y):
                            time_limit = 60
                        if time_5_mins.has_been_clicked(mouse_x, mouse_y):
                            time_limit = 300
                        if time_10_mins_button.has_been_clicked(mouse_x, mouse_y):
                            time_limit = 600
                        if time_30_mins_button.has_been_clicked(mouse_x, mouse_y):
                            time_limit = 1800
                        if time_1_hour_button.has_been_clicked(mouse_x, mouse_y):
                            time_limit = 3600

                        if board_8x8.has_been_clicked(mouse_x, mouse_y):
                            board_size = 8
                        if board_10x10.has_been_clicked(mouse_x, mouse_y):
                            board_size = 10

        elif state == "login":
            if len(players) < 2:
                running = True

                username_field = InputBox(WINDOW_SIZE[0] * 0.28, 150, 200, 50)
                password_field = InputBox(
                    WINDOW_SIZE[0] * 0.28, 250, 200, 50, hide_text=True
                )
                error_message = ""

                while running:
                    screen.fill((60, 60, 60))

                    add_text(
                        "Login to your account", ((WINDOW_SIZE[0] + 1) / 2, 20), screen
                    )

                    add_text("Username: ", (WINDOW_SIZE[0] * 0.15, 175), screen)
                    add_text("Password: ", (WINDOW_SIZE[0] * 0.15, 275), screen)

                    add_text(
                        error_message,
                        ((WINDOW_SIZE[0] + 1) / 2, 575),
                        screen,
                        15,
                        (255, 0, 0),
                    )

                    back_button = MenuItem(
                        (15, 10),
                        15,
                        "Back",
                        (255, 255, 255),
                        screen,
                    )

                    login_button = MenuItem(
                        ((WINDOW_SIZE[0] + 1) / 2, 525),
                        30,
                        "Login",
                        (255, 255, 255),
                        screen,
                    )

                    username_field.draw(screen)
                    password_field.draw(screen)

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        username_field.handle_event(event)
                        password_field.handle_event(event)

                        # Quit the game if the user presses the close button
                        if event.type == pygame.QUIT:
                            running = False
                            state = None

                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            # If the mouse is clicked
                            if back_button.has_been_clicked(mouse_x, mouse_y):
                                state = "main menu"
                                running = False
                            elif login_button.has_been_clicked(mouse_x, mouse_y):
                                if validate_login(
                                    username_field.text, password_field.text
                                ):
                                    error_message = ""
                                    state = "main menu"
                                    running = False
                                else:
                                    error_message = "Username or Password is incorrect or that user is already logged in"  # noqa: E501
                            else:
                                pass

                    pygame.display.update()
            else:
                state = "main menu"
        elif state == "logout":
            if len(players) == 0:
                state = "main menu"
            elif len(players) == 1:
                players = []
            elif len(players) == 2:
                running = True

                while running:
                    screen.fill((60, 60, 60))
                    add_text("Logout", ((WINDOW_SIZE[0] + 1) / 2, 50), screen)

                    back_button = MenuItem(
                        (15, 10),
                        15,
                        "Back",
                        (255, 255, 255),
                        screen,
                    )

                    player_0 = MenuItem(
                        ((WINDOW_SIZE[0] + 1) / 2, 150),
                        30,
                        players[0].username,
                        (255, 255, 255),
                        screen,
                    )

                    player_1 = MenuItem(
                        ((WINDOW_SIZE[0] + 1) / 2, 200),
                        30,
                        players[1].username,
                        (255, 255, 255),
                        screen,
                    )

                    for event in pygame.event.get():
                        # Quit the game if the user presses the close button
                        if event.type == pygame.QUIT:
                            running = False
                            state = None

                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if player_0.has_been_clicked(mouse_x, mouse_y):
                                players.pop(0)
                                state = "main menu"
                                running = False
                            elif player_1.has_been_clicked(mouse_x, mouse_y):
                                players.pop(1)
                                state = "main menu"
                                running = False

                            elif back_button.has_been_clicked(mouse_x, mouse_y):
                                state = "main menu"
                                running = False

                    pygame.display.update()
        elif state == "register":
            if len(players) < 2:
                running = True

                username_field = InputBox(WINDOW_SIZE[0] * 0.28, 150, 200, 50)
                password_field = InputBox(
                    WINDOW_SIZE[0] * 0.28, 250, 200, 50, hide_text=True
                )
                confirm_password_field = InputBox(
                    WINDOW_SIZE[0] * 0.4, 350, 200, 50, hide_text=True
                )

                error_message = ""

                while running:
                    screen.fill((60, 60, 60))

                    add_text(
                        "Register a new account", ((WINDOW_SIZE[0] + 1) / 2, 20), screen
                    )

                    add_text("Username: ", (WINDOW_SIZE[0] * 0.15, 175), screen)
                    add_text("Password: ", (WINDOW_SIZE[0] * 0.15, 275), screen)
                    add_text("Confirm Password: ", (WINDOW_SIZE[0] * 0.2, 375), screen)

                    add_text(
                        error_message,
                        ((WINDOW_SIZE[0] + 1) / 2, 575),
                        screen,
                        15,
                        (255, 0, 0),
                    )

                    back_button = MenuItem(
                        (15, 10),
                        15,
                        "Back",
                        (255, 255, 255),
                        screen,
                    )

                    register_button = MenuItem(
                        ((WINDOW_SIZE[0] + 1) / 2, 525),
                        30,
                        "Register",
                        (255, 255, 255),
                        screen,
                    )

                    username_field.draw(screen)
                    password_field.draw(screen)
                    confirm_password_field.draw(screen)

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        username_field.handle_event(event)
                        password_field.handle_event(event)
                        confirm_password_field.handle_event(event)

                        # Quit the game if the user presses the close button
                        if event.type == pygame.QUIT:
                            running = False
                            state = None

                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            # If the mouse is clicked
                            if back_button.has_been_clicked(mouse_x, mouse_y):
                                state = "main menu"
                                running = False
                            elif register_button.has_been_clicked(mouse_x, mouse_y):
                                # Check the username and password
                                if (
                                    len(username_field.text) == 0
                                    or len(password_field.text) == 0
                                ):
                                    error_message = (
                                        "Please enter both a username and password"
                                    )
                                elif len(username_field.text) <= 2:
                                    error_message = "Username too short"
                                elif len(username_field.text) >= 16:
                                    error_message = "Username is too long"
                                elif len(password_field.text) >= 20:
                                    error_message = "Password is too long"
                                elif (
                                    password_field.text == password_field.text.upper()
                                    or password_field.text
                                    == password_field.text.lower()
                                ):
                                    error_message = "Password must contain both uppercase and lowercase"  # noqa: E501
                                else:
                                    numbers = False
                                    symbols = False

                                    for char in password_field.text:
                                        if char in [str(i) for i in range(10)]:
                                            numbers = True

                                        if char in list(
                                            "!\"#$%&'()*+,-./<;=:>?@[\]^_`{|}~"
                                        ):
                                            symbols = True

                                    if not symbols or not numbers:
                                        error_message = "Passwords must contain at least one number and at least one symbol"  # noqa: E501
                                    elif (
                                        password_field.text
                                        != confirm_password_field.text
                                    ):
                                        error_message = "Passwords must match"
                                    else:
                                        # It meets every criteria
                                        # Check if its already in the database
                                        # if not, add it and log them in
                                        data = db.select(
                                            "SELECT * FROM users WHERE username = ?",
                                            (username_field.text,),
                                        )

                                        if len(data) == 1:
                                            error_message = "Duplicate username"
                                        else:
                                            db.execute(
                                                "INSERT INTO users(username, password) VALUES (?, ?)",  # noqa: E501
                                                (
                                                    username_field.text,
                                                    password_field.text,
                                                ),
                                            )

                                            data = db.select(
                                                "SELECT userID, username FROM users WHERE username = ?",  # noqa: E501
                                                (username_field.text,),
                                            )

                                            players.append(
                                                User(data[0][0], data[0][1], None)
                                            )

                                            state = "main menu"
                                            running = False

                            else:
                                pass

                    pygame.display.update()
            else:
                state = "main menu"
        elif state == "results":
            if results[0] == "":
                if not white_user.guest:
                    db.execute(
                        "UPDATE users SET games_played = games_played + 1, draws = draws + 1 WHERE userID = ?",  # noqa: E501
                        (white_user.user_id,),
                    )
                if not black_user.guest:
                    db.execute(
                        "UPDATE users SET games_played = games_played + 1, draws = draws + 1 WHERE userID = ?",  # noqa: E501
                        (black_user.user_id,),
                    )
            elif results[0] == "white":
                if not white_user.guest:
                    db.execute(
                        "UPDATE users SET games_played = games_played + 1, wins = wins + 1 WHERE userID = ?",  # noqa: E501
                        (white_user.user_id,),
                    )
                if not black_user.guest:
                    db.execute(
                        "UPDATE users SET games_played = games_played + 1 WHERE userID = ?",  # noqa: E501
                        (black_user.user_id,),
                    )
            else:
                if not black_user.guest:
                    db.execute(
                        "UPDATE users SET games_played = games_played + 1, wins = wins + 1 WHERE userID = ?",  # noqa: E501
                        (black_user.user_id,),
                    )
                if not white_user.guest:
                    db.execute(
                        "UPDATE users SET games_played = games_played + 1 WHERE userID = ?",  # noqa: E501
                        (white_user.user_id,),
                    )

                if not white_user.guest and not black_user.guest:
                    # Update their ratings

                    if white_user.rating == black_user.rating:
                        difference = 50
                        print("Ratings are the same")
                    else:
                        difference = abs(white_user.rating - black_user.rating) * 0.2

                    if results[0] == "white":
                        db.execute(
                            "UPDATE users SET rating = rating + ? WHERE userID = ?",
                            (difference, white_user.user_id),
                        )
                        white_user.rating += difference

                        db.execute(
                            "UPDATE users SET rating = rating - ? WHERE userID = ?",
                            (difference, black_user.user_id),
                        )
                        black_user.rating -= difference
                    else:
                        db.execute(
                            "UPDATE users SET rating = rating + ? WHERE userID = ?",
                            (difference, black_user.user_id),
                        )
                        black_user.rating += difference

                        db.execute(
                            "UPDATE users SET rating = rating - ? WHERE userID = ?",
                            (difference, white_user.user_id),
                        )
                        white_user.rating -= difference

            db.execute(
                "INSERT INTO games(whitePlayerID, blackPlayerID, result, resultReason) VALUES (?, ?, ?, ?)",  # noqa: E501
                (
                    white_user.user_id,
                    black_user.user_id,
                    1 if results[0] == "white" else 2,
                    results[1],
                ),
            )

            screen.fill((60, 60, 60))

            add_text("Game ended!", ((WINDOW_SIZE[0] + 1) / 2, 50), screen, 50)

            add_text(
                "Draw"
                if results[0] == ""
                else f"{white_user.username.title()} wins"
                if results[0] == "white"
                else f"{black_user.username.title()} wins",
                ((WINDOW_SIZE[0] + 1) / 2, 250),
                screen,
            )

            add_text(results[1], ((WINDOW_SIZE[0] + 1) / 2, 350), screen)

            pygame.display.update()

            running = True

            while running:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        state = "main menu"
                        running = False

        elif state == "leaderboard":
            data = db.select(
                "SELECT username, rating, wins, draws, games_played FROM users ORDER BY rating DESC, wins DESC, draws DESC LIMIT 5"  # noqa: E501
            )
            running = True
            while running:
                screen.fill((60, 60, 60))

                add_text("Leaderboard", ((WINDOW_SIZE[0] + 1) / 2, 20), screen, 40)

                back_button = MenuItem(
                    (15, 10),
                    15,
                    "Back",
                    (255, 255, 255),
                    screen,
                )

                add_text(
                    "User, username, rating, wins, draws, loses",
                    ((WINDOW_SIZE[0] + 1) / 2, 100),
                    screen,
                )

                for i, user in enumerate(data):
                    add_text(
                        f"{user[0]}, {user[1]}, {user[2]}, {user[3]}, {user[4] - user[2] - user[3]}",  # noqa: E501
                        ((WINDOW_SIZE[0] + 1) / 2, 175 + (i * 50)),
                        screen,
                    )

                pygame.display.update()

                mouse_x, mouse_y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    # Quit the game if the user presses the close button
                    if event.type == pygame.QUIT:
                        running = False
                        state = None

                    elif (  # noqa: SIM102
                        event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                    ):
                        # If the mouse is clicked
                        if back_button.has_been_clicked(mouse_x, mouse_y):
                            state = "main menu"
                            running = False

        else:
            break
