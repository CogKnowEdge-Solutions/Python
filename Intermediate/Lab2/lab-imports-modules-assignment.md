# Lab 2 Assignment: Imports & Modules

This assignment tests what you learned in **Lab 2: Imports & Modules**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab2_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-imports-modules.md) and [Section 10 (Step-wise Instructions)](lab-imports-modules.md).

## Concept Questions

**1.** What is a module? What is the "standard library"?

**2.** Name the three import styles covered in the lab and give one example line of code for each.

**3.** What is the difference between `import math` and `from math import sqrt`? Specifically, how would you call the square root function differently under each?

**4.** Why might a lab print `"Is it a valid roll? True"` instead of just printing the exact dice roll value?

## Short Code Tasks

**5.** Write code that imports `math` and prints `math.pi` rounded to 2 decimal places using an f-string format spec.

**6.** Write code that imports `date` and `timedelta` from `datetime`, creates a date for `2026-12-25`, and prints the date exactly 10 days before it.

**7.** Write code using `random.choice()` that picks one random item from `["rock", "paper", "scissors"]` and prints it.

## Applied Tasks

**8.** Write a function `area_of_circle(radius: float) -> float` that uses `math.pi` and returns the area, rounded to 2 decimal places. Call it with `radius=3` and print the result.

**9.** Using `datetime`, write code that computes how many days remain between today's date (`date(2026, 9, 1)`) and the end of the year (`date(2026, 12, 31)`), and prints the result as `"X days remaining in the year."`

**10.** Explain why `random.shuffle()` is described in the lab as modifying a list "in place." What would you expect `shuffled_names = sample_names.copy()` followed by `random.shuffle(shuffled_names)` to do to the *original* `sample_names` list, and why does the lab do the `.copy()` step at all?

---

## Answer Key

**1.** A module is a Python file full of pre-written functions, constants, and classes you can reuse via `import`. The standard library is the collection of modules that ships with Python itself, with no extra installation required.

**2.**
- `import math` — whole-module import, accessed with a prefix: `math.sqrt(16)`.
- `from math import sqrt` — imports a specific name directly: `sqrt(16)`, no prefix.
- `import datetime as dt` — whole-module import under a shorter alias: `dt.date(2026, 1, 1)`.

**3.** `import math` requires the `math.` prefix every time you call something from it: `math.sqrt(16)`. `from math import sqrt` imports `sqrt` directly into your code's namespace, so you call it as `sqrt(16)` with no prefix. Both call the exact same underlying function — they only differ in how you refer to it.

**4.** Because `random`-based values are different every time the program runs, printing the exact value in a lab's expected output would make it impossible to verify correctness on a different run. Printing a `True`/`False` check of a *property* (like "is this number between 1 and 6") verifies the result is valid regardless of which specific value came out.

**5.**
```python
import math
print(f"{math.pi:.2f}")
```
This prints `3.14`.

**6.**
```python
from datetime import date, timedelta
christmas = date(2026, 12, 25)
ten_days_before = christmas - timedelta(days=10)
print(ten_days_before)
```
This prints `2026-12-15`.

**7.**
```python
import random
print(random.choice(["rock", "paper", "scissors"]))
```
This prints one of `rock`, `paper`, or `scissors` — the exact value differs each run.

**8.**
```python
import math

def area_of_circle(radius: float) -> float:
    return round(math.pi * radius ** 2, 2)

print(area_of_circle(3))
```
This prints `28.27`.

**9.**
```python
from datetime import date

today = date(2026, 9, 1)
year_end = date(2026, 12, 31)
days_remaining = (year_end - today).days
print(f"{days_remaining} days remaining in the year.")
```
This prints `121 days remaining in the year.`

**10.** `random.shuffle()` modifies the list it's given directly — it doesn't return a new shuffled list, it reorders the existing one and returns `None`. If the lab had called `random.shuffle(sample_names)` directly (without `.copy()` first), it would have permanently reordered `sample_names` itself, which the lab wants to keep in its original order for the "Original order" printout. `.copy()` creates a separate list so the shuffle only affects `shuffled_names`, leaving `sample_names` untouched.
