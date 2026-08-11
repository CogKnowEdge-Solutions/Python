# Advanced Python

A set of hands-on, self-contained Python labs for an advanced Python curriculum. Each
lab ships as a Jupyter notebook, a companion guide (`.md`), an assignment sheet with an
answer key, and an end-to-end `pytest` suite that executes the notebook in a fresh
kernel and validates the real output.

## Labs

| Lab | Topic | Difficulty |
|-----|-------|------------|
| [Lab 1](Lab1) | Functional Data Wrangling with Lambda Functions | Beginner |
| [Lab 2](Lab2) | The Safe Resource Vault — Context Managers | Beginner |
| [Lab 3](Lab3) | The Memory-Efficient Data Pipeline — Iterators and Generators | Intermediate |
| [Lab 4](Lab4) | The Metaprogramming Toolkit — Decorators, Closures and Caching | Intermediate |

## Repository Structure

```
Advanced python/
├── CONSTITUTION.md   # the rules every lab must follow before it can ship
├── AGENTS.md         # operating procedure for building and validating labs
├── GUIDELINES.md     # writing guide for lab notebooks and guides
├── TEST.md           # the testing framework used to validate each lab
├── Lab1/ … Lab4/     # one folder per lab (notebook, guide, assignment, tests)
└── README.md         # this file
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

This project is licensed under the [MIT License](../LICENSE).
