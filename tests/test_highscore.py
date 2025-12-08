"""Simple unit tests for the high-score helper functions."""

import sys
from pathlib import Path
from highscore import load_high_score, save_high_score, is_new_high_score

# Add parent directory to path so we can import highscore module
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))


def test_empty_file_returns_zero(tmp_path) -> None:
    """
    When the scores file does not exist, load_high_score should return 0.
    
    paramerer:
    tmp_path: pytest fixture that provides a temporary directory
    
    returns: None
    """
    path = tmp_path / "score.txt"
    score = load_high_score(path=path)
    assert score == 0


def test_save_and_load_score(tmp_path) -> None:
    """
    A saved score should be retrievable.
    
    paramerer:
    tmp_path: pytest fixture that provides a temporary directory
    
    returns: None
    """
    path = tmp_path / "score.txt"

    save_high_score(100, path=path)
    score = load_high_score(path=path)
    assert score == 100


def test_only_saves_higher_score(tmp_path) -> None:
    """
    Only higher scores should be saved.
    
    paramerer:
    tmp_path: pytest fixture that provides a temporary directory
    
    returns: None
    """
    path = tmp_path / "score.txt"

    save_high_score(100, path=path)
    save_high_score(50, path=path)  
    
    score = load_high_score(path=path)
    assert score == 100  

    save_high_score(200, path=path)  
    score = load_high_score(path=path)
    assert score == 200


def test_is_new_high_score(tmp_path) -> None:
    """
    is_new_high_score should detect whether a score beats the existing high score.
    paramerer:
    tmp_path: pytest fixture that provides a temporary directory
    returns: None
    """
    path = tmp_path / "score.txt"
    
    # No existing score, any score is a high score
    assert is_new_high_score(10, path=path) is True
    
    save_high_score(100, path=path)
    
    assert is_new_high_score(200, path=path) is True
    assert is_new_high_score(50, path=path) is False
    assert is_new_high_score(100, path=path) is False  
    assert is_new_high_score(101, path=path) is True  
    assert is_new_high_score(10, path=path) is False
