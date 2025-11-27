# Ski Patrol Adventure

A simple 2D skiing game built with Python and Pygame for our programming course project.

## What This Game Does

You control a skier going down a snowy mountain. Your goal is to:
- Avoid obstacles (trees and rocks) - they cost you lives
- Collect yellow flags for points
- Rescue people stuck in the snow (red jackets) for bonus points and extra lives
- Survive as long as possible and get a high score

The game gets progressively harder as you play - things move faster and spawn more frequently.

## Code Structure

We organized the code into separate modules to keep it clean and readable:

- `main.py` - Entry point to run the game
- `game.py` - Main game loop and state management (menu, tutorial, playing, game over)
- `sprites.py` - All sprite classes (Skier, Obstacle, Flag, Rescuee)
- `config.py` - Game settings and constants (colors, speeds, difficulty levels)
- `highscore.py` - Functions to save and load high score
- `ui_helpers.py` - Helper functions for drawing text and tutorial sprites
- `game_screens.py` - Drawing functions for menu, tutorial, and game over screens
- `background.py` - Background rendering (mountains, snow, lane markers)
- `tests/` - Unit tests for the high score module


## How to Run

1. Make sure you have Python 3.10+ installed

2. Install dependencies:
```bash
pip install pygame pytest
```

3. Run the game:
```bash
python3 main.py
```

## Controls

**Main Menu:**
- Press `1`, `2`, or `3` to select difficulty (Easy, Medium, Hard)
- `ESC` to quit

**Tutorial Screen:**
- `SPACE` or `ENTER` to start playing
- `ESC` to return to menu

**During Gameplay:**
- `←/→` or `A/D` to move left/right
- `P` to pause
- `ESC` to return to menu

**Game Over Screen:**
- `R` to restart with same difficulty
- `M` to return to main menu
- `ESC` to quit

## Testing

Run unit tests with:
```bash
pytest
```

## Design Decisions

We used object-oriented programming with Pygame sprites to keep the code organized. We split the large game file into smaller modules so each file has a clear purpose. All game parameters are centralized in `config.py` so we can easily adjust difficulty and scoring without touching the main game logic.

The graphics are simple shapes drawn with Pygame - no external image files needed. We added a tutorial screen so players understand what each game element does before they start playing.

## What We Learned

This project helped us practice:
- Object-oriented design in Python
- Working with Pygame for game development
- Organizing code into modules
- Writing unit tests
- Managing game state and events

---

Made for EN.540.635 Software Carpentry course project.
