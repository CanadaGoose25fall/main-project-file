"""Sprite classes for the Ski Patrol Adventure game."""

from __future__ import annotations

import random

import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLUE,
    RED,
    GREEN,
)


class Skier(pygame.sprite.Sprite):
    """Player-controlled skier sprite with visible skis and poles."""

    def __init__(self) -> None:
        super().__init__()
        width, height = 40, 50
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # Skis
        ski_color = (160, 80, 40)
        pygame.draw.rect(self.image, ski_color, (4, height - 8, 14, 4))
        pygame.draw.rect(self.image, ski_color, (width - 18, height - 8, 14, 4))

        # Body (blue jacket)
        body_rect = pygame.Rect(10, 18, 20, 22)
        pygame.draw.rect(self.image, BLUE, body_rect)

        # Head
        pygame.draw.circle(self.image, (250, 220, 180), (width // 2, 12), 7)

        # Arms and ski poles
        pole_color = (120, 120, 120)
        pygame.draw.line(self.image, pole_color, (10, 22), (2, height - 10), 2)
        pygame.draw.line(
            self.image,
            pole_color,
            (width - 10, 22),
            (width - 2, height - 10),
            2,
        )

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 60
        self.speed_x: float = 0.0
        self.move_speed: float = 6.0

    def update(self) -> None:
        """Update the skier position based on keyboard input."""
        keys = pygame.key.get_pressed()
        self.speed_x = 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -self.move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = self.move_speed

        self.rect.x += int(self.speed_x)

        # Keep the skier on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Obstacle(pygame.sprite.Sprite):
    """Tree or rock that the skier must avoid."""

    def __init__(self, speed_y: float) -> None:
        super().__init__()
        width, height = 32, 48
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # Randomly decide if this is a tree or a rock
        if random.random() < 0.7:
            # Tree
            pygame.draw.polygon(
                self.image,
                GREEN,
                [
                    (width // 2, 5),
                    (4, height - 18),
                    (width - 4, height - 18),
                ],
            )
            pygame.draw.rect(
                self.image,
                (120, 80, 40),
                (width // 2 - 3, height - 18, 6, 16),
            )
        else:
            # Rock
            pygame.draw.polygon(
                self.image,
                (160, 160, 160),
                [
                    (4, height - 8),
                    (width // 2 - 6, height - 22),
                    (width - 4, height - 10),
                ],
            )

        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(20, SCREEN_WIDTH - 20)
        self.rect.bottom = 0

        self.speed_y: float = speed_y

    def update(self) -> None:
        """Move the obstacle down the slope and remove it when it leaves the screen."""
        self.rect.y += int(self.speed_y)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Flag(pygame.sprite.Sprite):
    """Collectible flag sprite that gives bonus score."""

    def __init__(self, speed_y: float) -> None:
        super().__init__()
        width, height = 18, 36
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # Flag pole
        pygame.draw.rect(
            self.image,
            (160, 160, 160),
            (width // 2 - 1, 5, 3, height - 8),
        )
        # Flag cloth
        pygame.draw.polygon(
            self.image,
            (255, 255, 0),
            [(width // 2 + 1, 7), (width - 3, 14), (width // 2 + 1, 21)],
        )

        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(20, SCREEN_WIDTH - 20)
        self.rect.bottom = 0

        self.speed_y: float = speed_y

    def update(self) -> None:
        """Move the flag down the slope and remove it when it leaves the screen."""
        self.rect.y += int(self.speed_y)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Rescuee(pygame.sprite.Sprite):
    """Person stuck in the snow that the skier can rescue."""

    def __init__(self, speed_y: float) -> None:
        super().__init__()
        width, height = 30, 34
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # Snow mound
        pygame.draw.ellipse(
            self.image,
            (240, 240, 255),
            (0, height - 18, width, 18),
        )

        # Body (red jacket)
        pygame.draw.rect(
            self.image,
            (220, 50, 50),
            (width // 2 - 6, height - 26, 12, 10),
        )

        # Head
        pygame.draw.circle(
            self.image,
            (250, 220, 180),
            (width // 2, height - 30),
            5,
        )

        # Small waving arm
        pygame.draw.line(
            self.image,
            (220, 50, 50),
            (width // 2 + 4, height - 26),
            (width - 4, height - 32),
            2,
        )

        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(20, SCREEN_WIDTH - 20)
        self.rect.bottom = 0

        # Rescuees move a bit slower than obstacles
        self.speed_y: float = speed_y * 0.9

    def update(self) -> None:
        """Move the rescuee down the slope and remove it when it leaves the screen."""
        self.rect.y += int(self.speed_y)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
