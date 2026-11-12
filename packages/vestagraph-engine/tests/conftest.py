"""Makes the shared test helper module (engine_support.py) importable by name.

The project runs pytest with ``--import-mode=importlib``, which does not put the test folder on
``sys.path``, so the folder is added here.
"""

import sys
from pathlib import Path

_TESTS = str(Path(__file__).resolve().parent)
if _TESTS not in sys.path:
    sys.path.insert(0, _TESTS)
