# Ski Patrol Adventure

A small 2D skiing game written in Python using Pygame.

The player controls a skier going down a snowy slope, avoiding trees and rocks, collecting flags, and rescuing people who are stuck in the snow. The goal is to survive as long as possible, increase your score, and set new high scores on your local machine.


## Features

- **Object-oriented design**
  - `Skier`, `Obstacle`, `Flag`, and `RescueTarget` are implemented as Pygame `Sprite` classes.
  - `Game` class encapsulates the main game loop and state machine.
- **Multi-file structure**
  - Game logic, sprites, configuration, and high-score persistence are organized into separate modules.
- **Config module**
  - All screen sizes, speeds, colors, difficulty settings, and scoring constants are centralized in `config.py`.
- **Difficulty modes**
  - Easy, Medium, Hard modes with different scroll speeds and spawn rates.
  - Difficulty automatically ramps up over time (faster scrolling, more obstacles, more items).
- **Rescue mechanic**
  - Special `RescueTarget` sprites represent people stuck in the snow.
  - Colliding with a rescue target grants a large score bonus and can restore lives (up to a maximum).
- **Score and high-score system**
  - Score increases over time and when collecting flags or rescuing people.
  - High scores are stored in a simple text file (`highscores.txt`) using a separate `highscore.py` module.
- **Menu and game states**
  - Main menu with difficulty selection.
  - In-game state with HUD (score, lives, difficulty).
  - Game-over screen showing final score, top scores, and “New high score!” message when appropriate.
- **Pause function**
  - Press `P` to pause and resume during the game; a dark overlay and text appear while paused.
- **Unit tests**
  - `pytest` tests for the high-score module (`tests/test_highscore.py`).

---

## Project Structure

Top-level layout of the repository:

```text
canadagoose/
│  main.py            # Entry point that creates and runs the Game
│  game.py            # Game class, state machine, main loop, drawing and events
│  sprites.py         # Sprite classes: Skier, Obstacle, Flag, RescueTarget
│  config.py          # Configuration: screen, colors, difficulty, scoring constants
│  highscore.py       # High-score file loading/saving utilities
│  highscores.txt     # High-score file (created automatically on first run)
│  README.md          # This file
│
└─ tests/
   │  __init__.py
   │  test_highscore.py

main modules:
config.py
Contains DifficultySettings dataclass and constants for screen size, colors, difficulty presets, scoring, and file names.
sprites.py
Skier: player-controlled character with skis and simple body graphics.
Obstacle: randomly chosen tree or rock that the player must avoid.
Flag: collectible item that grants additional score.
RescueTarget: a person lying on the slope; colliding with them rescues them, giving a big score bonus and potentially extra lives.
highscore.py
Provides three functions:

load_high_scores(...)

save_high_score(...)

is_new_high_score(...)
This module is responsible only for reading/writing the high-score text file and is unit-tested.

game.py
Implements the Game class and the main state machine:

States: "MENU", "PLAYING", "GAME_OVER".

Handles events, spawning sprites, collisions, scoring, drawing HUD and backgrounds.

Manages difficulty progression and pause functionality.

main.py
Minimal entry point that creates a Game instance and calls game.run().

Installation
Requirements

Python 3.10+ (tested with Python 3.13 on macOS)

pygame

pytest (for running unit tests)

Setup (recommended: virtual environment)
From the project root directory (canadagoose):
python3 -m venv venv
source venv/bin/activate             # On macOS / Linux
# venv\Scripts\activate              # On Windows

pip install pygame pytest


How to Run the Game
From the project root (with the virtual environment activated):
python3 main.py

A Pygame window titled "Ski Patrol Adventure" should appear.
Controls
Menu:


1 – Start game on Easy


2 – Start game on Medium


3 – Start game on Hard


ESC – Quit the game / close the window


In-game:


← / → or A / D – Move the skier left/right


Avoid trees and rocks (obstacles)


Collect yellow flags to gain points


Rescue red-jacket rescue targets lying in the snow to gain a large score bonus and possibly extra lives


P – Pause / resume the game


ESC – Return to main menu


Game Over:


R – Restart the game with the same difficulty


M – Return to main menu


ESC – Quit the game



Gameplay Details


The skier automatically moves “down” the mountain as the background scrolls upward.


Obstacles (Obstacle sprites):


Trees (green) and rocks (gray) spawn above the screen and move downward.


Colliding with an obstacle reduces the player’s lives.




Flags (Flag sprites):


Collect flags to gain additional score.




Rescue targets (RescueTarget sprites):


People stuck in the snow. Colliding with them:


Adds a large score bonus (POINTS_PER_RESCUE).


Increases your lives by RESCUE_LIFE_BONUS up to MAX_LIVES.






Difficulty progression:


Every DIFFICULTY_SCALE_INTERVAL_SECONDS seconds, the scroll speed increases slightly and the spawn rates for obstacles, flags, and rescue targets become more aggressive.




Score and lives:


Score increases over time and from collecting items/rescuing people.


Once lives reach zero, the game transitions to the Game Over screen.




High scores:


When a game ends, the final score is compared to existing scores stored in highscores.txt.


If it is a new high score, a “New high score!” message is shown on the Game Over screen.


The high-score file keeps only the top few scores.





Running the Tests
To run the unit tests:
pytest

This will run tests from tests/test_highscore.py, which verify:


Loading high scores from a file that does not exist.


Sorting and truncating saved scores.


The behavior of is_new_high_score.



Design Notes
Some design choices made for this project:


Object-oriented Pygame design:
Sprites and the main game loop are encapsulated in classes instead of being written in a single script. This matches the course emphasis on object-oriented programming and clean code organization.FinalProject_Handout_revised FA…


Config-driven tuning:
Game parameters such as speeds, spawn rates, scoring, and colors are all defined in config.py, making it easy to tweak difficulty or look-and-feel without changing the game logic.final project proposal


Separation of concerns:


sprites.py focuses only on visual representation and movement of objects.


game.py handles high-level state and interaction logic.


highscore.py is responsible only for file I/O and is unit-tested.


main.py is a minimal entry point.




Limitations:


Graphics are simple 2D shapes drawn with Pygame surfaces instead of imported image assets.


There is no sound or music yet.





Possible Future Improvements
If we had more time, we would consider:


Replacing drawn shapes with real sprite images and adding sprite animations.


Adding sound effects and background music (collisions, flag collection, rescue, etc.).


Implementing additional game modes (e.g., time attack, endless mode with increasing slope angle).


Adding an options menu (volume, key bindings, more difficulty presets).


More advanced scoring mechanics such as combos or streaks.



External Resources and Acknowledgements


We were inspired by the article
“Build epic PyGame – Skiing Adventure” on GeeksforGeeks, which demonstrates how to create a skiing game in Pygame and discusses obstacles and flag collection on a snowy slope. We used this tutorial for conceptual guidance, but wrote our own code and structure for this project.GeeksforGeeks


We used ChatGPT (OpenAI GPT-5.1 Pro) to help brainstorm game design ideas, suggest code organization patterns (multi-file structure, class design, and configuration module), and assist in debugging. All final code was reviewed and integrated by the project team, and we adjusted it to match the requirements of EN.540.635 and our own preferences.FinalProject_Handout_revised FA…


All other code in this repository was written specifically for this project.


