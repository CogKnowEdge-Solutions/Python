"""End-to-end tests for lab-memory-efficient-data-pipeline.ipynb.

The notebook is executed top-to-bottom in a fresh kernel via testbook; tests
then assert on real kernel state and cell output. The first-cell `!pip install`
is stripped so the run is hermetic and offline.

Run from the lab folder::

    pip install pytest testbook ipykernel tabulate
    pytest test_memory_efficient_data_pipeline.py -q
"""

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from testbook import testbook

NOTEBOOK = "lab-memory-efficient-data-pipeline.ipynb"


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


class TestWarmUpProtocol:
    def test_next_unpacks_values(self, executed_nb):
        text = output_of(executed_nb, "numbers = iter([10, 20, 30])")
        assert "10\n20\n30\n" in text

    def test_stop_iteration_raised_at_end(self, executed_nb):
        text = output_of(executed_nb, "numbers = iter([10, 20, 30])")
        assert "StopIteration - the iterator is exhausted" in text


class TestDataGeneration:
    def test_log_file_written(self, executed_nb):
        from pathlib import Path
        assert Path("data/server.log").exists()
        assert Path("data/server.log").stat().st_size > 5_000_000

    def test_log_line_format(self, executed_nb):
        from pathlib import Path
        first = Path("data/server.log").read_text(encoding="utf-8").splitlines()[0]
        parts = first.split()
        assert len(parts) == 5
        assert parts[2] in ("GET", "POST")
        assert parts[4] in ("200", "404", "500")


class TestNaiveBaseline:
    def test_lines_count(self, executed_nb):
        assert executed_nb.ref("len(lines_list)") == 140610

    def test_list_uses_significant_memory(self, executed_nb):
        assert executed_nb.ref("sys.getsizeof(lines_list)") > 1_000_000


class TestPart1ClassIterator:
    def test_class_total_matches_naive(self, executed_nb):
        assert executed_nb.ref("total_class") == 140610

    def test_class_error_count(self, executed_nb):
        assert executed_nb.ref("errors_class") == 28321


class TestPart2Generator:
    def test_generator_total_matches(self, executed_nb):
        assert executed_nb.ref("total_gen") == 140610

    def test_generator_errors_match_class(self, executed_nb):
        assert executed_nb.ref("errors_gen") == executed_nb.ref("errors_class")

    def test_verify_print_says_true(self, executed_nb):
        text = output_of(executed_nb, "Totals match:")
        assert "Totals match: True" in text


class TestSpikes:
    def test_busiest_second_found(self, executed_nb):
        text = output_of(executed_nb, "Busiest second:")
        assert "('2026-08-09 00:13:38', 500)" in text

    def test_spike_count(self, executed_nb):
        text = output_of(executed_nb, "n_spikes")
        assert "Seconds with > 100 requests: 76" in text


class TestMemoryPayoff:
    def test_generator_far_smaller_than_list(self, executed_nb):
        text = output_of(executed_nb, "Ratio:")
        assert "readlines() list object:" in text
        assert "generator object:" in text
        assert "Ratio:" in text
        ratio = float(text.split("Ratio:")[1].split("x")[0].strip())
        assert ratio > 1000


class TestResultsTable:
    def test_table_lists_all_three_readers(self, executed_nb):
        text = output_of(executed_nb, "tabulate(rows")
        assert "readlines() list" in text
        assert "LogReader class" in text
        assert "read_log_lines generator" in text
        assert "140,610 lines" in text
        assert "1 line at a time" in text


class TestAssignmentExercises:
    def test_challenge_chunk_generator_solution(self):
        import textwrap

        solution = textwrap.dedent(
            """
            def read_log_chunks(path, chunk_size=1000):
                with open(path, encoding="utf-8") as f:
                    while True:
                        lines = []
                        for _ in range(chunk_size):
                            line = f.readline()
                            if not line:
                                break
                            lines.append(line)
                        if not lines:
                            break
                        yield lines

            total = 0
            errors = 0
            for chunk in read_log_chunks("data/server.log"):
                total += len(chunk)
                errors += sum(1 for line in chunk if line.split()[-1] == "500")
            """
        )
        ns = {}
        exec(textwrap.dedent(solution), ns)
        assert ns["total"] == 140610
        assert ns["errors"] == 28321


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
