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
        # Article II's ceiling is about *code*, so blanks and comment lines are
        # not counted: teaching comments are a requirement in this catalog, and
        # counting them would push every lab over the limit for being explained.
        import json

        with open(NOTEBOOK, encoding="utf-8") as f:
            nb = json.load(f)
        code_lines = sum(
            1
            for c in nb["cells"] if c["cell_type"] == "code"
            for line in "".join(c["source"]).splitlines()
            if line.strip() and not line.strip().startswith("#")
        )
        assert code_lines <= 180, f"{code_lines} code lines, ceiling is 180"

    def test_pip_cell_is_first(self):
        import json

        with open(NOTEBOOK, encoding="utf-8") as f:
            nb = json.load(f)
        first_code = next(c for c in nb["cells"] if c["cell_type"] == "code")
        assert first_code["source"][0].strip().startswith("!")

    def test_workloads_module_importable(self):
        from workloads import (
            COUNTER,
            COUNTER_LOCK,
            IMAGES,
            blur,
            bump_locked,
            bump_unlocked,
            counter_total,
            fetch,
            make_image,
            probe_worker,
            reset_counter,
        )

        assert len(IMAGES) == 100
        img = make_image(4)
        assert len(blur(img)) == 4
        assert fetch(3) == 6
        # The counter and its lock are module-level, so they are the same object
        # for every thread in this process - that is the memory model under test.
        assert COUNTER == {"count": 0}
        assert counter_total() == 0
        reset_counter()
        assert counter_total() == 0
        assert COUNTER_LOCK.acquire(blocking=False)
        COUNTER_LOCK.release()
        row = probe_worker("smoke-test")
        assert row["label"] == "smoke-test"
        assert row["pid"] > 0 and row["thread_id"] > 0
        assert isinstance(row["thread_name"], str)
        assert callable(bump_unlocked) and callable(bump_locked)


class TestMechanics:
    """Section 2-5: who is running, what is shared, what must be pickled."""

    def test_threads_share_one_process_id(self, executed_nb):
        # One interpreter, one GIL: every thread reports the kernel's own pid,
        # while the thread ids differ - the memory-model claim in Section 7.4.
        parent = executed_nb.ref("os").getpid()
        observations = executed_nb.ref("observations")
        assert len(observations) == 4
        assert {row["pid"] for row in observations} == {parent}
        assert len({row["thread_id"] for row in observations}) == 4
        assert all(isinstance(row["thread_name"], str) for row in observations)

    def test_thread_pool_and_process_pool_report_different_identities(self, executed_nb):
        by_pool = executed_nb.ref("probes_by_pool")
        assert set(by_pool) == {"threads", "processes"}
        thread_pids = {row["pid"] for row in by_pool["threads"]}
        process_pids = {row["pid"] for row in by_pool["processes"]}
        # Threads: one pid for the whole pool. Processes: one per live worker.
        assert len(thread_pids) == 1
        assert len(process_pids) >= 2
        assert not (thread_pids & process_pids)
        # All 16 tasks must have run, and on more than one worker - otherwise
        # the pid counts above would be measuring which worker booted first.
        assert len(by_pool["processes"]) == 16

    def test_unshared_race_loses_updates(self, executed_nb):
        # sleep(0) between the read and the write guarantees the GIL window is
        # hit, so the unguarded counter must come up short of 8000.
        assert executed_nb.ref("unlocked_total") < executed_nb.ref("EXPECTED")

    def test_lock_prevents_lost_updates(self, executed_nb):
        # The identical loop under COUNTER_LOCK loses nothing - deterministic.
        assert executed_nb.ref("locked_total") == executed_nb.ref("EXPECTED")
        assert executed_nb.ref("unlocked_total") < executed_nb.ref("locked_total")

    def test_process_workers_never_write_back_to_the_parent(self, executed_nb):
        # Which worker picks up which task is up to the pool, so a worker may
        # handle more than one of the 4 tasks and report 4000 or 6000. The
        # invariant is what makes the point: every reported total is a positive
        # multiple of STEPS (private copy, no partial sums from other workers),
        # they add up to all the work, and the parent still sees 0.
        per_worker = executed_nb.ref("per_worker")
        steps = executed_nb.ref("STEPS")
        assert len(per_worker) == 4
        assert all(v > 0 and v % steps == 0 for v in per_worker)
        assert sum(per_worker) == steps * len(per_worker)
        assert executed_nb.ref("counter_total")() == 0


class TestStartMethods:
    def test_start_method_cell_reports_and_catches(self, executed_nb):
        import multiprocessing as mp

        cell_text = ""
        for i, cell in enumerate(executed_nb.cells):
            if cell.cell_type == "code" and "get_start_method" in cell.source:
                cell_text = executed_nb.cell_output_text(i)
        assert "start method here" in cell_text
        assert "lambda via pool" in cell_text
        # The lambda must fail loudly-but-caught, never propagate out of the cell.
        assert "PicklingError" in cell_text or "AttributeError" in cell_text
        reported = executed_nb.ref("mp").get_start_method()
        assert reported == mp.get_start_method()
        assert reported in mp.get_all_start_methods()


class TestConceptDepth:
    """Guards the concept scaffolding the lab is judged on (Section 7)."""

    GUIDE = "lab-concurrency-models.md"

    def test_notebook_carries_the_three_way_comparison(self):
        import json

        with open(NOTEBOOK, encoding="utf-8") as f:
            nb = json.load(f)
        prose = "\n".join(
            "".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown"
        )
        assert "| | Threads | Processes | asyncio |" in prose
        for row in ("CPU parallelism (GIL on)", "Passing work and data",
                    "Shared mutable state", "Failure mode"):
            assert row in prose

    def test_guide_has_the_three_way_comparison_table(self):
        with open(self.GUIDE, encoding="utf-8") as f:
            guide = f.read()
        assert "| | Threads (`threading`, `ThreadPoolExecutor`) |" in guide
        assert "Processes (`multiprocessing`, `ProcessPoolExecutor`)" in guide
        for row in ("**Unit of execution**", "**Memory model**", "**True CPU parallelism**",
                    "**Cost to start a worker**", "**Shared mutable state**",
                    "**Practical ceiling**", "**Choose it when**"):
            assert row in guide

    def test_guide_documents_each_model_in_depth(self):
        with open(self.GUIDE, encoding="utf-8") as f:
            guide = f.read()
        for heading in ("### 7.4 Threading", "### 7.5 Multiprocessing",
                        "### 7.6 asyncio", "### 7.7 The three compared",
                        "### 7.8 Choosing", "### 7.9 When one answer is not enough"):
            assert heading in guide
        # Threads and processes each need their own mechanisms documented.
        for term in ("threading.Lock", "daemon", "start method", "fork", "spawn",
                     "BrokenProcessPool", "maxtasksperchild", "run_in_executor",
                     "head-of-line"):
            assert term in guide

    def test_guide_has_mermaid_diagrams_for_each_concept(self):
        with open(self.GUIDE, encoding="utf-8") as f:
            guide = f.read()
        diagrams = guide.count("```mermaid")
        assert diagrams >= 6, f"only {diagrams} mermaid diagrams in Section 7"
        # House style: every diagram opens with the shared %%{init}%% directive,
        # so rendered diagrams look identical across the catalog.
        assert guide.count("%%{init:") >= diagrams
        assert "flowchart" in guide or "graph" in guide


class TestSpeedupSanity:
    def test_io_inverts_to_cpu(self, executed_nb):
        # On CPU, processes win; on I/O, asyncio wins. The inversion is the lesson.
        cpu_seq = executed_nb.ref("cpu_seq")
        assert executed_nb.ref("cpu_proc") < cpu_seq
        assert executed_nb.ref("io_async_elapsed") < executed_nb.ref("io_seq_elapsed")
