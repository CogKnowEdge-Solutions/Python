# Lab 3 Assignment: Collections — Lists, Dictionaries, Tuples & Sets

This assignment tests what you learned in **Lab 3: Collections — Lists, Dictionaries, Tuples & Sets**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab3_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-collections.md) and [Section 10 (Step-wise Instructions)](lab-collections.md).

## Concept Questions

**1.** For each of the four collection types — list, dict, tuple, set — in one line state what it is best used for.

**2.** What is the key difference between a list and a tuple in terms of mutability? Why does that make tuples good for course configuration?

**3.** What makes a set different from a list regarding duplicates and order? Give one operation a set supports more efficiently than a list.

**4.** What is the difference between `grades["Eve"]` and `grades.get("Eve", "none")` in the lab?

## Short Code Tasks

**5.** Write code that creates a list of three colors, appends a fourth, and prints the list.

**6.** Write code that builds a one-entry dict mapping `"course"` to `"Data Science"`, adds a key `"credits"` with value `3`, then prints the value for `"course"`.

**7.** Write a single line that checks whether `"math"` is in the set `{"math", "stats", "python"}` and print the result (`True` or `False`).

## Applied Tasks

**8.** Using the gradebook from the lab, write code that:
- Adds `"Omar"` with `73` and `"Lena"` with `96` to the `grades` dict.
- Computes and prints the new class average (rounded to two decimals).

**9.** Write code that stores a course record `("Intro to Data", 3, 25)` and unpacks it into `course_name`, `credit_hours`, and `max_seats`. Then use an f-string to print a sentence like `"Intro to Data has 3 credits and 25 seats"`. Explain in one sentence why unpacking works.

**10.** Explain how the lab decides *when to use* each structure, and give a real-world example of a data shape that fits each of the four.

---

## Answer Key

**1.** List: ordered sequences that change over time. Dict: mapping keys to values for fast name-based lookup. Tuple: immutable, fixed records. Set: storing unique values and answering membership questions quickly.

**2.** A list is **mutable** (you can add or change items in place); a tuple is **immutable** (it cannot be changed after creation). Because a tuple cannot be modified, it is safe for fixed settings like a course's configuration — nothing can accidentally alter it.

**3.** A list allows duplicates and preserves order; a set drops duplicates and (broadly) has no guaranteed order. A set supports the membership test `item in my_set` efficiently, without scanning the whole collection.

**4.** `grades["Eve"]` raises a `KeyError` if `"Eve"` is absent, whereas `grades.get("Eve", "none")` returns the default value `"none"` instead of crashing.

**5.**
```python
colors = ["red", "blue", "green"]
colors.append("yellow")
print(colors)
```
This prints `['red', 'blue', 'green', 'yellow']`.

**6.**
```python
course = {"course": "Data Science"}
course["credits"] = 3
print(course["course"])
```
This prints `Data Science`.

**7.**
```python
print("math" in {"math", "stats", "python"})
```
This prints `True`.

**8.**
```python
grades = {"Ana": 88, "Ben": 80, "Clara": 91, "Dina": 85}
grades["Omar"] = 73
grades["Lena"] = 96
total = sum(grades.values())
average = total / len(grades)
print(f"Class average: {average:.2f}")
```
Total is `513`, divided by `6` = `85.5`, so it prints `Class average: 85.50`.

**9.**
```python
course_info = ("Intro to Data", 3, 25)
course_name, credit_hours, max_seats = course_info
print(f"{course_name} has {credit_hours} credits and {max_seats} seats")
```
This prints `Intro to Data has 3 credits and 25 seats`. Unpacking works because the tuple's length matches the number of variables on the left, and Python assigns each element to a variable in order.

**10.** The lab chooses by what the data represents and what operations are needed: order and change → list; lookup by name → dict; fixed record → tuple; uniqueness/membership → set. Examples: a leaderboard order → list; a contact's phone number by name → dict; a product's immutable specs → tuple; the set of distinct tags on a post → set.