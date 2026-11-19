"""Contract tests for the TestBench manifest's private-evidence pin set.

The regression suite sandboxes HOME, so every fixture a test reads through
an environment variable must be pinned to an absolute host path there;
anything unpinned silently resolves inside the sandbox and skips. These
tests keep the pin set complete so new fixture variables cannot drift into
silent skips. Deterministic: no environment or private artifact access.
"""
import ast
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


def _is_os_environ(node):
    return (isinstance(node, ast.Attribute) and node.attr == "environ"
            and isinstance(node.value, ast.Name) and node.value.id == "os")


def _first_str_arg(node):
    if node.args and isinstance(node.args[0], ast.Constant):
        value = node.args[0].value
        if isinstance(value, str) and value.startswith("WGRD_"):
            return value
    return None


def consumed_vars(tests_dir):
    """WGRD_* vars read via os.environ.get / os.getenv / os.environ[...].

    AST-based on purpose: string literals and comments (including this
    module's own negative-control samples) are not reads.
    """
    used = set()
    for path in sorted(Path(tests_dir).glob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if (isinstance(func, ast.Attribute) and func.attr == "get"
                        and _is_os_environ(func.value)):
                    name = _first_str_arg(node)
                    if name:
                        used.add(name)
                elif (isinstance(func, ast.Attribute) and func.attr == "getenv"
                        and isinstance(func.value, ast.Name)
                        and func.value.id == "os"):
                    name = _first_str_arg(node)
                    if name:
                        used.add(name)
            elif isinstance(node, ast.Subscript) and _is_os_environ(node.value):
                sl = node.slice
                if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
                    if sl.value.startswith("WGRD_"):
                        used.add(sl.value)
    return used


def missing_pins(used, overrides):
    return sorted(v for v in used if v not in overrides)


def suite_overrides(manifest, name):
    for suite in manifest.get("suite", []):
        if suite.get("name") == name:
            return suite.get("env_overrides", {})
    raise AssertionError(f"suite {name!r} not found in .testbench.toml")


class RegressionPinCompleteness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = tomllib.loads((ROOT / ".testbench.toml").read_text())
        cls.used = consumed_vars(ROOT / "tests")
        cls.overrides = suite_overrides(cls.manifest, "private-evidence-regression")

    def test_every_consumed_fixture_var_is_pinned(self):
        missing = missing_pins(self.used, self.overrides)
        self.assertEqual(
            missing, [],
            "regression suite must pin every WGRD_* fixture var consumed by "
            f"tests; unpinned vars skip silently in the sandbox: {missing}")

    def test_pins_are_absolute_host_paths(self):
        # env_overrides values are literal strings: no ~ expansion happens.
        for var, value in self.overrides.items():
            if var.startswith("WGRD_"):
                self.assertTrue(
                    value.startswith("/"),
                    f"{var} must be an absolute path, got {value!r}")

    def test_offline_unit_suite_pins_the_public_fixture(self):
        # test_unit_data fetches from the network when WGRD_UNIT_DATA is
        # unset; the offline suite must never trigger that.
        overrides = suite_overrides(self.manifest, "offline-unit")
        self.assertIn("WGRD_UNIT_DATA", overrides)
        self.assertTrue(overrides["WGRD_UNIT_DATA"].startswith("/"))


class NegativeControls(unittest.TestCase):
    def test_missing_pin_is_reported(self):
        used = {"WGRD_A", "WGRD_B"}
        self.assertEqual(missing_pins(used, {"WGRD_A": "/x"}), ["WGRD_B"])

    def test_complete_pin_set_reports_nothing(self):
        used = {"WGRD_A", "WGRD_B"}
        self.assertEqual(
            missing_pins(used, {"WGRD_A": "/x", "WGRD_B": "/y"}), [])

    def test_consumer_extraction_finds_all_read_forms(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test_sample.py"
            p.write_text(
                'a = os.environ.get("WGRD_GET", "d")\n'
                'b = os.environ["WGRD_INDEX"]\n'
                'c = os.getenv("WGRD_GETENV")\n')
            found = consumed_vars(tmp)
        self.assertEqual(found, {"WGRD_GET", "WGRD_INDEX", "WGRD_GETENV"})


if __name__ == "__main__":
    unittest.main()