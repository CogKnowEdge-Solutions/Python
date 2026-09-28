# Python Learning Labs

A structured, lab-based curriculum for learning Python end to end — from
beginner fundamentals through intermediate object-oriented programming to
advanced production patterns (concurrency, async, generators, metaprogramming).
Each lab is a self-contained Jupyter notebook (`lab-<topic>.ipynb`) paired
with a markdown guide, a knowledge-check assignment with an answer key, and a
standalone `pytest` suite that validates the lab's real output.

## Project Structure

```
├── Beginner/                   # Beginner labs (6)
│   ├── Lab1/  lab-variables-data-types-operators
│   ├── Lab2/  lab-strings
│   ├── Lab3/  lab-collections
│   ├── Lab4/  lab-control-flow
│   ├── Lab5/  lab-comprehensions
│   └── Lab6/  lab-student-report-generator
├── Intermediate/               # Intermediate labs (10)
│   ├── Lab1/   lab-functions-scope
│   ├── Lab2/   lab-imports-modules
│   ├── Lab3/   lab-functions-ii
│   ├── Lab4/   lab-miscellaneous-topics
│   ├── Lab5/   lab-error-handling
│   ├── Lab6/   lab-recursion-algorithms
│   ├── Lab7/   lab-file-handling
│   ├── Lab8/   lab-oop-core-concepts
│   ├── Lab9/   lab-oop-advanced-tools
│   └── Lab10/  lab-school-management-system
├── Advanced/                   # Advanced labs (7)
│   ├── Lab1/  lab-functional-data-wrangling
│   ├── Lab2/  lab-safe-resource-vault
│   ├── Lab3/  lab-memory-efficient-data-pipeline
│   ├── Lab4/  lab-metaprogramming-toolkit
│   ├── Lab5/  lab-async-api-fetcher
│   ├── Lab6/  lab-concurrency-models
│   └── Lab7/  lab-ultimate-async-data-stream
├── Capstone/                   # Course-wide capstone project (solve-it-yourself)
├── scripts/                    # Tooling (pytest-to-xlsx converter)
├── test-results/               # JUnit XML + .xlsx reports per lab
├── AGENTS.md                   # Instructions for AI coding agents
├── CLAUDE.md                   # Instructions for Claude Code
├── CONSTITUTION.md             # Project rules and constraints
├── GUIDELINES.md               # Lab-writing guidelines
├── TEST.md                     # Comprehensive testing guide
├── README.md                   # this file
└── LICENSE                     # MIT
```

## Lab Contents

Each lab ships four files (Advanced labs add an Excel test-results workbook in
their folder):

| File | Purpose |
|------|---------|
| `lab-<topic>.ipynb` | Interactive Jupyter notebook with step-by-step lessons |
| `lab-<topic>.md` | Markdown version of the lab guide (all 12 sections) |
| `lab-<topic>-assignment.md` | Knowledge-check exercises with an answer key |
| `test_<topic>.py` | Standalone pytest test suite validating the lab's exercises |

## Difficulty Levels

- **Beginner** — No prerequisites. Variables, data types, operators, strings,
  collections, control flow, comprehensions, plus a mini project.
- **Intermediate** — Requires the Beginner series. Functions and scope,
  modules, error handling, recursion, file handling, and OOP.
- **Advanced** — Requires the Intermediate series. Lambdas and functional
  pipelines, context managers, iterators/generators, decorators, `asyncio`,
  threading vs multiprocessing, and a capstone async data stream.

## Beginner Labs

| Lab | Topic | Time |
|-----|-------|------|
| [Lab 1](Beginner/Lab1) | Variables, Data Types & Operators | ~20 min |
| [Lab 2](Beginner/Lab2) | Strings | ~20 min |
| [Lab 3](Beginner/Lab3) | Collections | ~25 min |
| [Lab 4](Beginner/Lab4) | Control Flow | ~25 min |
| [Lab 5](Beginner/Lab5) | Comprehensions | ~25 min |
| [Lab 6](Beginner/Lab6) | Student Report Generator (Mini Project) | ~30 min |

## Intermediate Labs

| Lab | Topic | Time |
|-----|-------|------|
| [Lab 1](Intermediate/Lab1) | Functions & Scope | ~25 min |
| [Lab 2](Intermediate/Lab2) | Imports & Modules | ~30 min |
| [Lab 3](Intermediate/Lab3) | Functions II | ~30 min |
| [Lab 4](Intermediate/Lab4) | Miscellaneous Topics | ~35 min |
| [Lab 5](Intermediate/Lab5) | Error Handling | ~30 min |
| [Lab 6](Intermediate/Lab6) | Recursion & Algorithms | ~35 min |
| [Lab 7](Intermediate/Lab7) | File Handling | ~35 min |
| [Lab 8](Intermediate/Lab8) | OOP I: Core Concepts | ~25 min |
| [Lab 9](Intermediate/Lab9) | OOP II: Advanced Class Tools | ~25 min |
| [Lab 10](Intermediate/Lab10) | School Management System (Capstone) | ~40 min |

## Advanced Labs

| Lab | Topic | Time |
|-----|-------|------|
| [Lab 1](Advanced/Lab1) | Functional Data Wrangling with Lambda Functions | ~25 min |
| [Lab 2](Advanced/Lab2) | The Safe Resource Vault — Context Managers | ~25 min |
| [Lab 3](Advanced/Lab3) | The Memory-Efficient Data Pipeline — Iterators and Generators | ~40 min |
| [Lab 4](Advanced/Lab4) | The Metaprogramming Toolkit — Decorators, Closures and Caching | ~40 min |
| [Lab 5](Advanced/Lab5) | The Async API Fetcher — Concurrency in Action with `asyncio` | ~40 min |
| [Lab 6](Advanced/Lab6) | Threading vs Multiprocessing vs asyncio — Which Concurrency Tool When? | ~45 min |
| [Lab 7](Advanced/Lab7) | The Ultimate Async Data Stream (Capstone) | ~50 min |

Each Advanced lab ships a `lab<N>_test_results.xlsx` with per-test pass/fail
results, durations, and failure messages. Lab 6 additionally ships a
`workloads.py` companion module so its worker *processes* can import the
workloads by name.

## Capstone Project

After finishing all three sections, the course-wide capstone lives in
[`Capstone/`](Capstone/) — a **solve-it-yourself** real-time data analytics
dashboard that integrates every lab's topics. Read
[`CAPSTONE_PROJECT.md`](Capstone/CAPSTONE_PROJECT.md) (the full spec), then
run [`CAPSTONE_SETUP.ipynb`](Capstone/CAPSTONE_SETUP.ipynb) to bootstrap the
project's data files and templates.

## Getting Started

### Prerequisites

- Python 3.10+
- Jupyter (Notebook or VS Code with the Jupyter extension)

### Install Dependencies

Open any notebook and run the **first cell**, which installs all required
modules with pinned versions. Or, from inside a lab folder:

```bash
python -m venv .venv
# Windows:        .venv\Scripts\activate
# macOS / Linux:  source .venv/bin/activate

pip install notebook pytest ipykernel
```

### Running a Lab

```bash
jupyter notebook Beginner/Lab1/lab-variables-data-types-operators.ipynb
```

Or open the file in VS Code and run cells from top to bottom.

### Doing an Assignment

1. Read the `lab-<topic>-assignment.md` file.
2. Attempt the exercises in a fresh notebook or script.
3. Check your answers against the answer key at the end of the file.
4. Run the lab's tests to validate your solutions:

```bash
pytest Beginner/Lab1/test_variables_data_types_operators.py -v
```

## Testing

Tests are written as standalone pytest files (one per lab) and follow the
framework in `TEST.md`. Each test run is reported both as console output and as
an `.xlsx` workbook for reviewability.

Run the whole suite:

```bash
pytest Beginner Intermediate Advanced -v
```

Generate an `.xlsx` report:

```bash
pytest <test_file>.py --junitxml=test-results/junit-<lab>.xml
python scripts/pytest_to_xlsx.py test-results/junit-<lab>.xml test-results/test_<lab>_<YYYY-MM-DD>.xlsx
```

### Test Results

The Advanced catalog's own test run is fully passing — all 135 tests across
all 7 labs:

| Lab | Tests | Status |
|-----|-------|--------|
| Lab 1 | 23/23 | PASS |
| Lab 2 | 19/19 | PASS |
| Lab 3 | 19/19 | PASS |
| Lab 4 | 20/20 | PASS |
| Lab 5 | 17/17 | PASS |
| Lab 6 | 14/14 | PASS |
| Lab 7 | 23/23 | PASS |

Beginner and Intermediate labs keep their JUnit XML + `.xlsx` test reports in
`test-results/`.

## Contributing

This repository follows the rules in `CONSTITUTION.md`. Before creating or
editing a lab:

1. Read `CONSTITUTION.md`, `AGENTS.md`, and `GUIDELINES.md`.
2. Determine the difficulty level and use the line reference to scope the lab.
3. Follow the 12-section structure defined in Article I.
4. Validate the lab against the five gates described in `AGENTS.md` before
   publishing.

## License

This project is licensed under the [MIT License](LICENSE).