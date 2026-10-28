"""Compatibility entry point: full discovery, with absence guards in the tests.

Prefer: PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
No class/method exclusions. Present private artifacts execute normally.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main():
    suite = unittest.defaultTestLoader.discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
