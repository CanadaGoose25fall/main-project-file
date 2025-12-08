"""Screen drawing functions for menu, tutorial, and game over."""

from typing import Tuple
import pygame
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    BLACK,
    GRAY,
    DARK_GRAY,
    GREEN,
    RED,
    POINTS_PER_FLAG,
    POINTS_PER_RESCUE,
)
from highscore import load_high_score
from ui_helpers import (
    draw_text_center,
    draw_text_topleft,
    create_tree_sprite,
    create_rock_sprite,
    create_flag_sprite,
    create_rescuee_sprite,
)


def draw_menu(screen: pygame.Surface, fonts: dict) -> None:
    """
    Draw the main menu screen.
    Parameters
        screen: pygame.Surface
            The game screen surface to draw on.
        fonts: dict
            Dictionary of font objects for different text sizes.
    Returns: None
    """
    screen.fill(DARK_GRAY)

    draw_text_center(
        screen,
        "Ski Patrol Adventure",
        fonts['large'],
        WHITE,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4),
    )
    draw_text_center(
        screen,
        "Avoid trees and rocks, rescue people, and survive!",
        fonts['small'],
        GRAY,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 50),
    )

    draw_text_center(
        screen,
        "Press 1 for Easy",
        fonts['medium'],
        WHITE,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
    )
    draw_text_center(
        screen,
        "Press 2 for Medium",
        fonts['medium'],
        WHITE,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40),
    )
    draw_text_center(
        screen,
        "Press 3 for Hard",
        fonts['medium'],
        WHITE,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80),
    )

    draw_text_center(
        screen,
        "In game: arrows/A-D to move, P to pause, ESC for menu",
        fonts['small'],
        GRAY,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 90),
    )
    draw_text_center(
        screen,
        "Press ESC or close window to quit",
        fonts['small'],
        GRAY,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60),
    )

    high_score = load_high_score()
    if high_score > 0:
        draw_text_center(
            screen,
            f"High Score: {high_score}",
            fonts['small'],
            WHITE,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130),
        )

    pygame.display.flip()


def draw_tutorial(screen: pygame.Surface, fonts: dict) -> None:
    """
    Draw the tutorial screen with examples of game elements.
    Parameters
        screen: pygame.Surface
            The game screen surface to draw on.
        fonts: dict
            Dictionary of font objects for different text sizes.
    No Returns
    """
    screen.fill(DARK_GRAY)

    draw_text_center(
        screen,
        "How to Play",
        fonts['large'],
        WHITE,
        (SCREEN_WIDTH // 2, 50),
    )

    start_y = 120
    item_spacing = 105

    # Tree obstacle
    draw_tutorial_item(
        screen,
        fonts,
        start_y,
        "Tree (Obstacle)",
        "Avoid trees! They will cost you a life.",
        create_tree_sprite(),
        GREEN
    )

    # Rock obstacle
    draw_tutorial_item(
        screen,
        fonts,
        start_y + item_spacing,
        "Rock (Obstacle)",
        "Avoid rocks! They will also cost you a life.",
        create_rock_sprite(),
        (160, 160, 160)
    )

    # Flag
    draw_tutorial_item(
        screen,
        fonts,
        start_y + item_spacing * 2,
        "Yellow Flag",
        f"Collect flags to gain {POINTS_PER_FLAG} points!",
        create_flag_sprite(),
        (255, 255, 0)
    )

    # Rescue target
    draw_tutorial_item(
        screen,
        fonts,
        start_y + item_spacing * 3,
        "Person in Need (Red Jacket)",
        f"Rescue them for {POINTS_PER_RESCUE} points + 1 extra life!",
        create_rescuee_sprite(),
        RED
    )

    draw_text_center(
        screen,
        "Press SPACE or ENTER to start playing",
        fonts['medium'],
        (255, 215, 0),
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50),
    )
    draw_text_center(
        screen,
        "Press ESC to return to menu",
        fonts['small'],
        GRAY,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20),
    )

    pygame.display.flip()


def draw_tutorial_item(
    screen: pygame.Surface,
    fonts: dict,
    y_pos: int, 
    title: str, 
    description: str, 
    sprite_surface: pygame.Surface,
    highlight_color: Tuple[int, int, int]
) -> None:
    """
    Draw a single tutorial item with sprite and text.
    Parameters
        screen: pygame.Surface
            The game screen surface to draw on.
        fonts: dict
            Dictionary of font objects for different text sizes.
        y_pos: int
            Vertical position for this tutorial item.
        title: str
            Title text for this game element.
        description: str
            Description text explaining what this element does.
        sprite_surface: pygame.Surface
            The visual representation of the game element.
        highlight_color: Tuple[int, int, int]
            RGB color for the border around the sprite.
    No returns
    """
    sprite_x = 100
    screen.blit(sprite_surface, (sprite_x, y_pos - sprite_surface.get_height() // 2))
    
    box_padding = 10
    pygame.draw.rect(
        screen,
        highlight_color,
        (
            sprite_x - box_padding,
            y_pos - sprite_surface.get_height() // 2 - box_padding,
            sprite_surface.get_width() + box_padding * 2,
            sprite_surface.get_height() + box_padding * 2
        ),
        3
    )

    draw_text_topleft(
        screen,
        title,
        fonts['medium'],
        WHITE,
        (200, y_pos - 30)
    )
    draw_text_topleft(
        screen,
        description,
        fonts['small'],
        GRAY,
        (200, y_pos + 5)
    )


def draw_game_over(
    screen: pygame.Surface,
    fonts: dict,
    score: int,
    rescued_count: int,
    is_high_score: bool,
    high_score: int
) -> None:
    """Draw the game-over screen."""
    screen.fill(DARK_GRAY)

    draw_text_center(
        screen,
        "Game Over",
        fonts['large'],
        WHITE,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4),
    )
    draw_text_center(
        screen,
        f"Your score: {score}",
        fonts['medium'],
        WHITE,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 60),
    )
    draw_text_center(
        screen,
        f"Total rescued: {rescued_count}",
        fonts['medium'],
        WHITE,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 110),
    )

    if is_high_score:
        draw_text_center(
            screen,
            "New High Score!",
            fonts['medium'],
            (255, 215, 0),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 110),
        )
    else:
        draw_text_center(
            screen,
            f"High Score: {high_score}",
            fonts['small'],
            GRAY,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 160),
        )

    draw_text_center(
        screen,
        "Press R to restart, M for menu, ESC to quit",
        fonts['small'],
        GRAY,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80),
    )

    pygame.display.flip()
