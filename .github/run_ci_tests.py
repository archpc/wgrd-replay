"""Run discovery on public CI; explicitly report tests requiring private replays.

The ordinary full-suite command remains strict about missing samples. This runner
skips only the known legacy tests that do not provide their own missing-file guard.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

PRIVATE_CLASSES = {
    'test_entities.AuthenticEntityCatalog',
    'test_orders.AuthenticOrders',
    'test_timeline.AuthenticTimeline',
    'test_wgrd_replay.Malformed',
    'test_wgrd_replay.RealSamples',
}
PRIVATE_METHODS = {
    'test_wgrd_replay.CommandBlocks.test_authentic_multi_blocks_reassemble_and_opaque_is_not_decoded',
    'test_wgrd_replay.CommandBlocks.test_authentic_op07_boundaries',
    'test_wgrd_replay.CommandBlocks.test_authentic_op09_boundaries',
}


def cases(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from cases(item)
        else:
            yield item


def main():
    discovered = list(cases(unittest.defaultTestLoader.discover('tests')))
    excluded = [test for test in discovered if test.id() in PRIVATE_METHODS
                or test.id().rsplit('.', 1)[0] in PRIVATE_CLASSES]
    matched_classes = {test.id().rsplit('.', 1)[0] for test in excluded}
    matched_methods = {test.id() for test in excluded} & PRIVATE_METHODS
    if not PRIVATE_CLASSES <= matched_classes or matched_methods != PRIVATE_METHODS:
        print('CI private-test exclusions are stale; review .github/run_ci_tests.py', file=sys.stderr)
        return 1
    excluded_ids = {test.id() for test in excluded}
    print('Private replay tests excluded from CI (run the full suite with artifacts):', flush=True)
    for test in excluded:
        print('  ' + test.id(), flush=True)
    selected = unittest.TestSuite(test for test in discovered if test.id() not in excluded_ids)
    result = unittest.TextTestRunner(verbosity=2).run(selected)
    print('Excluded private replay tests: {}'.format(len(excluded)))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
