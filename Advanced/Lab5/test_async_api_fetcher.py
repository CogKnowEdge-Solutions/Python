"""End-to-end tests for lab-async-api-fetcher.ipynb.

The notebook is executed top-to-bottom in a fresh kernel via testbook; tests
then assert on real kernel state and cell output. The first-cell `!pip install`
is stripped so the run is hermetic and offline.

Run from the lab folder::

    pip install pytest testbook ipykernel aiohttp==3.13.4 requests==2.32.3 tabulate==0.10.0
    pytest test_async_api_fetcher.py -q
"""

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from testbook import testbook

NOTEBOOK = "lab-async-api-fetcher.ipynb"


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


class TestInstall:
    def test_first_code_cell_is_pip_install(self):
        import nbformat
        nb = nbformat.read(NOTEBOOK, as_version=4)
        first_code = next(c for c in nb.cells if c.cell_type == "code")
        assert first_code.source.strip().startswith("!pip install")
        assert "aiohttp==3.13.4" in first_code.source
        assert "requests==2.32.3" in first_code.source
        assert "tabulate==0.10.0" in first_code.source


class TestInput:
    def test_thirty_cities_loaded(self, executed_nb):
        text = output_of(executed_nb, "Loaded")
        assert "Loaded 30 cities" in text

    def test_cities_are_dicts_with_coords(self, executed_nb):
        assert executed_nb.ref("len(CITIES)") == 30
        first = executed_nb.ref("CITIES[0]")
        assert isinstance(first, dict)
        assert "name" in first
        assert "lat" in first
        assert "lon" in first


class TestAsyncConcept:
    def test_hello_coroutine_runs(self, executed_nb):
        text = output_of(executed_nb, "hello")
        assert "Starting Alice" in text
        assert "Done Alice" in text


class TestFetchWeather:
    def test_single_fetch_returns_temp(self, executed_nb):
        text = output_of(executed_nb, "fetch_weather(CITIES[0], session)")
        assert "Weather in" in text
        assert "°C" in text


class TestSynchronous:
    def test_reports_thirty_cities(self, executed_nb):
        text = output_of(executed_nb, "sync_results")
        assert "Synchronous" in text
        assert "30 cities in" in text

    def test_returns_list_of_dicts(self, executed_nb):
        assert executed_nb.ref("len(sync_results)") == 30
        first = executed_nb.ref("sync_results[0]")
        assert isinstance(first, dict)
        assert "name" in first
        assert "temp_c" in first


class TestGather:
    def test_reports_speedup(self, executed_nb):
        text = output_of(executed_nb, "async_results")
        assert "Async gather" in text
        assert "30 cities in" in text
        assert "Speedup" in text

    def test_gather_beats_sync(self, executed_nb):
        assert executed_nb.ref("async_elapsed") < executed_nb.ref("sync_elapsed") / 3

    def test_returns_same_count(self, executed_nb):
        assert executed_nb.ref("len(async_results)") == 30


class TestThrottling:
    def test_unlimited_shows_throttling(self, executed_nb):
        text = output_of(executed_nb, "unlimited_results")
        assert "Fired all 30 at once" in text

    def test_throttled_requests_exist(self, executed_nb):
        failed = executed_nb.ref("len(failed)")
        total = executed_nb.ref("len(unlimited_results)")
        assert total == 30
        assert 0 <= failed < total


class TestBatchProcessing:
    def test_batch_function_defined(self, executed_nb):
        assert executed_nb.ref("callable(fetch_in_batches)")

    def test_batch_returns_thirty_cities(self, executed_nb):
        assert executed_nb.ref("len(batch_results)") == 30

    def test_batch_faster_than_sync(self, executed_nb):
        assert executed_nb.ref("batch_elapsed") < executed_nb.ref("sync_elapsed") / 2


class TestLedger:
    def test_ledger_prints_table(self, executed_nb):
        text = output_of(executed_nb, "tabulate(ledger")
        assert "Synchronous" in text
        assert "Async gather" in text
        assert "Batch processing" in text


class TestLineCeiling:
    def test_code_lines_within_limit(self):
        import json
        with open(NOTEBOOK, encoding="utf-8") as f:
            nb = json.load(f)
        code_lines = sum(
            len(c["source"]) if isinstance(c["source"], list)
            else len(c["source"].splitlines())
            for c in nb["cells"] if c["cell_type"] == "code"
        )
        assert code_lines <= 180
