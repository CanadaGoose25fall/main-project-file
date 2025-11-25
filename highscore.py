"""Utility functions for loading and saving high scores to a text file."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from config import HIGH_SCORE_FILE


DEFAULT_HIGH_SCORE_PATH = Path(HIGH_SCORE_FILE)


def load_high_scores(limit: int = 5, path: Optional[Path] = None) -> List[int]:
    """Load high scores from a text file.

    The file is expected to contain one integer score per line.

    Args:
        limit: Maximum number of scores to return.
        path: Optional path override for unit testing.

    Returns:
        A list of scores sorted from highest to lowest.
    """
    used_path = path or DEFAULT_HIGH_SCORE_PATH
    if not used_path.exists():
        return []
    scores: List[int] = []
    try:
        with used_path.open("r", encoding="utf-8") as file:
            for line in file:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    value = int(stripped)
                except ValueError:
                    continue
                scores.append(value)
    except OSError:
        return []

    scores.sort(reverse=True)
    return scores[:limit]


def save_high_score(score: int, limit: int = 5, path: Optional[Path] = None) -> None:
    """Append a new score to the high-score file and keep only the best ones.

    Args:
        score: The score to store.
        limit: Maximum number of scores to keep.
        path: Optional path override for unit testing.
    """
    used_path = path or DEFAULT_HIGH_SCORE_PATH
    scores = load_high_scores(limit=limit, path=used_path)
    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:limit]

    try:
        used_path.parent.mkdir(parents=True, exist_ok=True)
        with used_path.open("w", encoding="utf-8") as file:
            for value in scores:
                file.write(f"{value}\n")
    except OSError:
        # Failing to write high scores should not crash the game.
        return


def is_new_high_score(score: int, path: Optional[Path] = None) -> bool:
    """Check whether the given score is higher than existing stored scores.

    Args:
        score: Score to compare.
        path: Optional path override for unit testing.

    Returns:
        True if the score is a new high score or if no scores are stored yet.
    """
    scores = load_high_scores(path=path)
    if not scores:
        return True
    return score > max(scores)
