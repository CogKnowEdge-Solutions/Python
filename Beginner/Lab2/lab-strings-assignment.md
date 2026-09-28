# Lab 2 Assignment: Strings

This assignment tests what you learned in **Lab 2: Strings**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab2_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-strings.md) and [Section 10 (Step-wise Instructions)](lab-strings.md).

## Concept Questions

**1.** What is a string, and what does the built-in `len()` function tell you about it?

**2.** Explain the difference between indexing and slicing. Then, for the string `text = "Python"`, state what each of these returns **and why** — say which value is the `start`, which is the `end`, and whether the `end` character is included: `text[0]`, `text[-1]`, `text[0:5]`, `text[5:]`, `text[-3:]`. Finish by explaining what changes when the `end` value is **too large** (say, `text[0:99]`) compared with a single index that is too large (`text[99]`) — does one of them raise an error?

**3.** What does `find()` return when the text you're looking for is **not** present in the string?

**4.** Why do we prefer f-strings over joining with `+` when building output? (Hint: think about what happens when a value is not a string.)

## Short Code Tasks

**5.** Write a single line that removes whitespace from both ends of `raw = "  Welcome!  "` and prints the result. What value should it print?

**6.** Using only slicing, print the year out of `filename = "report_2026_final.pdf"`, and print the file extension (`.pdf`). For each slice you write, name which part is the `start` and which is the `end`. Then say what `filename[0:99]` returns and why it is not an error.

**7.** Write code that splits `"apple, banana, cherry"` into a list using `", "` (a comma followed by a space) as the separator, then joins it back into a string with `"-"`. Print both the list and the joined result.

**8.** Write an f-string that stores `temperature = 36.6` and prints it rounded to **two** decimal places.

## Applied Tasks

**9.** Write code that:
- Stores `message = "The quick brown fox"`.
- Prints the first word using slicing (`message[:message.find(" ")]`).
- Prints the last three characters using a negative slice.
- Converts the whole message to uppercase with `upper()` and prints it.
- Prints what `message[0:99]` gives, and what a single index such as `message[99]` would do.

**10.** Explain what happens if you run `"2" + "3"` (two strings) versus `2 + 3` (two integers), and how this connects to why `find()` and `replace()` always operate on strings.

---

## Answer Key

**1.** A string (`str`) is a piece of text wrapped in quotes. `len()` returns the number of characters (including spaces) in the string.

**2.**
- Indexing (`text[i]`) pulls out a **single character** by position; slicing (`text[start:end]`) pulls out a **run** of characters.
- In a slice, `start` is the **first character kept** and `end` is the **first character dropped** — the `end` character is never part of the result.
- Omitting `start` means "from the beginning" (`0`); omitting `end` means "to the end of the string".
- A negative index counts back from the end: `-1` is the last character.

For `text = "Python"` (positions `0`–`5`):

| Expression | `start` | `end` | Why | Result |
|---|---|---|---|---|
| `text[0]` | `0` | — | indexing, not slicing — one position only | `"P"` |
| `text[-1]` | `-1` | — | `-1` is the last character | `"n"` |
| `text[0:5]` | `0` | `5` | keep positions `0`–`4`; position `5` (`"n"`) is excluded | `"Pytho"` |
| `text[5:]` | `5` | omitted | from position `5` to the end — one character | `"n"` |
| `text[-3:]` | `-3` | omitted | from 3-from-the-end (`"h"`) to the end | `"hon"` |

**Out-of-range bounds:** `text[0:99]` returns `"Python"` — no error. In a slice, an `end` past the last character simply means "to the end", because the slice always produces *something*. A single index has no such fallback: `text[99]` raises `IndexError: string index out of range`, because it claims a character at a position that does not exist. Related cases: a `start` past the end (`text[99:]`) or an `end` before the `start` (`text[3:1]`) return the empty string `""`, not an error.

**3.** `find()` returns `-1` when the text is not present.

**4.** f-strings automatically convert values to text, and they read more cleanly. With `+`, you must convert non-string values yourself with `str()`, otherwise you raise a `TypeError` (e.g., `"I am " + 28` fails).

**5.**
```python
print("  Welcome!  ".strip())
```
This prints `Welcome!` — the outer spaces are removed.

**6.**
```python
filename = "report_2026_final.pdf"
print(filename[7:11])   # start = 7, end = 11
print(filename[-4:])    # start = -4, no end
print(filename[0:99])   # end is far past the last character
```
`filename[7:11]` prints `2026` — `start` `7` is the first `"2"` and `end` `11` is the underscore *after* `2026`, which is dropped. `filename[-4:]` prints `.pdf` — `start` `-4` counts back from the end to the `"."`, and with no `end` it runs to the final `"f"`. `filename[0:99]` prints the whole `report_2026_final.pdf`: an oversized `end` is treated as "to the end", so the slice degrades gracefully instead of raising.

**7.**
```python
parts = "apple, banana, cherry".split(", ")
print(parts)
rejoined = "-".join(parts)
print(rejoined)
```
The list is `['apple', 'banana', 'cherry']`; the joined result is `apple-banana-cherry`. Note the separator `", "` must match the string exactly — a comma and a space. Splitting `"apple,banana,cherry"` on `", "` would not split, because there is no space after each comma.

**8.**
```python
temperature = 36.6
print(f"Temperature: {temperature:.2f}")
```
`{temperature:.2f}` rounds to two decimals, printing `36.60`.

**9.**
```python
message = "The quick brown fox"
print(message[:message.find(" ")])
print(message[-3:])
print(message.upper())
print(message[0:99])   # oversized end -> the whole string, no error
# print(message[99])   # IndexError: string index out of range
```
This prints `The`, then `fox`, then `THE QUICK BROWN FOX`, then `The quick brown fox`. In the first line, `find(" ")` returns the index of the first space and that index becomes the `end` value, so the slice stops just before the space. The last two lines show the asymmetry: the slice with `end = 99` returns everything, while a single index of `99` raises `IndexError` because position `99` does not exist.

**10.** `"2" + "3"` joins the strings into `"23"`, while `2 + 3` adds the integers to give `5`. This shows that `+` behaves differently by type. Since `find()` and `replace()` are string methods, they require a string as their argument and work on the string's character sequence — they have nothing to do with numeric arithmetic.