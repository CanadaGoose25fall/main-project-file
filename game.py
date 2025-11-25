"""Main game logic and game loop for Ski Patrol Adventure."""

from __future__ import annotations

import random
from typing import Tuple

import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WHITE,
    BLACK,
    GRAY,
    DARK_GRAY,
    SKY_BLUE,
    SNOW_WHITE,
    MOUNTAIN_GRAY,
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
from highscore import load_high_scores, save_high_score, is_new_high_score
from sprites import Skier, Obstacle, Flag, Rescuee


class Game:
    """Encapsulates the skiing game state and main loop."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Ski Patrol Adventure")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_small = pygame.font.SysFont(FONT_NAME, 24)
        self.font_medium = pygame.font.SysFont(FONT_NAME, 32)
        self.font_large = pygame.font.SysFont(FONT_NAME, 54)

        self.running: bool = True
        self.state: str = "MENU"
        self.difficulty_key: str = "medium"

        self.all_sprites: pygame.sprite.Group
        self.obstacles: pygame.sprite.Group
        self.flags: pygame.sprite.Group
        self.rescuees: pygame.sprite.Group
        self.skier: Skier

        self.score: int = 0
        self.lives: int = STARTING_LIVES
        self.rescued_count: int = 0
        self.frame_count: int = 0
        self.seconds_elapsed: int = 0

        self.scroll_speed: float = DIFFICULTY_LEVELS[
            self.difficulty_key
        ].scroll_speed
        self.obstacle_spawn_rate: int = DIFFICULTY_LEVELS[
            self.difficulty_key
        ].obstacle_spawn_rate
        self.flag_spawn_rate: int = DIFFICULTY_LEVELS[
            self.difficulty_key
        ].flag_spawn_rate
        self.rescue_spawn_rate: int = RESCUE_BASE_SPAWN_RATE

        self.paused: bool = False
        self._background_offset: float = 0.0

        # Simple snow particles
        self.snowflakes: list[list[float]] = [
            [
                float(random.randrange(0, SCREEN_WIDTH)),
                float(random.randrange(0, SCREEN_HEIGHT)),
            ]
            for _ in range(80)
        ]

        self.reset_game_state()

    # ---------------------------------------------------------------------
    # Core state management
    # ---------------------------------------------------------------------

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
        """Apply the currently selected difficulty settings to the game."""
        settings = DIFFICULTY_LEVELS[self.difficulty_key]
        self.scroll_speed = settings.scroll_speed
        self.obstacle_spawn_rate = settings.obstacle_spawn_rate
        self.flag_spawn_rate = settings.flag_spawn_rate

    # ---------------------------------------------------------------------
    # Top-level run loop
    # ---------------------------------------------------------------------

    def run(self) -> None:
        """Main high-level game loop that switches between states."""
        while self.running:
            if self.state == "MENU":
                self.menu_loop()
            elif self.state == "PLAYING":
                self.play_loop()
            elif self.state == "GAME_OVER":
                self.game_over_loop()

        pygame.quit()

    # ---------------------------------------------------------------------
    # Menu state
    # ---------------------------------------------------------------------

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
                    elif event.key == pygame.K_1:
                        self.difficulty_key = "easy"
                        self.reset_game_state()
                        self.state = "PLAYING"
                        in_menu = False
                    elif event.key == pygame.K_2:
                        self.difficulty_key = "medium"
                        self.reset_game_state()
                        self.state = "PLAYING"
                        in_menu = False
                    elif event.key == pygame.K_3:
                        self.difficulty_key = "hard"
                        self.reset_game_state()
                        self.state = "PLAYING"
                        in_menu = False

            self.draw_menu()

    def draw_menu(self) -> None:
        """Draw the main menu screen."""
        self.screen.fill(DARK_GRAY)

        title_text = "Ski Patrol Adventure"
        subtitle_text = "Avoid trees and rocks, rescue people, and survive!"

        self.draw_text_center(
            title_text,
            self.font_large,
            WHITE,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4),
        )
        self.draw_text_center(
            subtitle_text,
            self.font_small,
            GRAY,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 50),
        )

        self.draw_text_center(
            "Press 1 for Easy",
            self.font_medium,
            WHITE,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        )
        self.draw_text_center(
            "Press 2 for Medium",
            self.font_medium,
            WHITE,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40),
        )
        self.draw_text_center(
            "Press 3 for Hard",
            self.font_medium,
            WHITE,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80),
        )

        self.draw_text_center(
            "In game: arrows/A-D to move, P to pause, ESC for menu",
            self.font_small,
            GRAY,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 90),
        )

        self.draw_text_center(
            "Press ESC or close window to quit",
            self.font_small,
            GRAY,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60),
        )

        # Show stored high scores
        scores = load_high_scores(limit=5)
        if scores:
            self.draw_text_center(
                "Top scores: " + ", ".join(str(s) for s in scores),
                self.font_small,
                WHITE,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130),
            )

        pygame.display.flip()

    # ---------------------------------------------------------------------
    # Play state
    # ---------------------------------------------------------------------

    def play_loop(self) -> None:
        """Main gameplay loop where the skier moves and dodges obstacles."""
        playing = True
        while playing and self.running and self.state == "PLAYING":
            dt = self.clock.tick(FPS) / 1000.0

            self.handle_play_events()

            if self.paused:
                self.draw_play(paused=True)
                continue

            self.frame_count += 1

            # Update timers
            self.seconds_elapsed = self.frame_count // FPS

            # Ramp up difficulty over time
            if (
                self.seconds_elapsed > 0
                and self.seconds_elapsed % DIFFICULTY_SCALE_INTERVAL_SECONDS == 0
                and self.frame_count % FPS == 0
            ):
                self.increase_difficulty()

            # Spawn new obstacles, flags, and rescuees
            self.maybe_spawn_obstacle()
            self.maybe_spawn_flag()
            self.maybe_spawn_rescue()

            # Update all sprites
            self.all_sprites.update()

            # Increase score gradually
            self.score += int(POINTS_PER_SECOND * dt)

            # Scroll background position
            self._background_offset += self.scroll_speed * dt * 60

            # Handle collisions
            self.handle_collisions()

            # Check for game over
            if self.lives <= 0:
                save_high_score(self.score)
                self.state = "GAME_OVER"
                playing = False

            # Draw frame
            self.draw_play(paused=False)

    def handle_play_events(self) -> None:
        """Handle events while the game is in the PLAYING state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.state = "MENU"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to menu
                    self.state = "MENU"
                    self.paused = False
                elif event.key == pygame.K_p:
                    # Toggle pause
                    self.paused = not self.paused

    def increase_difficulty(self) -> None:
        """Slightly increase scroll speed and spawn frequencies."""
        self.scroll_speed *= SCROLL_SPEED_MULTIPLIER
        self.obstacle_spawn_rate = max(
            15,
            int(self.obstacle_spawn_rate * SPAWN_RATE_MULTIPLIER),
        )
        self.flag_spawn_rate = max(
            20,
            int(self.flag_spawn_rate * SPAWN_RATE_MULTIPLIER),
        )
        self.rescue_spawn_rate = max(
            RESCUE_BASE_SPAWN_RATE // 2,
            int(self.rescue_spawn_rate * SPAWN_RATE_MULTIPLIER),
        )

    def maybe_spawn_obstacle(self) -> None:
        """Create a new obstacle at the top of the screen based on spawn rate."""
        if self.frame_count % self.obstacle_spawn_rate == 0:
            obstacle = Obstacle(speed_y=self.scroll_speed)
            self.all_sprites.add(obstacle)
            self.obstacles.add(obstacle)

    def maybe_spawn_flag(self) -> None:
        """Create a new collectible flag based on spawn rate."""
        if self.frame_count % self.flag_spawn_rate == 0:
            flag = Flag(speed_y=self.scroll_speed)
            self.all_sprites.add(flag)
            self.flags.add(flag)

    def maybe_spawn_rescue(self) -> None:
        """Create a new rescue target occasionally."""
        if self.frame_count < FPS * 5:
            return
        if self.frame_count % self.rescue_spawn_rate == 0:
            if random.random() < 0.85:
                rescuee = Rescuee(speed_y=self.scroll_speed)
                self.all_sprites.add(rescuee)
                self.rescuees.add(rescuee)

    def handle_collisions(self) -> None:
        """Check for collisions between the skier, obstacles, and flags."""
        # Collisions with obstacles reduce lives
        hits = pygame.sprite.spritecollide(self.skier, self.obstacles, True)
        if hits:
            self.lives -= 1
            if self.lives < 0:
                self.lives = 0

        # Collisions with flags give bonus score
        flag_hits = pygame.sprite.spritecollide(self.skier, self.flags, True)
        if flag_hits:
            self.score += POINTS_PER_FLAG * len(flag_hits)

        # Collisions with rescuees give big score and maybe extra life
        rescue_hits = pygame.sprite.spritecollide(
            self.skier,
            self.rescuees,
            True,
        )
        if rescue_hits:
            count = len(rescue_hits)
            self.rescued_count += count
            self.score += POINTS_PER_RESCUE * count
            if self.lives < MAX_LIVES:
                self.lives = min(MAX_LIVES, self.lives + 1)

    def draw_play(self, paused: bool = False) -> None:
        """Draw the current gameplay frame."""
        self.draw_scrolling_background()

        self.all_sprites.draw(self.screen)

        # HUD: score, lives, difficulty, rescued count
        score_text = f"Score: {self.score}"
        lives_text = f"Lives: {self.lives}"
        rescued_text = f"Rescued: {self.rescued_count}"
        difficulty_name = DIFFICULTY_LEVELS[self.difficulty_key].name
        difficulty_text = f"Difficulty: {difficulty_name}"

        self.draw_text_topleft(score_text, self.font_small, BLACK, (10, 10))
        self.draw_text_topleft(lives_text, self.font_small, BLACK, (10, 40))
        self.draw_text_topleft(rescued_text, self.font_small, BLACK, (10, 70))
        self.draw_text_topleft(difficulty_text, self.font_small, BLACK, (10, 100))

        self.draw_text_topleft(
            "P: pause | ESC: menu",
            self.font_small,
            BLACK,
            (SCREEN_WIDTH - 220, 10),
        )

        if paused:
            # Dark overlay + pause text
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.screen.blit(overlay, (0, 0))

            self.draw_text_center(
                "Paused",
                self.font_large,
                WHITE,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20),
            )
            self.draw_text_center(
                "Press P to resume",
                self.font_small,
                WHITE,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30),
            )

        pygame.display.flip()

    def draw_scrolling_background(self) -> None:
        """Draw a scrolling snow slope with lane markers, mountains, and falling snow."""
        # Sky
        self.screen.fill(SKY_BLUE)
        snow_top = SCREEN_HEIGHT // 4

        # Distant mountains
        pygame.draw.polygon(
            self.screen,
            MOUNTAIN_GRAY,
            [
                (0, snow_top + 40),
                (SCREEN_WIDTH // 4, 20),
                (SCREEN_WIDTH // 2, snow_top + 40),
            ],
        )
        pygame.draw.polygon(
            self.screen,
            MOUNTAIN_GRAY,
            [
                (SCREEN_WIDTH // 2, snow_top + 60),
                (3 * SCREEN_WIDTH // 4, 30),
                (SCREEN_WIDTH, snow_top + 60),
            ],
        )

        # Snow field
        pygame.draw.rect(
            self.screen,
            SNOW_WHITE,
            (0, snow_top, SCREEN_WIDTH, SCREEN_HEIGHT - snow_top),
        )

        # Slope lane markers
        offset = int(self._background_offset) % 40
        for y in range(-40, SCREEN_HEIGHT, 40):
            line_y = snow_top + y + offset
            if line_y < snow_top or line_y > SCREEN_HEIGHT:
                continue

            pygame.draw.line(
                self.screen,
                GRAY,
                (SCREEN_WIDTH // 3, line_y),
                (SCREEN_WIDTH // 3, line_y + 20),
                2,
            )
            pygame.draw.line(
                self.screen,
                GRAY,
                (2 * SCREEN_WIDTH // 3, line_y),
                (2 * SCREEN_WIDTH // 3, line_y + 20),
                2,
            )

        # Snowflakes
        for flake in self.snowflakes:
            flake[1] += self.scroll_speed * 0.6
            if flake[1] > SCREEN_HEIGHT:
                flake[0] = float(random.randrange(0, SCREEN_WIDTH))
                flake[1] = float(random.randrange(-30, 0))
            pygame.draw.circle(
                self.screen,
                WHITE,
                (int(flake[0]), int(flake[1])),
                2,
            )

    # ---------------------------------------------------------------------
    # Game-over state
    # ---------------------------------------------------------------------

    def game_over_loop(self) -> None:
        """Handle events and drawing for the game-over screen."""
        is_high = is_new_high_score(self.score)
        scores = load_high_scores(limit=5)

        in_game_over = True
        while in_game_over and self.running and self.state == "GAME_OVER":
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    in_game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Back to menu
                        self.state = "MENU"
                        in_game_over = False
                    elif event.key == pygame.K_r:
                        # Restart with same difficulty
                        self.reset_game_state()
                        self.state = "PLAYING"
                        in_game_over = False
                    elif event.key == pygame.K_m:
                        # Go back to main menu to choose difficulty
                        self.state = "MENU"
                        in_game_over = False

            self.draw_game_over(is_high, scores)

    def draw_game_over(self, is_high_score: bool, scores: list[int]) -> None:
        """Draw the game-over screen."""
        self.screen.fill(DARK_GRAY)

        self.draw_text_center(
            "Game Over",
            self.font_large,
            WHITE,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4),
        )
        self.draw_text_center(
            f"Final score: {self.score}",
            self.font_medium,
            WHITE,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 60),
        )
        self.draw_text_center(
            f"Total rescued: {self.rescued_count}",
            self.font_medium,
            WHITE,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 110),
        )

        if is_high_score:
            self.draw_text_center(
                "New high score!",
                self.font_medium,
                (255, 215, 0),
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 160),
            )

        if scores:
            top_scores_text = "Top scores: " + ", ".join(str(s) for s in scores)
            self.draw_text_center(
                top_scores_text,
                self.font_small,
                WHITE,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            )

        self.draw_text_center(
            "Press R to restart, M for menu, ESC to quit",
            self.font_small,
            GRAY,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80),
        )

        pygame.display.flip()

    # ---------------------------------------------------------------------
    # Text helpers
    # ---------------------------------------------------------------------

    def draw_text_center(
        self,
        text: str,
        font: pygame.font.Font,
        color: Tuple[int, int, int],
        center: Tuple[int, int],
    ) -> None:
        """Render text and draw it centered at the given position."""
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=center)
        self.screen.blit(surface, rect)

    def draw_text_topleft(
        self,
        text: str,
        font: pygame.font.Font,
        color: Tuple[int, int, int],
        topleft: Tuple[int, int],
    ) -> None:
        """Render text and draw it with the given top-left coordinate."""
        surface = font.render(text, True, color)
        rect = surface.get_rect(topleft=topleft)
        self.screen.blit(surface, rect)
