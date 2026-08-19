"""End-to-end tests for lab-metaprogramming-toolkit.ipynb.

The notebook is executed top-to-bottom in a fresh kernel via testbook; tests
then assert on real kernel state and cell output. The first-cell `!pip install`
is stripped so the run is hermetic and offline.

Run from the lab folder::

    pip install pytest testbook ipykernel tabulate
    pytest test_metaprogramming_toolkit.py -q
"""

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from testbook import testbook

NOTEBOOK = "lab-metaprogramming-toolkit.ipynb"


@pytest.fixture(scope="module")
def executed_nb():
    with testbook(NOTEBOOK, execute=False) as tb:
        tb.nb.cells = [
            cell for cell in tb.nb.cells
            if not (cell.cell_type == "code" and cell.source.strip().startswith("!"))
        ]
        tb.execute()
        yield tb


def output_of(executed_nb, needle):
    index = next(i for i, cell in enumerate(executed_nb.cells)
                 if cell.cell_type == "code" and needle in cell.source)
    return executed_nb.cell_output_text(index)


class TestWarmUp:
    def test_wrapper_transforms_result(self, executed_nb):
        text = output_of(executed_nb, "def shout(func):")
        assert "HELLO TEAM!" in text

    def test_naive_wrapper_loses_name(self, executed_nb):
        text = output_of(executed_nb, "def shout(func):")
        assert "function name is now: wrapper" in text


class TestTimer:
    def test_prints_elapsed_time(self, executed_nb):
        text = output_of(executed_nb, "def timer(func):")
        assert "ran in " in text
        assert "s" in text.split("ran in ")[1]

    def test_primes_count(self, executed_nb):
        text = output_of(executed_nb, "def timer(func):")
        assert "primes found: 303" in text
        assert executed_nb.ref("len(primes)") == 303

    def test_wraps_preserves_name(self, executed_nb):
        assert executed_nb.ref("find_primes.__name__") == "find_primes"


class TestAuthenticate:
    def test_admin_allowed(self, executed_nb):
        text = output_of(executed_nb, "def authenticate(role):")
        assert "Deleted user 7" in text

    def test_viewer_denied(self, executed_nb):
        text = output_of(executed_nb, "def authenticate(role):")
        assert "Denied: alice needs role 'admin'" in text

    def test_role_changed_in_shared_state(self, executed_nb):
        assert executed_nb.ref("current_user['role']") == "viewer"

    def test_wraps_preserves_name(self, executed_nb):
        assert executed_nb.ref("delete_user.__name__") == "delete_user"


class TestRetry:
    def test_retries_then_succeeds(self, executed_nb):
        text = output_of(executed_nb, "def retry(max_attempts=3):")
        assert "Attempt 1 failed: gateway timed out" in text
        assert "Attempt 2 failed: gateway timed out" in text
        assert "['order A', 'order B']" in text

    def test_gives_up_after_budget(self, executed_nb):
        text = output_of(executed_nb, "def retry(max_attempts=3):")
        assert text.count("Attempt") >= 5
        assert "giving up after 3 attempts: gateway timed out" in text

    def test_wraps_preserves_name(self, executed_nb):
        assert executed_nb.ref("fetch_orders.__name__") == "fetch_orders"


class TestCache:
    def test_computes_once_reuses_hit(self, executed_nb):
        text = output_of(executed_nb, "def cache(func):")
        assert text.count("computing expensive ...") == 2
        assert text.count("100") == 2

    def test_new_argument_computes_again(self, executed_nb):
        text = output_of(executed_nb, "def cache(func):")
        assert "144" in text

    def test_wraps_preserves_name(self, executed_nb):
        assert executed_nb.ref("expensive.__name__") == "expensive"


class TestAssignmentExercises:
    def test_optional_exercise_kwargs_cache_key(self):
        import functools

        def cache(func):
            store = {}

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (args, frozenset(kwargs.items()))
                if key not in store:
                    store[key] = func(*args, **kwargs)
                return store[key]

            return wrapper

        runs = []

        @cache
        def expensive(n, debug=False):
            runs.append((n, debug))
            return n ** 2

        assert expensive(10) == 100
        assert expensive(10, debug=True) == 100
        assert expensive(10) == 100
        assert runs == [(10, False), (10, True)]

    def test_log_decorator_solution(self):
        import functools

        def log(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"calling {func.__name__}")
                result = func(*args, **kwargs)
                print(f"finished {func.__name__}")
                return result

            return wrapper

        @log
        def greet(name):
            return f"hello {name}"

        assert greet.__name__ == "greet"
        assert greet("team") == "hello team"


class TestEnvironmentAndConfig:
    def test_tabulate_pinned_version(self):
        import tabulate
        assert tabulate.__version__ == "0.10.0"

    def test_line_ceiling_respected(self):
        import nbformat
        nb = nbformat.read(NOTEBOOK, as_version=4)
        code_lines = sum(len(c.source.splitlines()) for c in nb.cells
                         if c.cell_type == "code")
        assert code_lines <= 150

    def test_first_code_cell_is_pip_install(self):
        import nbformat
        nb = nbformat.read(NOTEBOOK, as_version=4)
        first_code = next(c for c in nb.cells if c.cell_type == "code")
        assert first_code.source.strip().startswith("!pip install")
        assert "tabulate==0.10.0" in first_code.source
