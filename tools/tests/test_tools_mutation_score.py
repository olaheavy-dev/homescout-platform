"""Tests for tools/mutation_score.py (port step P7, decision 0049 item 11b)."""

import json
from pathlib import Path

import mutation_score
import pytest


def _stats(**overrides: int) -> dict[str, int]:
    base = {
        "killed": 0,
        "survived": 0,
        "total": 0,
        "no_tests": 0,
        "skipped": 0,
        "suspicious": 0,
        "timeout": 0,
        "check_was_interrupted_by_user": 0,
        "segfault": 0,
    }
    base.update(overrides)
    return base


def _write(tmp_path: Path, stats: dict[str, int]) -> Path:
    path = tmp_path / "mutmut-cicd-stats.json"
    path.write_text(json.dumps(stats), encoding="utf-8")
    return path


def test_score_killed_and_survived_returns_killed_share() -> None:
    assert mutation_score.score(_stats(killed=90, survived=10)) == pytest.approx(90.0)


def test_score_timeout_counts_as_detected() -> None:
    assert mutation_score.score(_stats(killed=8, timeout=2, survived=10)) == pytest.approx(50.0)


def test_score_suspicious_no_tests_and_segfault_count_as_not_detected() -> None:
    stats = _stats(killed=6, suspicious=1, no_tests=1, segfault=2)
    assert mutation_score.score(stats) == pytest.approx(60.0)


def test_score_skipped_is_left_out() -> None:
    assert mutation_score.score(_stats(killed=1, skipped=5)) == pytest.approx(100.0)


def test_score_no_mutants_returns_none() -> None:
    assert mutation_score.score(_stats(skipped=3)) is None


def test_main_at_break_score_passes(tmp_path: Path) -> None:
    path = _write(tmp_path, _stats(killed=90, survived=10))
    assert mutation_score.main([str(path), "--break-score", "90"]) == 0


def test_main_below_break_score_fails(tmp_path: Path) -> None:
    path = _write(tmp_path, _stats(killed=89, survived=11))
    assert mutation_score.main([str(path), "--break-score", "90"]) == 1


def test_main_no_mutants_fails(tmp_path: Path) -> None:
    path = _write(tmp_path, _stats())
    assert mutation_score.main([str(path), "--break-score", "0"]) == 1


def test_main_interrupted_run_fails_even_with_a_high_score(tmp_path: Path) -> None:
    path = _write(tmp_path, _stats(killed=10, check_was_interrupted_by_user=1))
    assert mutation_score.main([str(path), "--break-score", "50"]) == 1


def test_main_missing_file_fails(tmp_path: Path) -> None:
    assert mutation_score.main([str(tmp_path / "absent.json"), "--break-score", "50"]) == 1


def test_main_prints_the_numbers(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = _write(tmp_path, _stats(killed=7, timeout=1, survived=2))
    mutation_score.main([str(path), "--break-score", "50"])
    out = capsys.readouterr().out
    assert "killed 7" in out
    assert "timeout 1" in out
    assert "survived 2" in out
    assert "80.00%" in out
    assert "break score 50.00%" in out
