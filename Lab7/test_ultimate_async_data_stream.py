"""End-to-end tests for lab-ultimate-async-data-stream.ipynb.

The notebook is executed top-to-bottom in a fresh kernel via testbook; tests
then assert on real kernel state and cell output. The first-cell `!pip install`
is stripped so the run is hermetic and offline.

Run from the lab folder::

    pip install pytest testbook ipykernel tabulate==0.10.0
    pytest test_ultimate_async_data_stream.py -q
"""

import asyncio
import json
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from testbook import testbook

NOTEBOOK = "lab-ultimate-async-data-stream.ipynb"


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


class TestPipelineAccounting:
    def test_all_events_came_off_the_wire(self, executed_nb):
        assert executed_nb.ref("fetched") == executed_nb.ref("TOTAL_PAGES") * executed_nb.ref("PAGE_SIZE")
        assert executed_nb.ref("fetched") == 100

    def test_kept_count_is_deterministic(self, executed_nb):
        assert executed_nb.ref("stored") == 61

    def test_file_holds_exactly_the_stored_rows(self, executed_nb):
        rows = executed_nb.ref("rows")
        assert len(rows) == executed_nb.ref("stored")
        assert all(isinstance(r, dict) and "price" in r for r in rows)

    def test_first_and_last_stored_rows(self, executed_nb):
        rows = executed_nb.ref("rows")
        assert rows[0]["event_id"] == 5
        assert rows[-1]["event_id"] == 99
        assert rows[0]["amount"] == 36
        assert rows[-1]["amount"] == 73

    def test_events_jsonl_is_valid_json_lines(self, executed_nb):
        with open("events.jsonl", encoding="utf-8") as f:
            lines = f.read().splitlines()
        assert len(lines) == 61
        for line in lines:
            json.loads(line)  # must not raise


class TestAsyncGenerator:
    def test_stream_pages_is_an_async_generator(self, executed_nb):
        # CO_ASYNC_GENERATOR = 0x200: async def + yield sets this code flag.
        assert executed_nb.ref("stream_pages.__code__.co_flags") & 0x200

    def test_lazy_proof_stops_after_two_pages(self, executed_nb):
        text = output_of(executed_nb, 'if seen == 2:')
        assert "consumed 2/10 pages" in text

    def test_generator_yields_page_dicts(self, executed_nb):
        executed_nb.inject(
            "async def _probe():\n"
            "    gen = stream_pages()\n"
            "    first = await gen.__anext__()\n"
            "    await gen.aclose()\n"
            "    return first\n"
            "_first_page = await _probe()",
            pop=True)
        first = executed_nb.ref("_first_page")
        assert first["page"] == 1
        assert len(first["events"]) == 10
        assert first["has_more"] is True


class TestTimer:
    def test_ingest_was_timed(self, executed_nb):
        text = output_of(executed_nb, "async def ingest()")
        assert "ingest ran in " in text

    def test_wraps_preserves_name(self, executed_nb):
        assert executed_nb.ref("ingest.__name__") == "ingest"

    def test_timer_handles_coroutine_functions(self, executed_nb):
        assert executed_nb.ref("asyncio.iscoroutinefunction(ingest)")


class TestStore:
    def test_store_implements_async_context_manager(self, executed_nb):
        store = executed_nb.ref("LocalStore")
        assert hasattr(store, "__aenter__") and hasattr(store, "__aexit__")

    def test_exit_reports_commit(self, executed_nb):
        text = output_of(executed_nb, "async def ingest()")
        assert "committed 61 rows to events.jsonl" in text

    def test_store_counts_rows_written(self, executed_nb, tmp_path):
        path = str(tmp_path / "probe.jsonl").replace("\\", "/")
        executed_nb.inject(
            "async def _probe(_path):\n"
            "    async with LocalStore(_path) as db:\n"
            "        db.write([{'x': 1}])\n"
            "        db.write([{'x': 2}, {'x': 3}])\n"
            "    return db.rows\n"
            f"_store_rows = await _probe({path!r})",
            pop=True)
        assert executed_nb.ref("_store_rows") == 3


class TestCleanPipeline:
    def test_clean_keeps_and_maps(self, executed_nb):
        clean = executed_nb.ref("clean")
        sample = [{"event_id": 0, "kind": "click", "amount": 5},
                  {"event_id": 1, "kind": "click", "amount": 40}]
        out = clean(sample)
        assert len(out) == 1
        assert out[0]["amount"] == 40
        assert out[0]["price"] == round(40 * 1.08, 2)

    def test_lambda_kept_count_printed_per_page(self, executed_nb):
        text = output_of(executed_nb, "async def ingest()")
        assert "page 1: kept 5/10" in text
        assert "page 10: kept 7/10" in text


class TestLedgerAndHygiene:
    def test_ledger_output_shows_all_stages(self, executed_nb):
        text = output_of(executed_nb, "tabulate(ledger")
        assert "fetched (events)" in text
        assert "kept (amount >= 30)" in text
        assert "stored (JSON lines)" in text
        assert "61/100 survived the filter" in text

    def test_line_ceiling_respected(self):
        with open(NOTEBOOK, encoding="utf-8") as f:
            nb = json.load(f)
        code_lines = sum(
            len("".join(c["source"]).splitlines())
            for c in nb["cells"]
            if c["cell_type"] == "code"
        )
        assert code_lines <= 180  # Advanced ceiling

    def test_pip_cell_is_first(self):
        with open(NOTEBOOK, encoding="utf-8") as f:
            nb = json.load(f)
        first_code = next(c for c in nb["cells"] if c["cell_type"] == "code")
        assert first_code["source"][0].strip().startswith("!")

    def test_tabulate_pinned_version(self):
        import tabulate
        assert tabulate.__version__ == "0.10.0"

    def test_no_tests_embedded_in_notebook(self):
        with open(NOTEBOOK, encoding="utf-8") as f:
            nb = json.load(f)
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                assert "pytest" not in cell["source"]


class TestOptionalExerciseLogic:
    """Section 11 in isolation: flaky source + retry, and the crash guarantee."""

    def test_retry_recovers_flaky_pages(self):
        PAGE_SIZE, TOTAL_PAGES = 10, 10
        flaky = {"hit": set()}

        async def fetch_page(page):
            await asyncio.sleep(0.01)
            if page % 4 == 0 and page not in flaky["hit"]:
                flaky["hit"].add(page)
                raise RuntimeError("gateway timed out")
            events = [{"amount": i * 7 + page} for i in range(PAGE_SIZE)]
            return {"page": page, "events": events, "has_more": page < TOTAL_PAGES}

        async def stream_pages():
            page = 1
            while True:
                for attempt in range(1, 4):
                    try:
                        data = await fetch_page(page)
                        break
                    except RuntimeError:
                        await asyncio.sleep(0.01)
                else:
                    raise RuntimeError(f"page {page} failed after 3 attempts")
                yield data
                if not data["has_more"]:
                    return
                page += 1

        async def run():
            pages = [p async for p in stream_pages()]
            return len(pages), sorted(flaky["hit"])

        n_pages, hit = asyncio.run(run())
        assert n_pages == 10
        assert hit == [4, 8]

    def test_crash_guarantee_closes_and_reports(self, tmp_path):
        path = tmp_path / "crash.jsonl"

        class LocalStore:
            def __init__(self, p):
                self.path = p
            async def __aenter__(self):
                self.file = open(self.path, "w", encoding="utf-8")
                self.rows = 0
                return self
            async def __aexit__(self, exc_type, exc, tb):
                self.file.close()
                self.exc_name = exc_type.__name__ if exc_type is not None else None
            def write(self, events):
                for ev in events:
                    self.file.write(json.dumps(ev) + "\n")
                    self.rows += 1
                self.file.flush()

        async def run():
            try:
                async with LocalStore(str(path)) as db:
                    db.write([{"x": 1}, {"x": 2}])
                    raise ValueError("boom mid-write")
            except ValueError:
                pass
            return db

        db = asyncio.run(run())
        assert db.exc_name == "ValueError"
        text = path.read_text(encoding="utf-8")
        assert text.splitlines() == ['{"x": 1}', '{"x": 2}']
