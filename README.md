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

Each lab folder ships four files: the Jupyter notebook, the companion guide (`.md`),
the assignment sheet with answer key, and the `pytest` suite that validates the lab.

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

## Repository Structure

```
Advanced_Python/
├── CONSTITUTION.md   # the rules every lab must follow before it can ship
├── AGENTS.md         # operating procedure for building and validating labs
├── GUIDELINES.md     # writing guide for lab notebooks and guides
├── TEST.md           # the testing framework used to validate each lab
├── Lab1/ … Lab4/     # one folder per lab (notebook, guide, assignment, tests)
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

## License

This project is licensed under the [MIT License](LICENSE).
