# Lab 4 — Miscellaneous Python Topics: Assignment

---

## Concept Questions

**1.** Why should you use `is None` instead of `== None` when checking whether a
variable is `None`?

**2.** Write a `match`/`case` block that takes a string `"start"`, `"stop"`, or
`"pause"` and prints the corresponding action. Include a default case.

**3.** What is the regex pattern (as a raw string) that would match an email
address of the form `name@domain.com`? Explain each part of the pattern.

**4.** List the three string formatting styles available in Python and give one
advantage of f-strings over the other two.

---

## Code Tasks

**Task 1 — Complete the `match`/`case`.**
Fill in the blanks so the function returns `"Discounted"` when the argument is
`True` and `"Full Price"` when it is `False`.

```python
def price_label(discounted):
    match discounted:
        case _____:
            return "Discounted"
        case _____:
            return "Full Price"
```

**Task 2 — Fix the identity check.**
The code below uses `==` instead of `is`. Change it to the correct form.

```python
x = None
if x == None:
    print("x is None")
```

**Task 3 — Validate a date string.**
Write code that takes the string `"2026-09-02"` and converts it to a
`datetime.date` object using `strptime`. Print the date and its day of the week.

**Task 4 — Regex extraction.**
Given the string `"Order SKU-5512-ZZ placed on 2026-09-02"`, use `re.search`
with a pattern to extract and print just the product code (`SKU-5512-ZZ`).

**Task 5 — Print a receipt line with `.format()`.**
Use `.format()` to print the following line (including the pipe characters):

```
| Widget | 4 x $3.50 | $14.00 |
```

**Task 6 — Monthly totals.**
Given the list below, compute and print the total revenue for month 9 using a
list comprehension or generator expression.

```python
sales = [
    {"month": 9, "amount": 120.00},
    {"month": 8, "amount": 75.50},
    {"month": 9, "amount": 200.25},
    {"month": 9, "amount": 45.00},
]
```

---

## Answer Key

### Concept Questions

**1.** `None` is a singleton — only one `None` object exists in memory. `is`
tests identity (same object), which is the correct semantic. `==` calls
`__eq__` and could be overridden by a custom class to return `True` even when
the object is not actually `None`.

**2.**

```python
def control(action):
    match action:
        case "start":
            print("Starting process")
        case "stop":
            print("Stopping process")
        case "pause":
            print("Pausing process")
        case _:
            print("Unknown action")
```

**3.** `r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"`  
- `[a-zA-Z0-9._%+-]+` — one or more valid local-part characters  
- `@` — literal at sign  
- `[a-zA-Z0-9.-]+` — one or more domain characters  
- `\.` — literal dot before TLD  
- `[a-zA-Z]{2,}` — two or more letters for the TLD

**4.** The three styles are f-strings (`f"..."`), `.format()`, and
`%`-formatting. F-strings are advantage because they are the most readable,
concise, and performant — expressions are evaluated at runtime and embedded
directly, with no extra method call or tuple packing.

### Code Tasks

**Task 1**

```python
def price_label(discounted):
    match discounted:
        case True:
            return "Discounted"
        case False:
            return "Full Price"
```

**Task 2**

```python
x = None
if x is None:
    print("x is None")
```

**Task 3**

```python
from datetime import datetime
d = datetime.strptime("2026-09-02", "%Y-%m-%d").date()
print(d)              # 2026-09-02
print(d.strftime("%A"))  # Wednesday
```

**Task 4**

```python
import re
text = "Order SKU-5512-ZZ placed on 2026-09-02"
match = re.search(r"SKU-\d{4}-[A-Z]{2}", text)
if match:
    print(match.group())  # SKU-5512-ZZ
```

**Task 5**

```python
name, qty, price = "Widget", 4, 3.50
total = qty * price
print("| {} | {} x ${:.2f} | ${:.2f} |".format(name, qty, price, total))
```

**Task 6**

```python
sales = [
    {"month": 9, "amount": 120.00},
    {"month": 8, "amount": 75.50},
    {"month": 9, "amount": 200.25},
    {"month": 9, "amount": 45.00},
]
total = sum(s["amount"] for s in sales if s["month"] == 9)
print(f"Month 9 total: ${total:.2f}")  # Month 9 total: $365.25
```
