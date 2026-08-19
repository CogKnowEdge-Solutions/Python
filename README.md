# Advanced Python

A set of hands-on, self-contained Python labs for an advanced Python curriculum. Each
lab ships as a Jupyter notebook, a companion guide (`.md`), an assignment sheet with an
answer key, and an end-to-end `pytest` suite that executes the notebook in a fresh
kernel and validates the real output.

## Labs

| Lab | Topic | Difficulty | Time |
|-----|-------|------------|------|
| [Lab 1](Lab1) | Functional Data Wrangling with Lambda Functions | Beginner | ~25 min |
| [Lab 2](Lab2) | The Safe Resource Vault — Context Managers | Beginner | ~25 min |
| [Lab 3](Lab3) | The Memory-Efficient Data Pipeline — Iterators and Generators | Intermediate | ~40 min |
| [Lab 4](Lab4) | The Metaprogramming Toolkit — Decorators, Closures and Caching | Intermediate | ~40 min |
| [Lab 5](Lab5) | The Async API Fetcher — Concurrency in Action with `asyncio` | Intermediate | ~40 min |
| [Lab 6](Lab6) | Threading vs Multiprocessing vs asyncio — Which Concurrency Tool When? | Advanced | ~45 min |
| [Lab 7](Lab7) | The Ultimate Async Data Stream (Capstone) | Advanced | ~50 min |

Each lab folder ships four files: the Jupyter notebook, the companion guide (`.md`),
the assignment sheet with an answer key, and the `pytest` suite that validates the
lab. Lab 6 additionally ships a `workloads.py` companion module so its worker
*processes* can import the workloads by name. Each lab also includes an Excel
file (`lab<N>_test_results.xlsx`) with per-test pass/fail results, durations, and
failure messages.

### Lab 1 — Functional Data Wrangling with Lambda Functions

Turn a messy JSON product catalog into a clean, ranked table in one pipeline. You
work on a real pain point — dirty data — using **`lambda`** composed with
`filter()`, `map()`, and `sorted(key=...)`.

- Practice: anonymous functions, higher-order functions, `filter`/`map`/`sorted`.
- Build: a single `filter → map → sorted` expression that keeps only sellable
  products, normalizes mixed `USD`/`EUR`/`GBP` prices, applies a 10% clearance
  discount, and ranks by category then price.
- Data: shipped `data/product_catalog.json` — 37 deliberately messy products
  (missing fields, string/`null` prices) so you defend against real-world data.

### Lab 2 — The Safe Resource Vault — Context Managers

Guarantee resource cleanup even when code crashes mid-operation, and turn it into a
commit-on-success, roll-back-on-error transaction.

- Practice: `with` statements, `__enter__` / `__exit__`, `@contextlib.contextmanager`,
  `try/finally`.
- Build: a class-based `DatabaseConnection` manager, its compact generator-function
  twin, and a transaction context manager that commits on success and rolls back on
  error — each proven to clean up even when the block raises.
- Data: none — the "database" is a simulated class; the only file touched is
  `vault_notes.txt`, created by the notebook.

### Lab 3 — The Memory-Efficient Data Pipeline — Iterators and Generators

Process a log file far larger than RAM without ever loading it into memory.

- Practice: `iter()` / `next()` / `StopIteration`, hand-written `__iter__` /
  `__next__`, generator functions (`yield`), `itertools.groupby`, `sys.getsizeof`.
- Build: two lazy readers — a chunked `LogReader` class and a generator — that count
  `500` errors and find traffic spikes on a generated ~50 GB log, verify both give
  identical answers, and measure the memory difference.
- Data: the notebook generates a deterministic `data/server.log` (~141k lines), so
  every learner reproduces the same output.

### Lab 4 — The Metaprogramming Toolkit — Decorators, Closures and Caching

Add cross-cutting behavior to existing functions without modifying their code — the
toolkit every messy production codebase needs.

- Practice: decorators and decorator factories, closures, `*args` / `**kwargs`,
  `functools.wraps`.
- Build: four decorators from scratch — `@timer` (timing), `@authenticate` (role
  checks), `@retry` (flaky-call resilience), `@cache` (memoization) — proven against
  small in-code demos and summarized in a final `tabulate` ledger.
- Data: none — decorates four small in-code functions, no downloads, no API keys.

### Lab 5 — The Async API Fetcher — Concurrency in Action with `asyncio`

Fetch weather for 100 cities three ways and measure the difference: a blocking
synchronous loop, a fully concurrent `asyncio.gather` run, and a rate-limited
`Semaphore(5)` version.

- Practice: coroutines and `await`, the event loop, `aiohttp.ClientSession`,
  `asyncio.gather`, `asyncio.Semaphore`, timing with `perf_counter`.
- Build: a local mock weather API, three fetchers for the same 100 cities, and a
  `tabulate` ledger — the ledger's speed-up column (roughly 20x, capped at 5x)
  makes blocking, overlapping, and rate-limited I/O visible in one table.
- Data: none — a deterministic mock API on `localhost` (50 ms simulated latency),
  no downloads, no API keys, works offline.

### Lab 6 — Threading vs Multiprocessing vs asyncio

Run the same CPU-bound task (blurring 100 synthetic images in pure Python) and
the same I/O-bound task (100 fake 50 ms requests) under four execution
strategies — sequential, threads, asyncio, processes — and watch the two
ledgers *invert*.

- Practice: `ThreadPoolExecutor`, `ProcessPoolExecutor`, asyncio, timing with
  `perf_counter`, and how the GIL dictates which tool fits which workload.
- Build: two `tabulate` ledgers proving threads and asyncio don't speed up CPU
  work, processes win it, and asyncio crushes the I/O task ~100×.
- Data: none — a pure-Python box blur on synthetic images in `workloads.py`,
  fully offline, no downloads, no API keys.

### Lab 7 — The Ultimate Async Data Stream (Capstone)

The capstone: one production-shaped architecture that wires together every lab
in the catalog — a slow paginated API streamed into local storage piece by
piece.

- Practice: async generators (`async def ... yield`), `async for`, an
  async-aware `@timer`, lambda + `filter`/`map` cleaning pipelines, and async
  context managers (`async with`).
- Build: an ingestion engine that lazily paginates a slow source (a
  lazy-proof timing shows two pages costing ~0.12 s of a ~0.5 s stream), cleans
  each page on arrival, writes it to a JSON-lines store through an `async with`
  block, and reconciles a fetched-vs-kept-vs-stored ledger. The Optional
  Exercise makes the source flaky and proves retry plus the crash guarantee.
- Data: none — a deterministic simulated paginated API (10 pages × 10 events),
  fully offline, no downloads, no API keys.

## Repository Structure

```
Advanced_Python/
├── CONSTITUTION.md   # the rules every lab must follow before it can ship
├── AGENTS.md         # operating procedure for building and validating labs
├── GUIDELINES.md     # writing guide for lab notebooks and guides
├── TEST.md           # the testing framework used to validate each lab
├── Lab1/ … Lab7/     # one folder per lab (notebook, guide, assignment, tests, results)
├── README.md         # this file
└── LICENSE           # MIT
```

## Getting Started

Each lab folder is self-contained. From inside a lab folder:

```bash
python -m venv .venv
# Windows:        .venv\Scripts\activate
# macOS / Linux:  source .venv/bin/activate

pip install tabulate==0.10.0 notebook pytest testbook ipykernel

# Run the lab's validation suite
pytest test_<lab>.py -q
```

The notebooks also install their own pinned dependency from the first cell, so opening
them in any existing Jupyter environment works too.

## Test Results

Each lab includes an Excel workbook with detailed test results. All 135 tests
pass across all 7 labs.

| Lab | Tests | Status |
|-----|-------|--------|
| Lab 1 | 23/23 | PASS |
| Lab 2 | 19/19 | PASS |
| Lab 3 | 19/19 | PASS |
| Lab 4 | 20/20 | PASS |
| Lab 5 | 17/17 | PASS |
| Lab 6 | 14/14 | PASS |
| Lab 7 | 23/23 | PASS |

## License

This project is licensed under the [MIT License](LICENSE).
