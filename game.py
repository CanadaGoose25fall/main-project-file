"""Main game logic and game loop for Ski Patrol Adventure."""

from __future__ import annotations

import random
import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WHITE,
    BLACK,
    STARTING_LIVES,
    MAX_LIVES,
    DIFFICULTY_LEVELS,
    DIFFICULTY_SCALE_INTERVAL_SECONDS,
    SCROLL_SPEED_MULTIPLIER,
    SPAWN_RATE_MULTIPLIER,
    POINTS_PER_SECOND,
    POINTS_PER_FLAG,
    POINTS_PER_RESCUE,
    RESCUE_BASE_SPAWN_RATE,
    FONT_NAME,
)
from highscore import load_high_score, save_high_score, is_new_high_score
from sprites import Skier, Obstacle, Flag, Rescuee
from game_screens import draw_menu, draw_tutorial, draw_game_over
from background import draw_scrolling_background
from ui_helpers import draw_text_topleft


class Game:
    """Encapsulates the skiing game state and main loop."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Ski Patrol Adventure")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Fonts dictionary for easy access
        self.fonts = {
            'small': pygame.font.SysFont(FONT_NAME, 24),
            'medium': pygame.font.SysFont(FONT_NAME, 32),
            'large': pygame.font.SysFont(FONT_NAME, 54),
        }

        self.running: bool = True
        self.state: str = "MENU"
        self.difficulty_key: str = "medium"

        # Sprite groups
        self.all_sprites: pygame.sprite.Group
        self.obstacles: pygame.sprite.Group
        self.flags: pygame.sprite.Group
        self.rescuees: pygame.sprite.Group
        self.skier: Skier

        # Game stats
        self.score: int = 0
        self.lives: int = STARTING_LIVES
        self.rescued_count: int = 0
        self.frame_count: int = 0
        self.seconds_elapsed: int = 0

        # Difficulty settings
        self.scroll_speed: float = DIFFICULTY_LEVELS[self.difficulty_key].scroll_speed
        self.obstacle_spawn_rate: int = DIFFICULTY_LEVELS[self.difficulty_key].obstacle_spawn_rate
        self.flag_spawn_rate: int = DIFFICULTY_LEVELS[self.difficulty_key].flag_spawn_rate
        self.rescue_spawn_rate: int = RESCUE_BASE_SPAWN_RATE

        self.paused: bool = False
        self._background_offset: float = 0.0

        # Snowflakes
        self.snowflakes: list[list[float]] = [
            [
                float(random.randrange(0, SCREEN_WIDTH)),
                float(random.randrange(0, SCREEN_HEIGHT)),
            ]
            for _ in range(80)
        ]

        self.reset_game_state()

    def reset_game_state(self) -> None:
        """Create all sprite groups and reset score, lives, and timers."""
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()
        self.rescuees = pygame.sprite.Group()

        self.skier = Skier()
        self.all_sprites.add(self.skier)

        self.score = 0
        self.lives = STARTING_LIVES
        self.rescued_count = 0
        self.frame_count = 0
        self.seconds_elapsed = 0
        self._background_offset = 0.0
        self.paused = False
        self.rescue_spawn_rate = RESCUE_BASE_SPAWN_RATE

        self.apply_difficulty_settings()

    def apply_difficulty_settings(self) -> None:
        """Apply the currently selected difficulty settings."""
        settings = DIFFICULTY_LEVELS[self.difficulty_key]
        self.scroll_speed = settings.scroll_speed
        self.obstacle_spawn_rate = settings.obstacle_spawn_rate
        self.flag_spawn_rate = settings.flag_spawn_rate

    def run(self) -> None:
        """Main high-level game loop that switches between states."""
        while self.running:
            if self.state == "MENU":
                self.menu_loop()
            elif self.state == "TUTORIAL":
                self.tutorial_loop()
            elif self.state == "PLAYING":
                self.play_loop()
            elif self.state == "GAME_OVER":
                self.game_over_loop()

        pygame.quit()

    # ===== MENU STATE =====
    def menu_loop(self) -> None:
        """Handle events and drawing for the main menu."""
        in_menu = True
        while in_menu and self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    in_menu = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        in_menu = False
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        difficulty_map = {
                            pygame.K_1: "easy",
                            pygame.K_2: "medium",
                            pygame.K_3: "hard"
                        }
                        self.difficulty_key = difficulty_map[event.key]
                        self.reset_game_state()
                        self.state = "TUTORIAL"
                        in_menu = False

            draw_menu(self.screen, self.fonts)

    # ===== TUTORIAL STATE =====
    def tutorial_loop(self) -> None:
        """Handle events and drawing for the tutorial screen."""
        in_tutorial = True
        while in_tutorial and self.running and self.state == "TUTORIAL":
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    in_tutorial = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.state = "PLAYING"
                        in_tutorial = False
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                        in_tutorial = False

            draw_tutorial(self.screen, self.fonts)

    # ===== PLAYING STATE =====
    def play_loop(self) -> None:
        """Main gameplay loop."""
        playing = True
        while playing and self.running and self.state == "PLAYING":
            dt = self.clock.tick(FPS) / 1000.0

            self.handle_play_events()

            if self.paused:
                self.draw_play(paused=True)
                continue

            self.update_game_state(dt)
            self.draw_play(paused=False)

            if self.lives <= 0:
                save_high_score(self.score)
                self.state = "GAME_OVER"
                playing = False

    def handle_play_events(self) -> None:
        """Handle keyboard events during gameplay."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.state = "MENU"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
                    self.paused = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused

    def update_game_state(self, dt: float) -> None:
        """Update all game logic."""
        self.frame_count += 1
        self.seconds_elapsed = self.frame_count // FPS

        # Ramp up difficulty
        if (
            self.seconds_elapsed > 0
            and self.seconds_elapsed % DIFFICULTY_SCALE_INTERVAL_SECONDS == 0
            and self.frame_count % FPS == 0
        ):
            self.increase_difficulty()

        # Spawn sprites
        self.spawn_sprites()

        # Update all sprites
        self.all_sprites.update()

        # Increase score
        self.score += int(POINTS_PER_SECOND * dt)

        # Scroll background
        self._background_offset += self.scroll_speed * dt * 60

        # Handle collisions
        self.handle_collisions()

    def spawn_sprites(self) -> None:
        """Spawn obstacles, flags, and rescue targets."""
        if self.frame_count % self.obstacle_spawn_rate == 0:
            obstacle = Obstacle(speed_y=self.scroll_speed)
            self.all_sprites.add(obstacle)
            self.obstacles.add(obstacle)

        if self.frame_count % self.flag_spawn_rate == 0:
            flag = Flag(speed_y=self.scroll_speed)
            self.all_sprites.add(flag)
            self.flags.add(flag)

        if self.frame_count >= FPS * 5:
            if self.frame_count % self.rescue_spawn_rate == 0:
                if random.random() < 0.85:
                    rescuee = Rescuee(speed_y=self.scroll_speed)
                    self.all_sprites.add(rescuee)
                    self.rescuees.add(rescuee)

    def increase_difficulty(self) -> None:
        """Increase scroll speed and spawn frequencies."""
        self.scroll_speed *= SCROLL_SPEED_MULTIPLIER
        self.obstacle_spawn_rate = max(15, int(self.obstacle_spawn_rate * SPAWN_RATE_MULTIPLIER))
        self.flag_spawn_rate = max(20, int(self.flag_spawn_rate * SPAWN_RATE_MULTIPLIER))
        self.rescue_spawn_rate = max(
            RESCUE_BASE_SPAWN_RATE // 2,
            int(self.rescue_spawn_rate * SPAWN_RATE_MULTIPLIER)
        )

    def handle_collisions(self) -> None:
        """Check for all sprite collisions."""
        # Obstacles
        hits = pygame.sprite.spritecollide(self.skier, self.obstacles, True)
        if hits:
            self.lives = max(0, self.lives - 1)

        # Flags
        flag_hits = pygame.sprite.spritecollide(self.skier, self.flags, True)
        if flag_hits:
            self.score += POINTS_PER_FLAG * len(flag_hits)

        # Rescuees
        rescue_hits = pygame.sprite.spritecollide(self.skier, self.rescuees, True)
        if rescue_hits:
            count = len(rescue_hits)
            self.rescued_count += count
            self.score += POINTS_PER_RESCUE * count
            if self.lives < MAX_LIVES:
                self.lives = min(MAX_LIVES, self.lives + 1)

    def draw_play(self, paused: bool = False) -> None:
        """Draw the gameplay screen."""
        draw_scrolling_background(
            self.screen,
            self._background_offset,
            self.snowflakes,
            self.scroll_speed
        )

        self.all_sprites.draw(self.screen)

        # HUD
        self.draw_hud()

        if paused:
            self.draw_pause_overlay()

        pygame.display.flip()

    def draw_hud(self) -> None:
        """Draw the heads-up display."""
        draw_text_topleft(
            self.screen,
            f"Score: {self.score}",
            self.fonts['small'],
            BLACK,
            (10, 10)
        )
        draw_text_topleft(
            self.screen,
            f"Lives: {self.lives}",
            self.fonts['small'],
            BLACK,
            (10, 40)
        )
        draw_text_topleft(
            self.screen,
            f"Rescued: {self.rescued_count}",
            self.fonts['small'],
            BLACK,
            (10, 70)
        )
        draw_text_topleft(
            self.screen,
            f"Difficulty: {DIFFICULTY_LEVELS[self.difficulty_key].name}",
            self.fonts['small'],
            BLACK,
            (10, 100)
        )
        draw_text_topleft(
            self.screen,
            "P: pause | ESC: menu",
            self.fonts['small'],
            BLACK,
            (SCREEN_WIDTH - 220, 10)
        )

    def draw_pause_overlay(self) -> None:
        """Draw the pause screen overlay."""
        from ui_helpers import draw_text_center
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        draw_text_center(
            self.screen,
            "Paused",
            self.fonts['large'],
            WHITE,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
        )
        draw_text_center(
            self.screen,
            "Press P to resume",
            self.fonts['small'],
            WHITE,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
        )

    # ===== GAME OVER STATE =====
    def game_over_loop(self) -> None:
        """Handle events and drawing for game over screen."""
        is_high = is_new_high_score(self.score)
        high_score = load_high_score()

        in_game_over = True
        while in_game_over and self.running and self.state == "GAME_OVER":
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    in_game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                        in_game_over = False
                    elif event.key == pygame.K_r:
                        self.reset_game_state()
                        self.state = "TUTORIAL"
                        in_game_over = False
                    elif event.key == pygame.K_m:
                        self.state = "MENU"
                        in_game_over = False

            draw_game_over(
                self.screen,
                self.fonts,
                self.score,
                self.rescued_count,
                is_high,
                high_score
            )
