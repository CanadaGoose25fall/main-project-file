"""UI helper functions for drawing text and tutorial sprites."""

from typing import Tuple
import pygame
from config import GREEN, RED


def draw_text_center(
    screen: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: Tuple[int, int, int],
    center: Tuple[int, int],
) -> None:
    """
    Render text and draw it centered at the given position.
    
    **Parameters**
    
        screen: *pygame.Surface*
            The surface to draw on.
        text: *str*
            The text string to render.
        font: *pygame.font.Font*
            The font object to use.
        color: *Tuple[int, int, int]*
            RGB color tuple.
        center: *Tuple[int, int]*
            The (x, y) position to center the text at.
            
    **Returns**
    
        None
    """
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=center)
    screen.blit(surface, rect)


def draw_text_topleft(
    screen: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: Tuple[int, int, int],
    topleft: Tuple[int, int],
) -> None:
    """
    Render text and draw it with the given top-left coordinate.
        
    **Parameters**
    
        screen: *pygame.Surface*
            The surface to draw on.
        text: *str*
            The text string to render.
        font: *pygame.font.Font*
            The font object to use.
        color: *Tuple[int, int, int]*
            RGB color tuple.
        topleft: *Tuple[int, int]*
            The (x, y) position for the top-left corner.
            
    **Returns**
    
        None
    """
    surface = font.render(text, True, color)
    rect = surface.get_rect(topleft=topleft)
    screen.blit(surface, rect)


def create_tree_sprite() -> pygame.Surface:
    """
    Create a tree sprite for tutorial display.
    
    **Parameters： None
        
    **Returns**
        surface: *pygame.Surface*
            A surface with a tree drawn on it.
    """
    width, height = 32, 48
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    
    pygame.draw.polygon(
        surface,
        GREEN,
        [
            (width // 2, 5),
            (4, height - 18),
            (width - 4, height - 18),
        ],
    )
    pygame.draw.rect(
        surface,
        (120, 80, 40),
        (width // 2 - 3, height - 18, 6, 16),
    )
    return surface


def create_rock_sprite() -> pygame.Surface:
    """
    Create a rock sprite for tutorial.
    No parameter. 
    Returns
        surface: *pygame.Surface*
            A surface with a rock drawn on it.
    """
    width, height = 32, 48
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    
    pygame.draw.polygon(
        surface,
        (160, 160, 160),
        [
            (4, height - 8),
            (width // 2 - 6, height - 22),
            (width - 4, height - 10),
        ],
    )
    return surface


def create_flag_sprite() -> pygame.Surface:
    """
    Create a flag sprite for tutorial.
    no parameter
    return surface: *pygame.Surface*
            A surface with a flag drawn on it.
    """
    width, height = 18, 36
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    
    pygame.draw.rect(
        surface,
        (160, 160, 160),
        (width // 2 - 1, 5, 3, height - 8),
    )
    pygame.draw.polygon(
        surface,
        (255, 255, 0),
        [(width // 2 + 1, 7), (width - 3, 14), (width // 2 + 1, 21)],
    )
    return surface


def create_rescuee_sprite() -> pygame.Surface:
    """
    Create a rescuee sprite for tutorial.
    No parameter
    Returns:
        surface: *pygame.Surface*
            A surface with a person in need drawn on it.
    """
    width, height = 30, 34
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    
    pygame.draw.ellipse(
        surface,
        (240, 240, 255),
        (0, height - 18, width, 18),
    )
    pygame.draw.rect(
        surface,
        (220, 50, 50),
        (width // 2 - 6, height - 26, 12, 10),
    )
    pygame.draw.circle(
        surface,
        (250, 220, 180),
        (width // 2, height - 30),
        5,
    )
    pygame.draw.line(
        surface,
        (220, 50, 50),
        (width // 2 + 4, height - 26),
        (width - 4, height - 32),
        2,
    )
    return surface
