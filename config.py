"""Configuration settings for the Ski Patrol Adventure game."""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DifficultySettings:
    """Simple container for difficulty-related settings."""

    name: str
    scroll_speed: float
    obstacle_spawn_rate: int
    flag_spawn_rate: int


# Screen settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (80, 160, 255)
RED = (220, 60, 60)
GREEN = (60, 200, 100)
GRAY = (210, 210, 210)
DARK_GRAY = (40, 40, 40)

# Extra colors for nicer background
SKY_BLUE = (135, 206, 250)
SNOW_WHITE = (245, 245, 255)
MOUNTAIN_GRAY = (200, 210, 220)

# Player and game stats
STARTING_LIVES: int = 3
MAX_LIVES: int = 5

# File used for storing high scores
HIGH_SCORE_FILE: str = "highscores.txt"

# Difficulty presets
DIFFICULTY_LEVELS: Dict[str, DifficultySettings] = {
    "easy": DifficultySettings(
        name="Easy",
        scroll_speed=3.0,
        obstacle_spawn_rate=70,
        flag_spawn_rate=110,
    ),
    "medium": DifficultySettings(
        name="Medium",
        scroll_speed=4.0,
        obstacle_spawn_rate=55,
        flag_spawn_rate=90,
    ),
    "hard": DifficultySettings(
        name="Hard",
        scroll_speed=5.0,
        obstacle_spawn_rate=40,
        flag_spawn_rate=70,
    ),
}

# How fast the game ramps up difficulty over time
DIFFICULTY_SCALE_INTERVAL_SECONDS: int = 10
SCROLL_SPEED_MULTIPLIER: float = 1.05
SPAWN_RATE_MULTIPLIER: float = 0.93

# Score tuning
POINTS_PER_SECOND: int = 10
POINTS_PER_FLAG: int = 100
POINTS_PER_RESCUE: int = 300
POINTS_PER_AVOIDED_OBSTACLE: int = 5  # currently unused but can be used later

# Base spawn rate for rescue targets (in frames)
RESCUE_BASE_SPAWN_RATE: int = 480  # roughly every 8 seconds at 60 FPS

# Font name used in menus and HUD
FONT_NAME: str = "arial"
