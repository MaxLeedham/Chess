import typing

import pygame


def add_text(
    text: str,
    cords: typing.Tuple[int, int],
    display,
    size=30,
    colour: typing.Tuple[int, int, int] = (255, 255, 255),
    font_name: str = "freesansbold.ttf",
) -> pygame.Rect:
    font = pygame.font.Font(font_name, size)
    display_text = font.render(text, True, colour)
    text_rect = display_text.get_rect()
    text_rect.center = cords
    display.blit(display_text, text_rect)
    return text_rect


class MenuItem:
    def __init__(
        self,
        center: typing.Tuple[int, int],
        size: int,
        text: str,
        colour: typing.Tuple[int, int, int],
        display,
    ) -> None:
        self.center = center
        self.size = size
        self.text = text
        self.colour = colour
        self.display = display

        self.rect = add_text(text, center, display, size, colour)

    def has_been_clicked(self, mousex: int, mousey: int) -> bool:
        return self.rect.collidepoint(mousex, mousey)


class InputBox:
    COLOUR_INACTIVE = pygame.Color(155, 155, 155)
    COLOUR_ACTIVE = pygame.Color(255, 255, 255)

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        text_size: int = 30,
        text: str = "",
        hide_text: bool = False,
    ):
        self.font = pygame.font.Font("freesansbold.ttf", text_size)
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = self.COLOUR_INACTIVE
        self.text = text
        self.txt_surface = self.font.render(text, True, self.colour)
        self.active = False
        self.hide_text = hide_text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.colour = self.COLOUR_ACTIVE if self.active else self.COLOUR_INACTIVE

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.colour = self.COLOUR_INACTIVE
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
                self.update()

            # Re-render the text
            self.txt_surface = self.font.render(
                self.text if not self.hide_text else "*" * len(self.text),
                True,
                self.colour,
            )

    def update(self):
        # Resize the box if the text is too long
        width = max(200, self.txt_surface.get_width() + 25)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Draw the rect
        pygame.draw.rect(screen, self.colour, self.rect, 2)
