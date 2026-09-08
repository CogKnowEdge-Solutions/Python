# Lab 5 Assignment: Comprehensions

This assignment tests what you learned in **Lab 5: Comprehensions**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab5_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-comprehensions.md) and [Section 10 (Step-wise Instructions)](lab-comprehensions.md).

## Concept Questions

**1.** What is a comprehension, and which collection types can it build?

**2.** Explain the difference between a conditional filter (`[x for x in seq if cond]`) and a conditional expression (`[x if cond else y for x in seq]`).

**3.** For each of the three syntaxes below, state which kind of collection it builds:
- `[expr for item in seq]`
- `{expr for item in seq}`
- `{key: value for item in seq}`

## Short Code Tasks

**4.** Write a list comprehension that adds `10` to every number in `[4, 15, 6, 20]`. What does it produce?

**5.** Write a list comprehension that keeps only the **even** numbers from `[1, 2, 3, 4, 5, 6]`. What does it produce?

**6.** Write a dictionary comprehension using `zip()` that maps each name in `names = ["Amy", "Bo"]` to each score in `scores = [85, 72]`. What does it produce?

## Applied Tasks

**7.** Write a set comprehension that collects the unique first letters from `words = ["cat", "dog", "cow", "deer"]`. Explain why the result has fewer than four items.

**8.** Using the lab's parallel lists, write a list comprehension that builds a list of **tuples** `(name, score)` only for students who passed (`score >= 60`). What does it produce for the lab data?

**9.** Rewrite the following loop as a list comprehension:
```python
results = []
for n in range(5):
    results.append(n * n)
```
State the comprehension and the resulting list.

---

## Answer Key

**1.** A comprehension is a single expression that builds a new collection from an existing one. It can build a list (`[...]`), a dictionary (`{key: value for ...}`), or a set (`{expr for ...}`).

**2.** A conditional filter drops items for which the condition is `False` — they never appear. A conditional expression keeps every item but chooses its value (`y` when the condition is false) — so the length is unchanged. One removes items, the other relabels them.

**3.**
- `[expr for item in seq]` → a **list**.
- `{expr for item in seq}` → a **set** (unique values).
- `{key: value for item in seq}` → a **dictionary**.

**4.**
```python
[n + 10 for n in [4, 15, 6, 20]]
```
This produces `[14, 25, 16, 30]`.

**5.**
```python
[n for n in [1, 2, 3, 4, 5, 6] if n % 2 == 0]
```
This produces `[2, 4, 6]`.

**6.**
```python
names = ["Amy", "Bo"]; scores = [85, 72]
{n: s for n, s in zip(names, scores)}
```
This produces `{'Amy': 85, 'Bo': 72}`. `zip()` pairs each name with its matching score, and the comprehension builds the key-value map.

**7.**
```python
words = ["cat", "dog", "cow", "deer"]
{w[0] for w in words}
```
This produces `{'c', 'd'}` — only two items, because `"cat"` and `"cow"` both start with `c`, and `"dog"` and `"deer"` both start with `d`. A set drops the duplicates.

**8.**
```python
[(name, score) for name, score in zip(student_names, scores) if score >= 60]
```
With the lab data this produces `[('Ana', 92), ('Ben', 67), ('Dina', 81), ('Eli', 74)]` — the four passing students; `Clara` (55) is filtered out.

**9.**
```python
results = [n * n for n in range(5)]
```
This produces `[0, 1, 4, 9, 16]`.