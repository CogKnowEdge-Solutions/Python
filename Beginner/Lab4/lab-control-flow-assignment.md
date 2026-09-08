# Lab 4 Assignment: Control Flow — Conditionals & Loops

This assignment tests what you learned in **Lab 4: Control Flow — Conditionals & Loops**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab4_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-control-flow.md) and [Section 10 (Step-wise Instructions)](lab-control-flow.md).

## Concept Questions

**1.** How does `if/elif/else` decide which branch to run? What happens if *two* branches have a `True` condition?

**2.** When should you use a `for` loop instead of a `while` loop, and vice versa?

**3.** What do `continue` and `break` each do, and why is it useful to pair them in one loop?

**4.** What is the difference between `enumerate()` and `zip()` in terms of what they yield?

## Short Code Tasks

**5.** Write a `final_grade(score)` function using only `if` and `return` (no `elif`/`else`) that returns `"A"` for a score `>= 90` and `"F"` otherwise. (Hint: use two `if` statements with early `return`.)

**6.** Write a `for` loop using `enumerate()` that prints the index and value of each name in `names = ["Zara", "Mia", "Owen"]`. The output should include `0: Zara` and so on.

**7.** Write a `while` loop that counts from `0` to `4` and stops, printing each number. Show the line that prevents the loop from never ending.

**8.** Write a one-line list comprehension that keeps only the numbers **greater than 50** from `[30, 60, 45, 80, 25]`.

## Applied Tasks

**9.** Using the lab's data, write a `for` loop over `zip(student_names, quiz_scores)` that prints each student's name and "PASS"/"FAIL", and stops (`break`) the first time it finds a score `>= 90`. (Refer back to Cells 5 and 6.)

**10.** Rewrite the **final report** to print, for each student, a line only if that student **passed** (`score >= 60`). Use `continue` to skip failing students. Compare with the lab's pass list `['Ana', 'Ben', 'Dina', 'Eli']` and explain how `continue` changes the printed output.

**11.** Explain, in two sentences, why the combination of branching, loops, and `break`/`continue` is described as the "logic backbone" for the rest of the course. Give one future scenario where you would need all three together.

---

## Answer Key

**1.** `if/elif/else` evaluates branches top to bottom and runs only the **first** one whose condition is `True`, then skips all the rest. So even if two conditions are `True`, only the first matching branch runs.

**2.** Use a `for` loop when you want to visit every element of a known sequence (e.g., a list). Use a `while` loop when the number of iterations isn't known in advance and you repeat until a condition becomes `False`.

**3.** `continue` skips the rest of the **current** iteration and moves to the next one; `break` ends the **entire** loop. Pairing them lets a loop skip unwanted items (`continue`) and stop once a goal is reached (`break`), which is exactly what Celss 5 and 6 of the lab demonstrate.

**4.** `enumerate()` yields `(index, value)` pairs for a single sequence, so you get positions. `zip()` yields paired elements from two (or more) sequences, lining up parallel data without index arithmetic.

**5.**
```python
def final_grade(score):
    if score >= 90:
        return "A"
    if score < 90:  # or simply: return "F"
        return "F"
```
Every call returns on the first `if` that matches, so the second `if` handles everything below 90. `final_grade(92)` → `"A"`, `final_grade(55)` → `"F"`.

**6.**
```python
names = ["Zara", "Mia", "Owen"]
for index, name in enumerate(names):
    print(f"{index}: {name}")
```
This prints `0: Zara`, `1: Mia`, `2: Owen`.

**7.**
```python
n = 0
while n < 5:
    print(n)
    n += 1
```
The line `n += 1` advances the counter each pass, so eventually `n < 5` becomes `False` and the loop ends. Without it, the loop would run forever.

**8.**
```python
greater = [num for num in [30, 60, 45, 80, 25] if num > 50]
```
This gives `[60, 80]`.

**9.**
```python
for student_name, score in zip(student_names, quiz_scores):
    status = "PASS" if final_grade(score) != "F" else "FAIL"
    print(f"{student_name}: {status}")
    if score >= 90:
        print(f"{student_name} is the top scorer — stopping.")
        break
```
This prints `Ana: PASS` and stops immediately, because `Ana` is the first student with `92 >= 90`.

**10.**
```python
for student_name, score in zip(student_names, quiz_scores):
    if score < 60:
        continue
    print(f"{student_name}: {final_grade(score)}")
```
This prints only passing students — `Ana`, `Ben`, `Dina`, `Eli` — matching the pass list. `continue` skips `Clara`, so she never prints a line. In the lab's version, `continue` had the same effect but `break` stopped the loop at the top scorer; here `continue` alone lets all passing students print.

**11.** Branching decides which path to take, loops repeat work over data, and `break`/`continue` refine how far the loop goes — together they make programs flexible enough to handle real data with varied cases. For example, a program that reads user input until valid, checks conditions per record, and stops early on an error needs branching, a loop, and `break`/`continue` all at once.