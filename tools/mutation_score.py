"""Pass mark for mutmut (decision 0049 item 11b, port step P7).

mutmut 3.8.1 has no pass mark of its own. `mutmut export-cicd-stats` writes the counts to
mutants/mutmut-cicd-stats.json; this script reads that file, prints the numbers and exits 1 when
the score is below the break score.

Score = (killed + timeout) / (killed + timeout + survived + suspicious + no_tests + segfault).
A timeout counts as detected, because a mutant that makes the code hang was noticed. A suspicious
mutant, one with no covering test or a crashed run is counted as not detected. Skipped mutants
are left out. A run with no scored mutants, one the user interrupted, or one where the listed
counts do not add up to `total` (some mutants not checked) fails.
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_STATS_PATH = "mutants/mutmut-cicd-stats.json"


def _say(message: str) -> None:
    sys.stdout.write(message + "\n")


def score(stats: dict[str, int]) -> float | None:
    """Percentage of scored mutants that were detected, or None when none were scored."""
    detected = stats["killed"] + stats["timeout"]
    scored = (
        detected + stats["survived"] + stats["suspicious"] + stats["no_tests"] + stats["segfault"]
    )
    if scored == 0:
        return None
    return detected * 100 / scored


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Fail when the mutmut score is below the break score."
    )
    parser.add_argument("stats_path", nargs="?", default=DEFAULT_STATS_PATH)
    parser.add_argument("--break-score", type=float, required=True)
    args = parser.parse_args(argv)

    path = Path(args.stats_path)
    if not path.is_file():
        _say(f"No mutmut statistics at {path}: run 'mutmut run' first.")
        return 1
    stats: dict[str, int] = json.loads(path.read_text(encoding="utf-8"))

    counts = ", ".join(
        f"{label} {stats[key]}"
        for label, key in (
            ("killed", "killed"),
            ("timeout", "timeout"),
            ("survived", "survived"),
            ("suspicious", "suspicious"),
            ("no tests", "no_tests"),
            ("segfault", "segfault"),
            ("skipped", "skipped"),
        )
    )
    _say(f"mutmut: {counts}")
    if stats["check_was_interrupted_by_user"]:
        _say("The run was interrupted: the score is not complete.")
        return 1
    listed = sum(
        stats[key]
        for key in (
            "killed",
            "timeout",
            "survived",
            "suspicious",
            "no_tests",
            "segfault",
            "skipped",
        )
    )
    if listed != stats["total"]:
        _say(
            f"The run is incomplete: {stats['total']} mutants in total but only {listed} have a "
            "verdict listed (the rest were not checked or were caught by the type checker)."
        )
        return 1
    result = score(stats)
    if result is None:
        _say("No mutants were scored: the run found nothing to mutate or nothing ran.")
        return 1
    _say(f"Mutation score {result:.2f}% (break score {args.break_score:.2f}%)")
    if result < args.break_score:
        _say("Below the break score.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
