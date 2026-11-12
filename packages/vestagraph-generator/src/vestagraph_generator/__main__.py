"""Command line: ``python -m vestagraph_generator [repo-root]`` (ported from the C# ``Program.cs``).

Writes ``packages/fixtures/generated/costs.json`` from ``packages/fixtures/data``. Exits 0 on
success, 1 when the cost engine reports a problem (its error code is printed, nothing is
written), and 2 when a data file is missing or cannot be understood.
"""

import sys
from pathlib import Path
from typing import TextIO

from vestagraph_generator.costs_generator import FILE_NAME, run
from vestagraph_generator.fixture_reader import InvalidDataError


def find_repository_root(start: Path) -> Path:
    """The nearest folder at or above ``start`` that holds ``packages/fixtures/data``."""
    for folder in (start.resolve(), *start.resolve().parents):
        if (folder / "packages" / "fixtures" / "data").is_dir():
            return folder
    message = f"packages/fixtures/data not found above {start}."
    raise FileNotFoundError(message)


def main(argv: list[str], stdout: TextIO, stderr: TextIO, cwd: Path) -> int:
    """Run the generator; ``argv`` is the command line without the program name."""
    try:
        root = Path(argv[0]).resolve() if argv else find_repository_root(cwd)
        fixtures = root / "packages" / "fixtures"
        exit_code = run(fixtures, stderr)
    except (OSError, InvalidDataError) as exception:
        stderr.write(f"Generator could not run: {exception}\n")
        return 2
    if exit_code == 0:
        stdout.write(f"Generated {fixtures / 'generated' / FILE_NAME}\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], sys.stdout, sys.stderr, Path.cwd()))
