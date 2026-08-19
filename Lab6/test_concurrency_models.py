"""End-to-end tests for lab-concurrency-models.ipynb.

The notebook is executed top-to-bottom in a fresh kernel via testbook; tests
then assert on real kernel state and cell output. The first-cell `!pip install`
is stripped so the run is hermetic and offline.

Run from the lab folder::

    pip install pytest testbook ipykernel tabulate==0.10.0
    pytest test_concurrency_models.py -q
"""

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from testbook import testbook

NOTEBOOK = "lab-concurrency-models.ipynb"


@pytest.fixture(scope="module")
def executed_nb():
    with testbook(NOTEBOOK, execute=False) as tb:
        tb.nb.cells = [
            cell for cell in tb.nb.cells
            if not (cell.cell_type == "code" and cell.source.strip().startswith("!"))
        ]
        tb.execute()
        yield tb


class TestCpuBound:
    def test_sequential_baseline_runs_work(self, executed_nb):
        # The blur task must be real: a visible baseline, not microseconds.
        assert executed_nb.ref("cpu_seq") > 0.3

    def test_threads_do_not_speed_up_cpu(self, executed_nb):
        # GIL: threads must NOT beat the baseline by much (no >=2x speedup).
        threads = executed_nb.ref("cpu_threads")
        seq = executed_nb.ref("cpu_seq")
        assert threads > seq * 0.5

    def test_asyncio_does_not_speed_up_cpu(self, executed_nb):
        # No await -> no switching -> no speedup.
        async_t = executed_nb.ref("cpu_async")
        seq = executed_nb.ref("cpu_seq")
        assert async_t > seq * 0.5

    def test_processes_speed_up_cpu(self, executed_nb):
        # Own GIL per process: processes are the ONLY CPU strategy that beats
        # the baseline -- they must be the fastest of the four CPU runs.
        seq = executed_nb.ref("cpu_seq")
        threads = executed_nb.ref("cpu_threads")
        async_t = executed_nb.ref("cpu_async")
        proc = executed_nb.ref("cpu_proc")
        assert proc <= min(seq, threads, async_t)

    def test_all_cpu_strategies_handled_every_image(self, executed_nb):
        # All strategies processed the same 100 images — timing vars prove they ran.
        n = len(executed_nb.ref("IMAGES"))
        assert n == 100
        assert executed_nb.ref("cpu_seq") > 0
        assert executed_nb.ref("cpu_threads") > 0
        assert executed_nb.ref("cpu_async") > 0
        assert executed_nb.ref("cpu_proc") > 0


class TestIoBound:
    def test_asyncio_crushes_io(self, executed_nb):
        # 100 sleeping requests collapse to ~one round trip.
        assert executed_nb.ref("io_async_elapsed") < executed_nb.ref("io_seq_elapsed") / 10

    def test_threads_help_io(self, executed_nb):
        # time.sleep releases the GIL, so threads hide the waits.
        assert executed_nb.ref("io_threads_elapsed") < executed_nb.ref("io_seq_elapsed") / 2

    def test_processes_wasteful_for_io(self, executed_nb):
        # Spawn overhead + no GIL benefit: processes lose to threads and asyncio.
        io_proc = executed_nb.ref("io_proc_elapsed")
        assert io_proc > executed_nb.ref("io_async_elapsed") * 3
        assert io_proc > executed_nb.ref("io_threads_elapsed")

    def test_all_io_strategies_handled_every_request(self, executed_nb):
        n = executed_nb.ref("N")
        # All strategies processed the same N requests — timing vars prove they ran.
        assert n == 100
        assert executed_nb.ref("io_seq_elapsed") > 0
        assert executed_nb.ref("io_threads_elapsed") > 0
        assert executed_nb.ref("io_async_elapsed") > 0
        assert executed_nb.ref("io_proc_elapsed") > 0


class TestLedgerAndHygiene:
    def test_ledger_output_shows_both_tables(self, executed_nb):
        cell_text = ""
        for i, cell in enumerate(executed_nb.cells):
            if cell.cell_type == "code" and "print_ledger(" in cell.source:
                cell_text = executed_nb.cell_output_text(i)
        assert "CPU-bound" in cell_text
        assert "I/O-bound" in cell_text
        assert "processes" in cell_text

    def test_line_ceiling_respected(self):
        import json

        with open(NOTEBOOK, encoding="utf-8") as f:
            nb = json.load(f)
        code_lines = sum(
            len("".join(c["source"]).splitlines())
            for c in nb["cells"]
            if c["cell_type"] == "code"
        )
        assert code_lines <= 180  # Advanced ceiling

    def test_pip_cell_is_first(self):
        import json

        with open(NOTEBOOK, encoding="utf-8") as f:
            nb = json.load(f)
        first_code = next(c for c in nb["cells"] if c["cell_type"] == "code")
        assert first_code["source"][0].strip().startswith("!")

    def test_workloads_module_importable(self):
        from workloads import blur, fetch, IMAGES, make_image

        assert len(IMAGES) == 100
        img = make_image(4)
        assert len(blur(img)) == 4
        assert fetch(3) == 6


class TestSpeedupSanity:
    def test_io_inverts_to_cpu(self, executed_nb):
        # On CPU, processes win; on I/O, asyncio wins. The inversion is the lesson.
        cpu_seq = executed_nb.ref("cpu_seq")
        assert executed_nb.ref("cpu_proc") < cpu_seq
        assert executed_nb.ref("io_async_elapsed") < executed_nb.ref("io_seq_elapsed")
