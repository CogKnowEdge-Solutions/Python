# Lab 7 — File Handling: Text, JSON & CSV: Assignment

---

## Concept Questions

**1.** What is the difference between file modes `'w'` and `'a'`? If a file
already contains `"Product,3"` and you open it with mode `'w'` and write
`"New,5"`, what does the file contain afterwards?

**2.** Why should you use the `with open(...)` context manager rather than
plain `open(...)` followed by `close()`?

**3.** What happens if you call `open("missing.txt", "r")` on a file that does
not exist? What exception is raised, and how would you handle it?

**4.** What is the difference between `csv.reader` and `csv.DictReader`? Which
one uses the first row as a header, and what type does each return per row?

---

## Code Tasks

**Task 1 — Write then read a text file.**

Using a `with open(...)` block, write the string `"Welcome to the shop!\n"` to
a file named `welcome.txt` with mode `'w'` and `encoding="utf-8"`, then read
it back and print it.

**Task 2 — Append a line.**

Write `"First sale\n"` to `sales.txt`, then append `"Second sale\n"` with mode
`'a'`. Read the final file and print how many lines it contains (should be 2).

**Task 3 — Save and load JSON.**

Create a list of two dicts: `{"name": "Mug", "price": 7.25}` and
`{"name": "Shirt", "price": 25.00}`. Use `json.dump` to save it to
`products.json` (with `indent=2`), then use `json.load` to read it back and
print the `price` of the Mug.

**Task 4 — Handle a missing file.**

Write a small `try/except` block that attempts to open `missing.csv` with
mode `'r'`, catches the `FileNotFoundError`, and prints
`"File not found, skipping"` instead of crashing.

**Task 5 — Write a CSV with DictWriter.**

Using `csv.DictWriter`, write a header row plus two rows to `items.csv`.

The fieldnames are `["name", "qty"]`. Rows: `{"name": "Mug", "qty": 4}` and
`{"name": "Shirt", "qty": 2}`. Use `newline=""` in the `open()` call.

**Task 6 — Read CSV back with DictReader.**

Open `items.csv` (as created in Task 5) and use `csv.DictReader` to read it.
Print the `fieldnames` and then each row dict.

---

## Answer Key

### Concept Questions

**1.** Mode `'w'` **overwrites** the file — it creates it if missing or
truncates it to empty if it exists — then writes. Mode `'a'` **appends** —
it creates the file if missing or writes to the end of the existing content.
So opening a file containing `"Product,3"` with `'w'` and writing `"New,5"`
leaves the file containing exactly `"New,5"` (the old content is erased).

**2.** The `with` block automatically calls `close()` when the block ends —
even if an exception is raised inside. With manual `open()` + `close()`, if an
error happens before `close()`, the file handle leaks and the file stays
locked, potentially losing buffered data. `with` makes cleanup guaranteed and
the code shorter.

**3.** It raises a **`FileNotFoundError`**. You handle it by wrapping the
`open()` in a `try/except FileNotFoundError` block and taking alternate
action (e.g., printing a message or creating the file) instead of crashing.

**4.** `csv.reader` returns each row as a **plain list of strings** and does
not treat any row specially. `csv.DictReader` uses the **first row as the
header (fieldnames)** and returns each subsequent row as a **dict** keyed by
those fieldnames. So `DictReader` is friendlier when you need to access
e.g. `row["price"]` by name.

### Code Tasks

**Task 1**

```python
with open("welcome.txt", "w", encoding="utf-8") as f:
    f.write("Welcome to the shop!\n")

with open("welcome.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(content)
```

**Task 2**

```python
with open("sales.txt", "w", encoding="utf-8") as f:
    f.write("First sale\n")

with open("sales.txt", "a", encoding="utf-8") as f:
    f.write("Second sale\n")

with open("sales.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print(len(lines))  # 2
```

**Task 3**

```python
import json

products = [
    {"name": "Mug", "price": 7.25},
    {"name": "Shirt", "price": 25.00},
]

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2)

with open("products.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded[0]["price"])  # 7.25
```

**Task 4**

```python
try:
    with open("missing.csv", "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found, skipping")
```

**Task 5**

```python
import csv

fieldnames = ["name", "qty"]
rows = [
    {"name": "Mug", "qty": 4},
    {"name": "Shirt", "qty": 2},
]

with open("items.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
```

**Task 6**

```python
import csv

with open("items.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print("Fieldnames:", reader.fieldnames)
    for row in reader:
        print(row)
```

Output (expected):

```
Fieldnames: ['name', 'qty']
{'name': 'Mug', 'qty': '4'}
{'name': 'Shirt', 'qty': '2'}
```
