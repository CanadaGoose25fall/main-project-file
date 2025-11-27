"""Utility functions for loading and saving high score to a text file."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from config import HIGH_SCORE_FILE


DEFAULT_HIGH_SCORE_PATH = Path(HIGH_SCORE_FILE)


def load_high_score(path: Optional[Path] = None) -> int:
    """Load the highest score from a text file.

    Args:
        path: Optional path override for unit testing.

    Returns:
        The highest score, or 0 if no score exists.
    """
    used_path = path or DEFAULT_HIGH_SCORE_PATH
    if not used_path.exists():
        return 0
    
    try:
        with used_path.open("r", encoding="utf-8") as file:
            content = file.read().strip()
            if content:
                try:
                    return int(content)
                except ValueError:
                    return 0
    except OSError:
        return 0
    
    return 0


def save_high_score(score: int, path: Optional[Path] = None) -> None:
    """Save a new high score if it's higher than the existing one.

    Args:
        score: The score to potentially store.
        path: Optional path override for unit testing.
    """
    used_path = path or DEFAULT_HIGH_SCORE_PATH
    current_high = load_high_score(path=used_path)
    
    if score > current_high:
        try:
            used_path.parent.mkdir(parents=True, exist_ok=True)
            with used_path.open("w", encoding="utf-8") as file:
                file.write(f"{score}\n")
        except OSError:
            return


def is_new_high_score(score: int, path: Optional[Path] = None) -> bool:
    """Check whether the given score is higher than the existing high score.

    Args:
        score: Score to compare.
        path: Optional path override for unit testing.

    Returns:
        True if the score is a new high score.
    """
    current_high = load_high_score(path=path)
    return score > current_high
