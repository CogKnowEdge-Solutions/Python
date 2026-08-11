"""End-to-end tests for lab-safe-resource-vault.ipynb.

The notebook is executed top-to-bottom in a fresh kernel via testbook; tests
then assert on real kernel state and cell output. The first-cell `!pip install`
is stripped so the run is hermetic and offline.

Run from the lab folder::

    pip install pytest testbook ipykernel
    pytest test_safe_resource_vault.py -q
"""

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from testbook import testbook

NOTEBOOK = "lab-safe-resource-vault.ipynb"


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


class TestWarmUpFile:
    def test_file_closed_after_with_block(self, executed_nb):
        text = output_of(executed_nb, "vault_notes.txt")
        assert "After the with block, is the file closed? True" in text

    def test_notes_file_was_written(self, executed_nb):
        from pathlib import Path
        text = Path("vault_notes.txt").read_text(encoding="utf-8")
        assert "always closes what it opens" in text


class TestWarmUpProtocol:
    def test_protocol_runs_on_entry_and_exit(self, executed_nb):
        text = output_of(executed_nb, "class TinyVault")
        assert "entering" in text
        assert "inside the block" in text
        assert "exiting" in text

    def test_exit_runs_after_the_block(self, executed_nb):
        text = output_of(executed_nb, "class TinyVault")
        assert text.index("entering") < text.index("inside the block") < text.index("exiting")


class TestPart1ClassBased:
    def test_connection_closed_after_normal_block(self, executed_nb):
        text = output_of(executed_nb, "class DatabaseConnection")
        assert "Opening users connection..." in text
        assert "Running a query inside the block..." in text
        assert "Closing users connection..." in text
        assert text.index("Opening users") < text.index("Running a query") < text.index("Closing users")

    def test_connection_closed_after_crash(self, executed_nb):
        text = output_of(executed_nb, 'raise ValueError("query timed out mid-request")')
        assert "Opening users connection..." in text
        assert "Closing users connection..." in text
        assert "Caught outside the block: query timed out mid-request" in text

    def test_cleanup_happens_before_error_surfaces(self, executed_nb):
        text = output_of(executed_nb, 'raise ValueError("query timed out mid-request")')
        assert text.index("Closing users connection...") < text.index("Caught outside")


class TestPart2Contextmanager:
    def test_decorator_runs_open_and_close(self, executed_nb):
        text = output_of(executed_nb, 'raise RuntimeError("replica went offline")')
        assert "Opening orders connection..." in text
        assert "Closing orders connection..." in text
        assert "Caught outside the block: replica went offline" in text


class TestPart3Transaction:
    def test_commit_keeps_statements(self, executed_nb):
        text = output_of(executed_nb, 'INSERT INTO payments VALUES (1, 49.99)')
        assert "Transaction log stored: ['INSERT INTO payments VALUES (1, 49.99)', " \
               "'UPDATE accounts SET balance = balance - 49.99 WHERE id = 7']" in text

    def test_commit_message_printed(self, executed_nb):
        text = output_of(executed_nb, 'transaction.execute("INSERT INTO payments VALUES (1, 49.99)")')
        assert "BEGIN transaction" in text
        assert "COMMIT 2 statement(s)" in text

    def test_rollback_discards_statements(self, executed_nb):
        text = output_of(executed_nb, 'raise RuntimeError("payment gateway timed out")')
        assert "ROLLBACK 1 statement(s)" in text
        assert "Statements kept after rollback: []" in text

    def test_rollback_message_printed_and_error_raised(self, executed_nb):
        text = output_of(executed_nb, 'raise RuntimeError("payment gateway timed out")')
        assert "ROLLBACK 1 statement(s)" in text
        assert "Caught outside the block: payment gateway timed out" in text
        assert "Statements kept after rollback: []" in text


class TestLedger:
    def test_ledger_has_five_rows(self, executed_nb):
        assert len(executed_nb.ref("ledger")) == 5

    def test_ledger_outcomes(self, executed_nb):
        outcomes = [row[2] for row in executed_nb.ref("ledger")]
        assert outcomes == ["closed", "closed, error surfaced", "closed", "committed", "rolled back"]

    def test_ledger_table_prints_grid(self, executed_nb):
        text = output_of(executed_nb, "tabulate(ledger")
        assert "Resource" in text and "Action" in text and "Outcome" in text
        assert text.count("| vault_notes.txt") == 1
        assert text.count("| payments transaction") == 2
        assert "committed" in text and "rolled back" in text


class TestEnvironmentAndConfig:
    def test_tabulate_pinned_version(self):
        import tabulate
        assert tabulate.__version__ == "0.10.0"

    def test_line_ceiling_respected(self):
        import nbformat
        nb = nbformat.read(NOTEBOOK, as_version=4)
        code_lines = sum(len(c.source.splitlines()) for c in nb.cells
                         if c.cell_type == "code")
        assert code_lines <= 110

    def test_first_code_cell_is_pip_install(self):
        import nbformat
        nb = nbformat.read(NOTEBOOK, as_version=4)
        first_code = next(c for c in nb.cells if c.cell_type == "code")
        assert first_code.source.strip().startswith("!pip install")
        assert "tabulate==0.10.0" in first_code.source

    def test_no_credential_patterns_in_shipped_files(self):
        from pathlib import Path

        for filename in (
            NOTEBOOK,
            "lab-safe-resource-vault.md",
            "lab-safe-resource-vault-assignment.md",
        ):
            text = Path(filename).read_text(encoding="utf-8")
            for pattern in ("sk-", "api_key", "apiKey", "password", "Bearer "):
                assert pattern not in text
