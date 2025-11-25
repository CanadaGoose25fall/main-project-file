"""Entry point for running the Ski Patrol Adventure game."""

from game import Game


def main() -> None:
    """Create a Game instance and start the main loop."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
