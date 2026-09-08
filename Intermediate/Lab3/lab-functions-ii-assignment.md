# Lab 3 Assignment: Functions II

This assignment tests what you learned in **Lab 3: Functions II**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab3_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-functions-ii.md) and [Section 10 (Step-wise Instructions)](lab-functions-ii.md).

## Concept Questions

**1.** What does `*args` collect a function's positional arguments into? What does `**kwargs` collect keyword arguments into?

**2.** What is a `lambda`? Give one example, and explain what makes it different from a regular `def` function.

**3.** What is the purpose of the `key=` argument in `sorted(iterable, key=function)`?

**4.** Why do `map()` and `filter()` need to be wrapped in `list(...)` to see their results?

## Short Code Tasks

**5.** Write a function `combine_words(*words: str) -> str` that joins any number of string arguments with a space. Call it with 4 words and print the result.

**6.** Write a lambda `cube` that returns a number raised to the power of 3. Call `cube(3)` and print the result.

**7.** Given `numbers = [4, 1, 7, 3]`, use `sorted()` with a `key=` lambda to sort them in **descending** order (largest first) without using `reverse=True`. (Hint: what happens if the key function negates the number?)

## Applied Tasks

**8.** Write a function `describe_person(name: str, **attributes: str) -> str` that takes a required `name` and any number of additional keyword attributes, and returns a string like `"Ana: age=28, city=Delhi"`. Call it with `name="Ana", age="28", city="Delhi"`.

**9.** Given `scores = [55, 92, 67, 81, 40]`, use `filter()` and a lambda to keep only scores `>= 60`, then use `map()` and a lambda to convert each surviving score into a letter grade string (`"PASS"` for now, or reuse the grading logic style from earlier labs if you like), and print the final list.

**10.** Explain, using the lab's `summarize_order` function as an example, why combining `*args` and `**kwargs` in the *same* function signature is useful. What real-world situation does it mirror?

---

## Answer Key

**1.** `*args` collects positional arguments into a **tuple**. `**kwargs` collects keyword arguments into a **dictionary**.

**2.** A `lambda` is a small, unnamed function written as `lambda parameters: expression`, e.g. `lambda x: x * 2`. Unlike a regular `def` function, a lambda has no name (unless assigned to a variable), is limited to a single expression (no statements, no multiple lines), and automatically returns that expression's value without a `return` keyword.

**3.** `key=function` tells `sorted()` to compare items by calling `function` on each one first, rather than comparing the raw items directly. This lets you sort by one specific field of a more complex item, like a dictionary's `"price"` value.

**4.** `map()` and `filter()` return **lazy iterators**, not lists — they compute values on demand rather than all at once. Wrapping them in `list(...)` forces Python to actually run through the iterator and collect every result into a concrete list you can print, index, or loop over more than once.

**5.**
```python
def combine_words(*words: str) -> str:
    return " ".join(words)

print(combine_words("the", "quick", "brown", "fox"))
```
This prints `the quick brown fox`.

**6.**
```python
cube = lambda x: x ** 3
print(cube(3))
```
This prints `27`.

**7.**
```python
numbers = [4, 1, 7, 3]
descending = sorted(numbers, key=lambda n: -n)
print(descending)
```
This prints `[7, 4, 3, 1]`. Negating each number before comparing means the largest original number becomes the smallest negated number, so ascending order on the negated values produces descending order on the originals.

**8.**
```python
def describe_person(name: str, **attributes: str) -> str:
    parts = [f"{key}={value}" for key, value in attributes.items()]
    return f"{name}: " + ", ".join(parts)

print(describe_person(name="Ana", age="28", city="Delhi"))
```
This prints `Ana: age=28, city=Delhi`.

**9.**
```python
scores = [55, 92, 67, 81, 40]
passing_scores = list(filter(lambda s: s >= 60, scores))
labeled = list(map(lambda s: "PASS", passing_scores))
print(labeled)
```
This prints `['PASS', 'PASS', 'PASS']` — three scores (`92`, `67`, `81`) pass the `>= 60` filter; `55` and `40` are dropped before `map()` ever sees them.

**10.** Combining `*args` and `**kwargs` in one signature mirrors a common real-world shape: "here is a variable-length list of *things*, plus some optional *metadata about the request*." `summarize_order(*item_prices, **order_info)` mirrors exactly this — the prices are the variable-length data being processed, while `customer` and `priority` are metadata *about* that processing that doesn't belong in the same list. Keeping them as separate parameter kinds lets the function tell "the data" and "the options describing what to do with the data" apart without the caller needing to build a combined structure themselves.
