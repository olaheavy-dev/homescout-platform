"""Command line: ``python -m vestagraph_fixture_validator [repo-root]``.

Ported from the C# ``Program.cs``.

Checks every file in ``packages/fixtures/data``, ``test-cases`` and ``generated`` against its JSON
Schema. Exits 0 when every file is valid, 1 when something is wrong (each problem is printed on
standard error), and 2 on a setup error (the repository cannot be found).
"""

import sys
from pathlib import Path
from typing import TextIO

from vestagraph_fixture_validator.validator import find_repository_root, validate_fixtures


def main(argv: list[str], stdout: TextIO, stderr: TextIO, cwd: Path) -> int:
    """Run the validator; ``argv`` is the command line without the program name."""
    try:
        root = Path(argv[0]).resolve() if argv else find_repository_root(cwd)
    except FileNotFoundError as exception:
        stderr.write(f"{exception}\n")
        return 2

    problems = validate_fixtures(root / "packages" / "fixtures")
    if not problems:
        stdout.write(
            "Fixtures: every data file, test case and generated file matches its schema.\n"
        )
        return 0

    for problem in problems:
        stderr.write(f"{problem}\n")
    stderr.write(f"Fixtures: {len(problems)} problem(s) found.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], sys.stdout, sys.stderr, Path.cwd()))
