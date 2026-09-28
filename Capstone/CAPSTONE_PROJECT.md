# Capstone Project: Real-Time Data Analytics Dashboard

**Difficulty: Advanced Capstone | Course-Wide Integration**\
**Duration: 120 min (implementation) — single session, timed like a lab**\
**Requires: Labs 1–23 (Beginner + Intermediate + Advanced) | Real-world data pipelines**

**This is a *solve-it-yourself* project.** No reference solution is included anywhere in this repository — you build every module from scratch against this specification. **Section 8 (Underlying Concepts)** maps every lab from all three sections to where it appears here, and **Section 12 (Marking Breakdown)** is your grading guide.

**This document is a complete, single-file reference** — no other guide is needed. Run **`CAPSTONE_SETUP.ipynb`** (the only companion file in `Capstone/`) once to bootstrap your project's data files and module templates, then build from this spec.

---

## 1. Lab Title

**Real-Time Data Analytics Dashboard: a production-grade pipeline that ingests messy streaming sales data from multiple stores, validates and normalizes it with regex and `None` identity checks, processes it concurrently with rate-limited async batches, aggregates it into ranked business insights, stores it in a queryable in-memory API, and exports formatted reports with a measured sequential-vs-async speedup — the full integration of every concept from Labs 1–23 applied to a real-world retail data problem.**

---

## 2. Problem Statement / Use Case Overview

You are building a **real-time data analytics dashboard** for a retail analytics company. The system ingests streaming sales data from multiple stores, processes it concurrently, applies business rules and transformations, and exposes a queryable API that web dashboards consume.

**The Challenge:**
- **Data arrives streaming** — you cannot wait for all of it at once.
- **Multiple stores report simultaneously** — you need concurrent processing without overwhelming the server.
- **Business rules are complex** — filtering, normalizing, aggregating, and ranking data.
- **Performance matters** — slow queries or blocking operations will kill the dashboard experience.
- **Data quality varies** — prices might be missing, store IDs might be malformed, and timestamps might be inconsistent.

By the end, you will have built an end-to-end system that handles all of this, demonstrating mastery of:
- **Beginner concepts:** data types, *strings (indexing, methods, f-strings)*, collections, comprehensions, control flow
- **Intermediate concepts:** functions, modules, *string formatting and regex*, *recursion*, OOP (including *advanced class tools*), file I/O, error handling
- **Advanced concepts:** lambdas and functional pipelines, *context managers*, generators, decorators, async/await and rate-limiting, *concurrency model comparison (sequential vs async)*

**Real-world impact:** analytics teams get clean, queryable, cost-bounded metrics streaming in instead of a pile of messy CSVs. The pipeline is the same shape real data-engineering stacks use (ingest → transform → warehouse → BI), scaled down to a single machine.

---

## 3. Project Structure

Unlike the section labs (which use a single notebook), this capstone is a **full project**. You build a directory of files, not a single `.ipynb`. The structure below is a starting point — **adapt it to your understanding and how you like to organize code.** There is no single right structure.

```
retail-analytics-capstone/
│
├── README.md                      # Project overview, setup instructions, objectives
├── requirements.txt               # aiohttp, requests, tabulate (pinned)
├── .env.example                   # Optional: template for real endpoints/keys (mock works without)
├── .gitignore
│
├── docs/
│   ├── project_brief.md           # Problem statement, goals, success criteria
│   ├── architecture.md            # System design / pipeline flow diagram
│   └── rubric.md                  # Grading criteria / evaluation checklist
│
├── src/
│   ├── __init__.py
│   ├── config.py                  # Constants, env loading, path setup
│   ├── ingestion.py               # CSV reader, validator, async API client
│   ├── analytics.py               # Aggregations, rankings, recursive category tree
│   ├── storage.py                 # AnalyticsStore: query API, indexing, dunder methods
│   ├── reporting.py               # @timed, console tables, CSV export
│   └── main.py                    # Entry point: orchestrates ingest → process → store → report
│
├── data/
│   ├── raw/                       # store_sales.csv, store_metadata.json (from CAPSTONE_SETUP.ipynb)
│   └── output/                    # Exported results.csv produced by reporting
│
├── notebooks/
│   └── exploration.ipynb          # Prototyping / experimentation
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_analytics.py
│   ├── test_storage.py
│   └── test_reporting.py
│
└── submission/
    ├── demo_video_link.md         # Or embedded demo instructions
    └── reflection.md              # Write-up: challenges, learnings
```

> **Note:** This structure is a suggestion, not a requirement. If a module is small, keep it in `src/` directly — you do not need to split further. The key is that someone else can understand your project by reading your `README.md` and looking at the folder names.

### What each folder/file is for

| Path | Purpose |
|------|---------|
| `README.md` | The front door. Explains what the project does, how to set it up, and how to run it. Write this last. |
| `requirements.txt` | Pinned dependencies. `pip install -r requirements.txt` should set up everything. |
| `.env.example` | Shows which config variables exist (real endpoints/keys later) without exposing anything. |
| `.gitignore` | Keeps `.env`, `__pycache__/`, `.venv/`, and generated `data/` files out of git. |
| `docs/` | Design documents. `project_brief.md` is your problem statement; `architecture.md` has your pipeline flow; `rubric.md` mirrors Section 12. |
| `src/` | All production code. `config.py` holds shared constants; each pipeline stage is one module. |
| `data/` | `raw/` holds the messy CSV/JSON you are given; `output/` holds exports. Never commit generated files. |
| `notebooks/` | Scratch space for prototyping. Working code gets moved into `src/`. |
| `tests/` | One pytest file per module. |
| `submission/` | What you hand in: `reflection.md` (write-up) and a demo link/walkthrough. |

---

## 4. Input Data

All synthetic, deterministic, reproducible — generated by **`CAPSTONE_SETUP.ipynb`**:

- **`data/raw/store_sales.csv`** — historical sales with at least 100 records, deliberately messy (see below).
- **`data/raw/store_metadata.json`** — store info (id, name, region, manager).
- **Simulated real-time API** — a `StoreAPIClient` class you provide that fetches "live" transactions from a URL, rate-limited to 10 concurrent requests (else HTTP 429).

### Record schema (data model)

```python
{
    "transaction_id": "TXN-001",          # string, unique
    "store_id": "STORE-123",               # string, may be malformed
    "timestamp": "2026-09-18T14:30:45Z",  # ISO 8601, may be inconsistent
    "product_name": "Widget A",            # string
    "category": "Electronics",             # string
    "price": 29.99,                        # float or string or None
    "quantity": 5,                         # int or string or None
    "discount_pct": 10.0,                  # float (0–100) or None
    "payment_method": "card",              # string: card, cash, online
    "region": "North America"              # string
}
```

### How messy is "messy"?

- Some prices are strings (`"29.99"`)
- Some prices are `None` or empty
- Some quantities are missing
- Some timestamps are malformed (wrong format, missing timezone)
- Some store IDs are malformed (lowercase, trailing spaces, or wrong length)
- Some product names have erratic casing and extra whitespace
- Discount percentages are sometimes > 100 or negative (invalid)

**Example rows** (note `TXN-005` has a malformed `store_id` and messy name):
```
transaction_id,store_id,timestamp,product_name,category,price,quantity,discount_pct,payment_method,region
TXN-001,STORE-123,2026-09-18T14:30:45Z,Widget A,Electronics,29.99,5,10.0,card,North America
TXN-002,STORE-456,2026-09-18T14:35:00Z,Gadget B,Electronics,"34.50",3,,5.0,cash,Europe
TXN-003,STORE-789,2026-09-18T14:40:30,Doohickey,Home,,"2",20.0,card,Asia
TXN-004,STORE-123,2026-09-18T15:00:00Z,Widget A,Electronics,-15.99,1,0,online,North America
TXN-005,store-abc ,2026-09-18T15:05:00Z,  WIDGET  a  ,Electronics,"19.99",2,5.0,cash,North America
```

**`data/raw/store_metadata.json`:**
```json
[
    {"store_id": "STORE-123", "name": "Downtown NYC", "region": "North America", "manager": "Alice"},
    {"store_id": "STORE-456", "name": "Paris Center", "region": "Europe", "manager": "Bob"},
    {"store_id": "STORE-789", "name": "Tokyo Mall", "region": "Asia", "manager": "Charlie"}
]
```

---

## 5. Processing

The system runs in **five phases** for each ingestion run (the CSV stream and the simulated API stream both flow through the same pipeline):

1. **Load data sources** — `src/ingestion.py` reads `store_sales.csv` as a generator that yields normalized records lazily, while `src/main.py` concurrently fetches "live" records from the mock API in rate-limited async batches (5 per batch).
2. **Validate & normalize each record** — required fields are checked with `None` identity checks; prices/quantities that arrive as strings or negatives are repaired; timestamps parse via `datetime.fromisoformat()`; free-text is sanitized with string methods and regex (`^STORE-\d{3}$`), with a `match`/`case` dispatching the right cleanup per field.
3. **Aggregate & compute metrics** — `src/analytics.py` groups by store, region, category, and payment method using comprehensions; transforms and ranks with `filter()`/`map()`/`sorted()` plus tuple sort keys; discovers unique values with set comprehensions; and builds a nested category tree with a recursive function.
4. **Store & query** — `src/storage.py` holds an `AnalyticsStore` (private attributes + properties) with a `query(**filters)` API that dispatches each filter via `match`/`case`, an inner result-row class, a `@classmethod` factory, and `__str__()`/`__repr__()`.
5. **Report & export** — `src/reporting.py` formats aligned tables and currency/percentages with f-string specifiers, exports CSV, and measures its own work with a `@timed` decorator and a `@contextlib.contextmanager` timing block; `src/main.py` prints the **Concurrency Report** (sequential vs async timings).

### Module responsibilities at a glance

| Module | File | Core responsibilities |
|--------|------|-----------------------|
| 1 — Ingestion | `src/ingestion.py` | Read CSV as a lazy generator; validate and normalize every record (`None` identity checks, `match`/`case`, regex `store_id` check, `datetime` parsing, price rounding); async batch API fetcher (5 per batch, rate-limited, HTTP errors handled) |
| 2 — Analytics | `src/analytics.py` | Aggregate by store, region, category, payment method; rank with multi-key tuple sorts; transform via lambdas + `filter()`/`map()`/`sorted()`; unique-value set comprehensions; recursive category tree (base case + stated Big-O) |
| 3 — Storage & Query | `src/storage.py` | In-memory `AnalyticsStore` (private attrs + properties, `__str__()`/`__repr__()`, inner result-row class, `@classmethod` factory); `query(**filters)` dispatch via `match`/`case`; custom exceptions for invalid filters |
| 4 — Reporting | `src/reporting.py` | f-string tables and currency/percent formatting; CSV export; `@timed` decorator (`functools.wraps`); context-manager timing; timing metadata |
| 5 — Orchestration | `src/main.py` | Pipeline ingest → process → store → report; CSV + API in parallel; skip-and-log per record, re-raise structural failures; `--region`/`--output`/`--top-n`; sequential-vs-async Concurrency Report |

## 6. Output

Four artifacts:

1. **Remote console report** — full golden-path run seen in the terminal (below).
2. **`data/output/results.csv`** — exported top performers (when `--output` is passed).
3. **Timing summary** — total elapsed time plus the Concurrency Report line.
4. **Module test results** — `tests/*.py` passing for each module (Section 11, Phase 7).

**Golden-path run:**

```bash
$ python src/main.py --region "North America" --output results.csv --top-n 5
```

```
Loading data…
  ✓ Read 150 records from store_sales.csv
  ✓ Fetched 50 live records from API (10 batches of 5)
  Total: 200 records

Processing…
  ✓ Normalized prices, quantities, timestamps
  ✓ Computed revenue per transaction
  ✓ Aggregated by store, region, category

Filtering…
  ✓ Filtered to North America (120 records)
  ✓ Top 5 performers:

┌────────────┬──────────────┬─────────────┬──────────────┐
│ Store ID   │ Store Name   │ Total ($)   │ Transactions │
├────────────┼──────────────┼─────────────┼──────────────┤
│ STORE-123  │ Downtown NYC │ $12,345.67  │ 45           │
│ STORE-456  │ Paris Center │ $11,234.56  │ 38           │
│ STORE-789  │ Tokyo Mall   │ $10,123.45  │ 37           │
└────────────┴──────────────┴─────────────┴──────────────┘

Exporting…
  ✓ Saved results to results.csv

Concurrency Report: sequential 3.20s vs async 0.71s — async is 4.5x faster

Total elapsed time: 2.34s
```

---

## 7. Tech Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Core language |
| `csv` (stdlib) | — | CSV reading and export |
| `json` (stdlib) | — | Store metadata + JSON handling |
| `re` (stdlib) | — | Store-ID/product-name validation and sanitization |
| `math` (stdlib) | — | Price rounding (`floor`/`ceil`/`round`) |
| `datetime` (stdlib) | — | Timestamp parsing and formatting |
| `asyncio` (stdlib) | — | Async API fetch, batched rate-limiting |
| `aiohttp` | 3.13.4 (pinned) | Async HTTP client (simulated real-time API) |
| `requests` | 2.32.3 (optional) | Synchronous baseline for the concurrency comparison |
| `tabulate` | 0.10.0 | Pretty console tables |
| `argparse` (stdlib) | — | CLI flags (`--region`, `--output`, `--top-n`) |
| `functools` / `contextlib` (stdlib) | — | `@timed` decorator (`wraps`), context managers |
| `logging` (stdlib) | — | Progress and error logging |
| `pytest` | any recent | Module test files (`tests/`) |

**Real-world dependencies (mocked in the lab):**
- Live transaction/market API (Alpha Vantage, IEX Cloud, store POS feeds) — mocked with a static feed in `CAPSTONE_SETUP.ipynb`
- Data warehouse / SQL store — mocked with the in-memory `AnalyticsStore`
- Streaming scheduler (Airflow/Kafka) — mocked with `asyncio` batched fetching in `main.py`

---

## 8. Underlying Concepts

This capstone integrates every lab concept from all three sections, applied to a real data pipeline. The map below is your guarantee that **every lab in the course has a place here** — topics are "present" at a level that makes sense for one integrated project, not every lab detail but every major concept. Use it to know *where* each lab you studied shows up again.

### Beginner Section

| Lab | Core topics | Where it appears in the capstone |
|-----|-------------|----------------------------------|
| Lab 1 — Variables, Data Types & Operators | `int`/`float`/`str`/`bool`, arithmetic, comparisons | Revenue math (`price × quantity × (1 − discount)`), range validation in **Modules 1–2** |
| Lab 2 — Strings | Indexing, slicing, methods, f-strings | Product-name cleaning (`.strip()`, `.title()`, `.upper()`) in **Module 1**; currency and column formatting via f-strings in **Module 4** |
| Lab 3 — Collections | Lists, dicts, tuples, sets | Record holders (lists of dicts), lookup dicts, tuple sort keys, set comprehensions of unique products in **Module 2** |
| Lab 4 — Control Flow | If/elif/else, for/while, break/continue, ternary | Validation branches and per-store loops in **Modules 1–2**; retry loops in **Module 5** |
| Lab 5 — Comprehensions | List/dict/set comprehensions, filtering | All aggregations and unique-value discovery in **Module 2** |
| Lab 6 — Student Report Generator (mini-project) | Integrating the basics end-to-end | The whole pipeline is a larger version of this mini-project |

### Intermediate Section

| Lab | Core topics | Where it appears in the capstone |
|-----|-------------|----------------------------------|
| Lab 1 — Functions & Scope | def, parameters, type hints, default args, scope | All module functions; `query(**filters)` and typed signatures in **Module 3** |
| Lab 2 — Imports & Modules | `import`, `math`, `datetime`, `random`, `from X import Y` | `datetime` for timestamps (**Modules 1, 4**), `math` for rounding prices (**Module 1**), module-level imports in **Module 5** |
| Lab 3 — Functions II | `*args`/`**kwargs`, lambda, `sorted(key=)`, `map()`/`filter()` | `**kwargs` filter API (**Module 3**); lambdas + functional tools (**Module 2**) |
| Lab 4 — Miscellaneous Topics | `match`/`case`, `None` checks, `input()`, `range()`, regex, string formatting | `match`-based field cleanup (**Module 1**), `match`-based filter dispatch (**Module 3**), regex store-ID validation (**Module 1**), argparse (**Module 5**) |
| Lab 5 — Error Handling | try/except/finally, specific exceptions, custom exceptions, re-raise | Custom `DataValidationError`/`QueryError`, skip-and-log recovery, re-raising structural failures (**Modules 1, 3, 5**) |
| Lab 6 — Recursion & Algorithms | Base case, recursion depth, call stack, efficiency | Recursive category-tree builder in **Module 2**; optional extension 8 adds a Big-O profiling pass |
| Lab 7 — File Handling | `with open()`, modes, encoding, JSON/CSV | All CSV/JSON reading and writing, CSV export, JSON metadata (**Modules 1, 4**) |
| Lab 8 — OOP I: Core Concepts | Classes, encapsulation, `@property`, inheritance, polymorphism | `AnalyticsStore` with private attributes + properties (**Module 3**); module classes (**Modules 1–4**) |
| Lab 9 — OOP II: Advanced Class Tools | Inner classes, static/class methods, dunder methods | Inner result-row class, `@classmethod` factory, `__str__()`/`__repr__()` (**Module 3**) |
| Lab 10 — School Management System (mini-project) | OOP composition end-to-end | The class-driven module design here is the bigger version |

### Advanced Section

| Lab | Core topics | Where it appears in the capstone |
|-----|-------------|----------------------------------|
| Lab 1 — Functional Data Wrangling | Lambda, `filter()`/`map()`/`sorted()`, messy data, multi-key sort | The full **Module 2** analytics pipeline |
| Lab 2 — Safe Resource Vault | `with`, `__enter__`/`__exit__`, `@contextlib.contextmanager`, commit/rollback | File-handle context managers (**Modules 1, 4**); `@contextlib.contextmanager` timing block (**Module 4**) |
| Lab 3 — Memory-Efficient Data Pipeline | Iterator protocol, generators, `yield`, memory payoff | Generator-based ingestion that yields records lazily (**Module 1**) |
| Lab 4 — Metaprogramming Toolkit | Decorators, closures, `functools.wraps`, decorator factories | `@timed` decorator (**Module 4**); `@cache` and `@retry` in optional extensions 1 & 6 |
| Lab 5 — Async API Fetcher | Event loop, `async def`/`await`, `asyncio.gather()`, rate limits, batches | The async batch fetcher in **Module 1** |
| Lab 6 — Concurrency Models | Sequential vs threading vs multiprocessing vs asyncio | Sequential-vs-async baseline in **Module 5**; optional extension 7 compares all four models |
| Lab 7 — Ultimate Async Data Stream (mini-project) | Async generators + decorators + context managers | The capstone's entire ingest pipeline builds on this |

### Real-world Skills (across all modules)

- Data validation and normalization of messy, realistic data
- Concurrent API client design with rate limiting
- Query optimization and indexing
- Error recovery, resilience, and logging
- Clear module boundaries and single-responsibility design

---

## 9. Prerequisites

- **Labs 1–23 (required)** — every concept is used; Section 8 maps each lab to where it appears
- **Python 3.11+** and a text editor/IDE
- **pinned packages** — `aiohttp`, `requests`, `tabulate`; internet access for `pip` install only
- **No API keys required** — the data API is fully mocked
- **Jupyter** (or `jupyter nbconvert`) — run `CAPSTONE_SETUP.ipynb` once to generate data + templates
- **Comfort with** `re`, `math`, `datetime`, `asyncio` — all taught in the Intermediate/Advanced labs
- **`pytest`** installed for the module test files

---

## 10. Environment / Dependencies Setup

Create the project and a virtual environment, then install pinned dependencies:

```bash
cd retail-analytics-capstone
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt`:

```text
aiohttp==3.13.4
requests==2.32.3      # optional, for the synchronous baseline
tabulate==0.10.0
pytest==8.3.5
```

Then generate your data files and module templates once:

```bash
# From the Capstone/ folder (where CAPSTONE_SETUP.ipynb lives):
jupyter nbconvert --execute CAPSTONE_SETUP.ipynb
# or open it in Jupyter and run all cells
```

That creates `data/raw/store_sales.csv`, `data/raw/store_metadata.json`, and skeleton files for `src/` and `docs/`.

---

## 11. Development Guide

This is not a step-by-step notebook — you are building a project. Below is the recommended order of work; adapt it to your pace. **Do not skip a phase** — each builds on the previous one.

### Phase 1: Foundation

| Task | What to build | Labs used |
|------|---------------|-----------|
| Set up project structure | Directory tree, `requirements.txt`, `.gitignore`, `README.md` stub | — |
| Config module | `src/config.py` — constants, paths, optional env loading | Beginner Lab 1, Intermediate Lab 2 |
| Generate data | Run `CAPSTONE_SETUP.ipynb` → `data/raw/*` | — |
| Module skeletons | Empty `src/ingestion.py` etc. + `tests/` foo files | — |

### Phase 2: Data Ingestion (Module 1)

| Task | What to build | Labs used |
|------|---------------|-----------|
| CSV reader + generator | `src/ingestion.py` using `csv.DictReader`, yielded records | Intermediate Lab 7 |
| Validation & normalization | `None` identity checks, `match`/`case`, regex, `math` rounding, `datetime` parsing | Beginner Labs 1–4, Intermediate Lab 4 |
| Async API client | `aiohttp` batch fetcher with rate-limiting and HTTP error handling | Advanced Labs 2, 5 |
| Context managers | File handles + `ClientSession` in `with`/`async with` | Advanced Lab 2 |

### Phase 3: Processing & Analytics (Module 2)

| Task | What to build | Labs used |
|------|---------------|-----------|
| Group & aggregate | Dict comprehension / `groupby()` by store, region, category, payment | Beginner Lab 5 |
| Rank & filter | Lambdas + `filter()`/`map()`/`sorted()` with tuple sort keys | Advanced Lab 1 |
| Unique discovery | Set comprehensions of products, regions, categories | Beginner Lab 5 |
| Recursive category tree | `build_tree(pairs, parent=None)` with base case + depth/Big-O comment | Intermediate Lab 6 |

### Phase 4: Storage & Query (Module 3)

| Task | What to build | Labs used |
|------|---------------|-----------|
| `AnalyticsStore` class | Private attributes + `@property` accessors | Intermediate Lab 8 |
| Query API | `query(**filters)` dispatching each filter via `match`/`case` | Intermediate Labs 3, 4 |
| Class tools | Inner result-row class, `@classmethod` factory, `__str__()`/`__repr__()` | Intermediate Lab 9 |
| Custom exceptions | `QueryError` etc. for invalid filters | Intermediate Lab 5 |

### Phase 5: Reporting (Module 4)

| Task | What to build | Labs used |
|------|---------------|-----------|
| `@timed` decorator | `functools.wraps` + `time.perf_counter()` | Advanced Lab 4 |
| Console tables | `tabulate` + f-string specifiers (`${total:,.2f}`, `{store:>20}`) | Beginner Lab 2 |
| CSV export | `csv.DictWriter` in a context manager | Intermediate Lab 7, Advanced Lab 2 |

### Phase 6: Orchestration & Concurrency (Module 5)

| Task | What to build | Labs used |
|------|---------------|-----------|
| Pipeline orchestration | `asyncio.gather()` for CSV + API in parallel, chained modules | Advanced Labs 5, 7 |
| Sequential-vs-async baseline | `time.perf_counter()` around sync loop vs batched async fetch | Advanced Lab 6 |
| CLI + logging | `argparse` flags, progress logs, main guard | Intermediate Lab 4 |
| Error policy | Skip-and-log per record; re-raise only structural failures | Intermediate Lab 5 |

### Phase 7: Testing & Submission

| Task | What to deliver | Where |
|------|-----------------|-------|
| Module tests | `test_ingestion.py`, `test_analytics.py`, `test_storage.py`, `test_reporting.py` | `tests/` |
| README | Overview, setup, how to run — write last | `README.md` |
| Reflection | Challenges, design decisions, what you learned | `submission/reflection.md` |
| Demo | 3–5 minute walkthrough or written run | `submission/demo_video_link.md` |
| Architecture diagram | Mermaid or hand-drawn pipeline flow | `docs/architecture.md` |

Write searchable tests per `TEST.md`: one standalone pytest `.py` file per module, never tests inside notebooks. Run them with `pytest --junitxml=...` and convert results via `scripts/pytest_to_xlsx.py` if you want a reviewable workbook.

> **Workflow tips (if you get stuck):** re-read the relevant lab — Section 8 maps every requirement back to the lab that taught it; print intermediate results to see where data flows; break the problem smaller — one module at a time; test each module independently before integrating; re-read Section 5 to confirm you haven't missed anything.

---

## 12. Marking Breakdown

| Criterion | Weight | What is evaluated |
|-----------|--------|-------------------|
| **Data Ingestion** | 20% | Reads CSV correctly; validates and normalizes prices (strings, None, negatives); parses ISO 8601 timestamps; async batch fetcher with rate-limiting; context managers for files; free-text sanitization with string methods; `store_id` regex validation; `None` identity checks and `match`/`case` cleanup |
| **Processing & Analytics** | 20% | Groups by store, region, category, payment method; correct revenue per transaction; lambdas + `filter()`/`map()`/`sorted()`; multi-key tuple sorting and set comprehensions; recursive category tree with a clear base case; class-based design; edge cases handled |
| **Storage & Query** | 15% | In-memory store; queryable interface with `**kwargs` filters; `match`/`case` dispatch; properties for safe access; `__str__()`/`__repr__()`, inner result-row class, `@classmethod` factory; custom exceptions for invalid queries; < 100ms query performance |
| **Reporting & Export** | 15% | Readable formatted tables; currency/percents via f-string specifiers with aligned columns; CSV export; `@timed` decorator with `functools.wraps`; timing metadata; context managers for file I/O |
| **Orchestration** | 20% | Full pipeline end-to-end; CSV + API fetched in parallel; graceful error handling (skip bad records, re-raise structural failures); command-line arguments; progress logging; sequential-vs-async Concurrency comparison with speedup |
| **Code Quality** | 10% | Well-organized modules with clear responsibilities; meaningful names; type hints (optional but recommended); helpful error messages; no unused imports or dead code |

### Grading Bands

| Score | Band | Description |
|-------|------|-------------|
| 90–100 | Distinction | Production-quality code, all five modules work, async win is measured and justified, complete documentation |
| 75–89 | Merit | Working system with minor issues (e.g., one module occasionally fails on messy rows, query edge cases), good documentation |
| 60–74 | Pass | Core pipeline works (ingest → aggregate → report), basic regex/validation, partial query or concurrency report |
| 50–59 | Borderline | Partial implementation (e.g., no async client or no recursive tree), memory/query incomplete |
| Below 50 | Fail | Does not demonstrate integrated understanding of Labs 1–23 concepts |

---

## 13. Optional Exercise

Once the golden path works, take it further. Each extension reuses the modules you already built:

1. **Caching & Memoization** — use a `@cache` decorator so repeated fetches don't hit the API again
2. **Database Persistence** — swap the in-memory store for SQLite, and implement SQL queries
3. **Web API** — expose the storage layer as a Flask or FastAPI endpoint
4. **Real-time Streaming** — use a WebSocket or SSE to push live updates to a browser dashboard
5. **Custom DSL** — implement a mini query language (e.g., `"store_id:STORE-123 AND region:Europe"`)
6. **Retry with Backoff** — write a `@retry` decorator factory that retries transient HTTP failures with a delay
7. **Concurrency Variants** — compare async/await vs threading vs multiprocessing on this workload with real timings
8. **Algorithm Profiling** — run the recursive category-tree builder against 3 data sizes and confirm its growth; state the Big-O you expect and whether the measurements agree
9. **Report Style Swap** — reformat the console report with a different string layout (e.g., `str.format()` or padding methods instead of f-strings) to prove you own all three formatting styles

---

## 14. What We Learnt

- **Real data is messy** — normalization is explicit work: regex, `None` identity checks, and `match`/`case`, never truthiness alone (an empty string isn't "missing" yet).
- **Async wins are measurable** — prove them with a sequential baseline and report the speedup instead of assuming.
- **Module boundaries make debugging tractable** — one single-responsibility module per stage (ingest → process → store → report), each testable on its own.
- **Recursion needs a contract** — a clear base case plus a stated depth/Big-O makes recursive code predictable instead of fragile.
- **OOP defaults pay off** — dunder methods, properties, and `@classmethod` factories turn a store into a pleasant library, not a pile of `[]` lookups.
- **Error policy beats hope** — skip-and-log for per-record problems, re-raise only structural failures; long pipelines survive.
- **f-string specifiers own presentation** — know `.zfill`, width/alignment, and `{:,}`/`.2f` so the report formats itself.

---

## Appendix A: Pre-Submission Checklist

Before handing in, verify:

- [ ] All five modules exist in `src/` and import cleanly
- [ ] Golden path runs end-to-end (`python src/main.py --top-n 5`) — output matches Section 6
- [ ] Messy rows are handled per Section 4 (bad price, missing quantity, malformed IDs, messy names)
- [ ] A `store_id` failing `^STORE-\d{3}$` is rejected or repaired — confirmed by test
- [ ] Recursive category tree has a base case and a depth/Big-O comment
- [ ] **Concurrency Report** line prints real sequential-vs-async timings
- [ ] `--region`, `--output`, `--top-n` flags all work
- [ ] `tests/*.py` pass with `pytest` (per TEST.md format)
- [ ] `README.md` explains setup and run steps
- [ ] No secrets, no absolute paths, no unused imports in the code

---

## Appendix B: System Diagram

```mermaid
%%{init: {"theme": "default", "flowchart": {"useMaxWidth": true}}}%%
flowchart TD
    subgraph MAIN["1 - main.py  (orchestrates everything)"]
        direction LR
        ORCH["Orchestrate ingest -> process -> store -> report"]
        CONC["Concurrency Report: sequential vs async"]
    end

    subgraph SOURCES["Data sources"]
        direction LR
        CSV[("store_sales.csv")]
        API[("Mock live API")]
    end

    subgraph M1["2 - ingestion.py"]
        direction LR
        R1["Read CSV lazily"]
        FAS["Async batch fetch, rate-limited"]
        VN["Validate + normalize"]
    end

    subgraph M2["3 - analytics.py"]
        direction LR
        AGG["Aggregate by store / region"]
        RANK["Filter + rank"]
        TREE["Recursive category tree"]
    end

    subgraph M3["4 - storage.py"]
        direction LR
        STORE[("AnalyticsStore")]
        QUERY["query(**filters)"]
    end

    subgraph M4["5 - reporting.py"]
        direction LR
        TAB["Format tables, f-strings"]
        EXP["Export results.csv"]
        TIMED["timed decorator"]
    end

    MAIN --> R1
    MAIN --> FAS
    MAIN --> CONC
    CSV --> R1
    API --> FAS
    R1 --> VN
    FAS --> VN
    VN --> AGG
    AGG --> RANK
    RANK --> TREE
    RANK --> STORE
    STORE --> QUERY
    QUERY --> TAB
    TAB --> EXP

    classDef mainFill fill:#99F6E4,stroke:#0F766E,color:#134E4A;

    classDef srcFill  fill:#E9D5FF,stroke:#7E22CE,color:#4A044E;

    classDef ingFill  fill:#BFDBFE,stroke:#1D4ED8,color:#1E3A8A;

    classDef anaFill  fill:#BBF7D0,stroke:#15803D,color:#14532D;

    classDef stoFill  fill:#FDE68A,stroke:#B45309,color:#78350F;

    classDef repFill  fill:#FECACA,stroke:#B91C1C,color:#7F1D1D;


    class ORCH,CONC mainFill;
    class CSV,API srcFill;
    class R1,FAS,VN ingFill;
    class AGG,RANK,TREE anaFill;
    class STORE,QUERY stoFill;
    class TAB,EXP,TIMED repFill;
``````

---

**You've got this. Build it step by step, test as you go, and you'll have a production-grade data pipeline. Good luck!** 🚀

