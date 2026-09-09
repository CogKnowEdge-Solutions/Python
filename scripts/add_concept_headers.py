"""Replace '## Step N — Topic' headings with concept headings + 1-2 line docs.

Affected: Intermediate Labs 4, 5, 6 — where each cell demonstrates an
independent concept (not a sequential build), so 'Step N' is misleading and the
cell previously had no explanation text.
"""
import json
import glob
import re

# NOTEBOOK -> ordered list of (pattern to match in cell markdown, new source)
# new source is a list of lines. Pattern is a substring/regex of the heading.
REPLACEMENTS = {
    "Lab4": [
        (r"Step 1 — `match`/`case` Pattern Matching",
         "## `match`/`case` pattern matching\n\n"
         "Python 3.10+ `match`/`case` branches on the *shape* of a value, not "
         "just its equality — a cleaner alternative to a long `if`/`elif` chain.\n"),
        (r"Step 2 — `None` Checks and Defaults",
         "## `None` checks and defaults\n\n"
         "`None` means \"missing\". Fill each missing field with a safe default "
         "so downstream code never trips over an empty value.\n"),
        (r"Step 3 — Identity Checks \(`is` vs `==`\)",
         "## Identity checks: `is` vs `==`\n\n"
         "`is` compares identity (same object); `==` compares value and can be "
         "overridden. Always test for `None` with `is None`, never `== None`.\n"),
        (r"Step 4 — User Input Handling \(Simulated\)",
         "## User input handling (simulated)\n\n"
         "`input()` always returns a string. Strip whitespace and cast to the "
         "right type (`float`, `int`) before trusting it.\n"),
        (r"Step 5 — `range\(\)` and the `array` Module",
         "## `range()` and the `array` module\n\n"
         "`range()` yields a lazy sequence of integers without a full list; "
         "`array` stores numbers in a compact typed layout.\n"),
        (r"Step 6 — Working with Dates",
         "## Working with dates\n\n"
         "`datetime.date.today()` returns today's date; `strftime` format codes "
         "control how it displays.\n"),
        (r"Step 7 — Regular Expressions",
         "## Regular expressions\n\n"
         "A regex like `SKU-\\d{4}-[A-Z]{2}` validates text patterns in one "
         "declarative expression, which is far shorter than manual checks.\n"),
        (r"Step 8 — Seed Data and Combining Records",
         "## Seed data and combining records\n\n"
         "Keep the running dataset as a list of dicts, then `append` new records "
         "so every later report sees the full history.\n"),
        (r"Step 9 — String Formatting: f-strings",
         "## String formatting: f-strings\n\n"
         "f-strings put values directly inside a string — Python's modern "
         "default, ideal for building readable receipts.\n"),
        (r"Step 10 — String Formatting: `\.format\(\)`",
         "## String formatting: `.format()`\n\n"
         "`.`format()` fills named `{}` placeholders — useful for template "
         "strings or where the format string is reused.\n"),
        (r"Step 11 — String Formatting: `%`-Formatting",
         "## String formatting: `%`-formatting\n\n"
         "The oldest style uses `%` placeholders; you'll meet it in legacy code, "
         "so learn to read and write it.\n"),
        (r"Step 12 — Monthly Summary",
         "## Monthly summary\n\n"
         "Filter the records to one month, sum revenue, and guard the average "
         "against division by zero.\n"),
    ],
    "Lab5": [
        (r"Step 1 — Basic try/except",
         "## Basic try/except\n\n"
         "Wrap a risky conversion like `float()` in `try`, and `except ValueError` "
         "to return a safe fallback instead of crashing.\n"),
        (r"Step 2 — Multiple Specific Exceptions",
         "## Multiple specific exceptions\n\n"
         "Stack several `except` clauses to give each error type its own "
         "handling — always catch the narrowest exception you expect.\n"),
        (r"Step 3 — try/finally Cleanup",
         "## try/finally cleanup\n\n"
         "`finally` runs whether the `try` succeeds or raises, so it's the right "
         "place for cleanup like closing files.\n"),
        (r"Step 4 — Custom Exception: InvalidOrderError",
         "## Custom exception: InvalidOrderError\n\n"
         "Subclass `Exception` to name a domain error and carry extra fields, "
         "separating business-rule failures from runtime errors.\n"),
        (r"Step 5 — Re-raising Errors",
         "## Re-raising errors\n\n"
         "`raise` inside an `except` (bare, no arguments) logs or inspects the "
         "error, then lets it keep propagating with its traceback.\n"),
        (r"Step 6 — Robust Order Validation",
         "## Robust order validation\n\n"
         "Collect *all* validation errors before raising one rich error, so the "
         "caller sees every problem in a single pass.\n"),
    ],
    "Lab6": [
        (r"Step 1 — Recursive Factorial",
         "## Recursive factorial\n\n"
         "A recursive function calls itself on a smaller input until a base case "
         "— here `n <= 1` — stops the descent.\n"),
        (r"Step 2 — Recursive Fibonacci",
         "## Recursive Fibonacci\n\n"
         "Each call branches into two (`F(n-1) + F(n-2)`), recomputing the same "
         "subproblems many times — the cost of naive recursion.\n"),
        (r"Step 3 — Recursive Sum of Inventory Prices",
         "## Recursive sum of inventory prices\n\n"
         "Split a list into `head` + `tail`, adding the head to a recursive call "
         "on the tail until the list is empty.\n"),
        (r"Step 4 — Linear Search",
         "## Linear search\n\n"
         "Scan every element from left to right until the target is found; "
         "return its index or `-1`. Simple, works on unsorted data.\n"),
        (r"Step 5 — Bubble Sort",
         "## Bubble sort\n\n"
         "Repeatedly swap adjacent out-of-order pairs so the largest value "
         "\"bubbles\" to the end each pass. Easy to learn, O(n²) — rarely used.\n"),
        (r"Step 6 — Palindrome Checker \(Recursive\)",
         "## Palindrome checker (recursive)\n\n"
         "Compare the outermost characters, then shrink inward; all pairs "
         "matching means the text reads the same forwards and backwards.\n"),
        (r"Step 7 — Practical Scenario: Recursive Binary Search",
         "## Practical scenario: recursive binary search\n\n"
         "On sorted data, halve the search range each call — O(log n), far "
         "faster than linear search.\n"),
    ],
}


def process(nb_path, replacements):
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    changed = 0
    matched_cells = set()
    for cell in nb["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        full = "".join(cell["source"])
        for pat, new_source in replacements:
            if re.search(pat, full):
                # split into a list of lines, each retaining its trailing newline
                lines = new_source.splitlines(keepends=True)
                cell["source"] = lines if lines else [""]
                changed += 1
                matched_cells.add(pat)
                break
    if changed:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write("\n")
    print(f"{nb_path.split(chr(92))[-1]}: changed {changed} cell(s)")
    # report unmatched patterns
    found_pats = {p for p, _ in replacements}
    for p in found_pats - set(matched_cells):
        print(f"   !! no match for: {p}")
    return changed


base = r"C:\Users\Dell\Downloads\Basic_Python\Intermediate"
for lab in ["Lab4", "Lab5", "Lab6"]:
    nb_path = glob.glob(base + f"\\{lab}\\*.ipynb")[0]
    process(nb_path, REPLACEMENTS[lab])
print("done")
