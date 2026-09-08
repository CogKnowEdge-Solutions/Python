# Lab 2 Assignment: Strings

This assignment tests what you learned in **Lab 2: Strings**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab2_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-strings.md) and [Section 10 (Step-wise Instructions)](lab-strings.md).

## Concept Questions

**1.** What is a string, and what does the built-in `len()` function tell you about it?

**2.** Explain the difference between indexing and slicing. What do `text[0]`, `text[-1]`, and `text[0:5]` each give you for a string `text = "Python"`?

**3.** What does `find()` return when the text you're looking for is **not** present in the string?

**4.** Why do we prefer f-strings over joining with `+` when building output? (Hint: think about what happens when a value is not a string.)

## Short Code Tasks

**5.** Write a single line that removes whitespace from both ends of `raw = "  Welcome!  "` and prints the result. What value should it print?

**6.** Write code that splits `"apple, banana, cherry"` into a list using `", "` (a comma followed by a space) as the separator, then joins it back into a string with `"-"`. Print both the list and the joined result.

**7.** Write an f-string that stores `temperature = 36.6` and prints it rounded to **two** decimal places.

## Applied Tasks

**8.** Write code that:
- Stores `message = "The quick brown fox"`.
- Prints the first word using slicing (`message[:message.find(" ")]`).
- Prints the last three characters using a negative slice.
- Converts the whole message to uppercase with `upper()` and prints it.

**9.** Explain what happens if you run `"2" + "3"` (two strings) versus `2 + 3` (two integers), and how this connects to why `find()` and `replace()` always operate on strings.

---

## Answer Key

**1.** A string (`str`) is a piece of text wrapped in quotes. `len()` returns the number of characters (including spaces) in the string.

**2.**
- Indexing pulls out a **single character** by position.
- Slicing pulls out a **substring** using `[start:end]`.
- `text[0]` → `"P"`, `text[-1]` → `"n"`, `text[0:5]` → `"Pytho"`.
- `text[-1]` is the last character because negative indexes count back from the end starting at `-1`.

**3.** `find()` returns `-1` when the text is not present.

**4.** f-strings automatically convert values to text, and they read more cleanly. With `+`, you must convert non-string values yourself with `str()`, otherwise you raise a `TypeError` (e.g., `"I am " + 28` fails).

**5.**
```python
print("  Welcome!  ".strip())
```
This prints `Welcome!` — the outer spaces are removed.

**6.**
```python
parts = "apple, banana, cherry".split(", ")
print(parts)
rejoined = "-".join(parts)
print(rejoined)
```
The list is `['apple', 'banana', 'cherry']`; the joined result is `apple-banana-cherry`. Note the separator `", "` must match the string exactly — a comma and a space. Splitting `"apple,banana,cherry"` on `", "` would not split, because there is no space after each comma.

**7.**
```python
temperature = 36.6
print(f"Temperature: {temperature:.2f}")
```
`{temperature:.2f}` rounds to two decimals, printing `36.60`.

**8.**
```python
message = "The quick brown fox"
print(message[:message.find(" ")])
print(message[-3:])
print(message.upper())
```
This prints `The`, then `fox`, then `THE QUICK BROWN FOX`.

**9.** `"2" + "3"` joins the strings into `"23"`, while `2 + 3` adds the integers to give `5`. This shows that `+` behaves differently by type. Since `find()` and `replace()` are string methods, they require a string as their argument and work on the string's character sequence — they have nothing to do with numeric arithmetic.