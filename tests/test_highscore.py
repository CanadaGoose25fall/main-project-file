"""Simple unit tests for the high-score helper functions."""

from pathlib import Path

from highscore import load_high_scores, save_high_score, is_new_high_score


def test_empty_file_returns_empty_list(tmp_path) -> None:
    """When the scores file does not exist, load_high_scores should return an empty list."""
    path = tmp_path / "scores.txt"
    scores = load_high_scores(path=path)
    assert scores == []


def test_save_and_load_scores_sorted(tmp_path) -> None:
    """Scores saved through save_high_score should be stored in descending order."""
    path = tmp_path / "scores.txt"

    save_high_score(50, path=path)
    save_high_score(10, path=path)
    save_high_score(100, path=path)

    scores = load_high_scores(limit=3, path=path)
    assert scores == [100, 50, 10]


def test_is_new_high_score(tmp_path) -> None:
    """is_new_high_score should detect whether a score beats existing values."""
    path = tmp_path / "scores.txt"
    save_high_score(30, path=path)
    save_high_score(60, path=path)

    assert is_new_high_score(100, path=path) is True
    assert is_new_high_score(10, path=path) is False
