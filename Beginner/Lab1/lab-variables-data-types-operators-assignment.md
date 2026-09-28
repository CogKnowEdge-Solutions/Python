# Lab 1 Assignment: Variables, Data Types & Operators

This assignment tests what you learned in **Lab 1: Variables, Data Types & Operators**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab1_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-variables-data-types-operators.md) and [Section 10 (Step-wise Instructions)](lab-variables-data-types-operators.md).

## Concept Questions

**1.** What is a variable? Give a one-line definition and a simple example of storing a value in one.

**2.** Name the four core data types covered in the lab and give one example value for each.

**3.** What does the built-in `type()` function do? Why is it useful to check a variable's type?

**4.** What is the difference between `=` and `==`?

**5.** What is **type casting**? Name the function you would use to (a) turn the number `28` into text, and (b) turn the text `"28"` back into a number. Does casting change the original value?

## Short Code Tasks

**6.** Write code that stores your favorite number in a variable named `favorite_number`, then prints its type using `type()`.

**7.** Write code that computes `20 / 3` and stores it in `result`, then prints `result`. What data type is `result`? (Hint: division always produces one particular type in Python.)

**8.** Write a single line using a **comparison operator** that checks whether the number `100` is less than `50`. What does that line evaluate to?

## Applied Tasks

**9.** Using the budget example from the lab, write code that:
- Stores a balance of `200.75` and a purchase price of `199.99`.
- Computes the remaining balance after the purchase.
- Prints `"Can afford"` if the balance is greater than or equal to the price, and `"Cannot afford"` otherwise.

**10.** Explain why the lab converts numbers to strings with `str()` before joining them into a message with `+`. What would happen if you wrote `"I am " + 28 + " years old"` without `str()`? Then answer: what does `int(3.9)` return, and what does `int("3.9")` do?

---

## Answer Key

**1.** A variable is a named box in memory that holds a value. Example: `my_score = 95` stores the value `95` in the box named `my_score`.

**2.** The four core types are:
- `str` (string): `"Ana"`
- `int` (integer): `28`
- `float`: `500.50`
- `bool` (boolean): `True`

**3.** `type()` returns the data type of the value passed to it, e.g. `type("Ana")` returns `str`. It is useful because operators behave differently on different types, so knowing the type helps you predict how a value will behave.

**4.** `=` is the assignment operator — it stores a value into a variable (`x = 5`). `==` is the equality comparison operator — it compares two values and returns a `bool` (`x == 5` returns `True`).

**5.** Type casting is asking Python to treat a value as a different type, by calling the type you want.
- (a) `str(28)` returns the text `"28"`.
- (b) `int("28")` returns the number `28`.

Casting does **not** change the original value. It returns a brand-new value of the new type, so both can exist at once — `student_age` stays an `int` while `age_as_text` is a `str`.

**6.**
```python
favorite_number = 7
print(type(favorite_number))
```
This prints `<class 'int'>`.

**7.**
```python
result = 20 / 3
print(result)
```
Division (`/`) always produces a `float` in Python, so `result` is a `float`.

**8.**
```python
100 < 50
```
This evaluates to `False`, because comparison operators always return a `bool`.

**9.**
```python
balance = 200.75
price = 199.99
remaining = balance - price
if balance >= price:
    print("Can afford")
else:
    print("Cannot afford")
```
This prints `Can afford`, since `200.75 >= 199.99` is `True`.

**10.** In Python you can only join strings with `+`. Numbers must be converted to strings first with `str()`. Without `str()`, writing `"I am " + 28` raises a `TypeError`, because you cannot add a string and an integer — the `+` operator does not know how to combine those two different types.

On the two casts:
- `int(3.9)` returns `3`. Casting a number to `int` **drops** the decimal part; it does not round, so use `round(3.9)` if you want `4`.
- `int("3.9")` raises a `ValueError`. Casting text is stricter than casting a number, because `"3.9"` is not a whole number. If you need the value anyway, cast twice: `int(float("3.9"))` returns `3`.
