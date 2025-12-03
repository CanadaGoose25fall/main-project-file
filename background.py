"""Background drawing functions."""

import random
import pygame
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    GRAY,
    SKY_BLUE,
    SNOW_WHITE,
    MOUNTAIN_GRAY,
)


def draw_scrolling_background(
    screen: pygame.Surface,
    background_offset: float,
    snowflakes: list,
    scroll_speed: float
) -> None:
    """
    Draw a scrolling snow slope with lane markers, mountains, and falling snow.
    Parameters
        screen: pygame.Surface
            The game screen surface to draw on.
        background_offset: float
            Current scroll position for animating lane markers.
        snowflakes: list
            List of snowflake positions to animate.
        scroll_speed: float
            The speed at which elements scroll down.
    Return： none
    """
    screen.fill(SKY_BLUE)
    snow_top = SCREEN_HEIGHT // 4

    # Distant mountains
    pygame.draw.polygon(
        screen,
        MOUNTAIN_GRAY,
        [
            (0, snow_top + 40),
            (SCREEN_WIDTH // 4, 20),
            (SCREEN_WIDTH // 2, snow_top + 40),
        ],
    )
    pygame.draw.polygon(
        screen,
        MOUNTAIN_GRAY,
        [
            (SCREEN_WIDTH // 2, snow_top + 60),
            (3 * SCREEN_WIDTH // 4, 30),
            (SCREEN_WIDTH, snow_top + 60),
        ],
    )

    # Snow field
    pygame.draw.rect(
        screen,
        SNOW_WHITE,
        (0, snow_top, SCREEN_WIDTH, SCREEN_HEIGHT - snow_top),
    )

    # Slope lane markers
    offset = int(background_offset) % 40
    for y in range(-40, SCREEN_HEIGHT, 40):
        line_y = snow_top + y + offset
        if line_y < snow_top or line_y > SCREEN_HEIGHT:
            continue

        pygame.draw.line(
            screen,
            GRAY,
            (SCREEN_WIDTH // 3, line_y),
            (SCREEN_WIDTH // 3, line_y + 20),
            2,
        )
        pygame.draw.line(
            screen,
            GRAY,
            (2 * SCREEN_WIDTH // 3, line_y),
            (2 * SCREEN_WIDTH // 3, line_y + 20),
            2,
        )

    # Snowflakes
    for flake in snowflakes:
        flake[1] += scroll_speed * 0.6
        if flake[1] > SCREEN_HEIGHT:
            flake[0] = float(random.randrange(0, SCREEN_WIDTH))
            flake[1] = float(random.randrange(-30, 0))
        pygame.draw.circle(
            screen,
            WHITE,
            (int(flake[0]), int(flake[1])),
            2,
        )
