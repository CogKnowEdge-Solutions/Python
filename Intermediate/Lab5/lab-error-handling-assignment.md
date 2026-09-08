# Lab 5 — Error Handling: Assignment

---

## Concept Questions

**1.** Why is it better to catch a specific exception like `ValueError` rather
than a bare `except:` or `except Exception:`?

**2.** What does the `finally` block do, and when is it the right choice over
putting cleanup code after the try/except block?

**3.** What are the two arguments to `raise` (when re-raising), and what is
the difference between `raise` and `raise ExceptionType("msg")` inside an
except block?

**4.** Why should a custom exception class inherit from `Exception` (or one of
its subclasses) rather than from `BaseException`?

---

## Code Tasks

**Task 1 — Catch only ValueError.**

The function below catches every exception. Change it so it only catches
`ValueError` (leave other exceptions to propagate):

```python
def to_int(raw):
    try:
        return int(raw)
    except:
        print("Something went wrong")
        return None
```

**Task 2 — Add a finally block.**

Add a `finally` block to the function below that prints `"Cleanup done"` so it
runs whether the try succeeds or fails:

```python
def risky_operation():
    try:
        result = 10 / 0
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero")
```

**Task 3 — Define a custom exception.**

Write a class called `NegativePriceError` that inherits from `Exception`. Its
`__init__` should accept a `price` parameter and store it as `self.price`.
The error message should be: `f"Price cannot be negative, got {price}"`.

**Task 4 — Re-raise with logging.**

Complete the function below so it prints the error message and then re-raises
the original exception:

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        # print the error, then re-raise
        ???
```

**Task 5 — Fix the exception order.**

The code below has the except clauses in the wrong order. Fix the ordering
so the more specific exception is caught first:

```python
def parse_number(raw):
    try:
        value = int(raw)
        result = 100 / value
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero")
    except ValueError:
        print("Not a valid number")
```

**Task 6 — Validate a dictionary.**

Write a function `validate_product(product)` that takes a dictionary and raises
a custom `InvalidProductError` if:
- `"name"` is missing or not a string, OR
- `"price"` is missing or not a positive number.

Test it with these two inputs and print the result for each:

```python
good = {"name": "Mug", "price": 12.50}
bad  = {"name": "", "price": -5}
```

---

## Answer Key

### Concept Questions

**1.** Catching a specific exception like `ValueError` means you only handle
the error you expect. A bare `except:` or `except Exception:` catches
*everything* — including `KeyboardInterrupt`, `SystemExit`, and bugs you
didn't anticipate — silently hiding problems that should crash the program.

**2.** `finally` always runs, whether the `try` block succeeded, raised an
exception that was caught, or raised an exception that was *not* caught.
Putting cleanup code after try/except only runs if the except block didn't
itself raise. `finally` is the correct choice for resource cleanup (closing
files, releasing connections) because it guarantees execution under all
circumstances.

**3.** `raise` with no arguments re-raises the *current* exception with its
original traceback. `raise ExceptionType("msg")` creates a *new* exception
and loses the original traceback. Inside an `except` block, bare `raise` is
almost always what you want for re-raising.

**4.** `BaseException` includes `KeyboardInterrupt`, `SystemExit`, and
`GeneratorExit` — errors that Python itself uses to control the interpreter.
Inheriting from `BaseException` means your custom error could be caught by a
bare `except:` and interfere with interpreter shutdown. Inheriting from
`Exception` keeps your error in the normal exception hierarchy where it
belongs.

### Code Tasks

**Task 1**

```python
def to_int(raw):
    try:
        return int(raw)
    except ValueError:
        print("Not a valid integer")
        return None
```

**Task 2**

```python
def risky_operation():
    try:
        result = 10 / 0
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero")
    finally:
        print("Cleanup done")
```

**Task 3**

```python
class NegativePriceError(Exception):
    def __init__(self, price):
        self.price = price
        super().__init__(f"Price cannot be negative, got {price}")
```

**Task 4**

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        print(f"Logged error: {e}")
        raise
```

**Task 5**

```python
def parse_number(raw):
    try:
        value = int(raw)
        result = 100 / value
        return result
    except ValueError:
        print("Not a valid number")
    except ZeroDivisionError:
        print("Cannot divide by zero")
```

**Task 6**

```python
class InvalidProductError(Exception):
    def __init__(self, message):
        super().__init__(message)

def validate_product(product):
    if not isinstance(product.get("name"), str) or not product["name"].strip():
        raise InvalidProductError("Product name must be a non-empty string")
    price = product.get("price")
    if price is None or not isinstance(price, (int, float)) or price <= 0:
        raise InvalidProductError(f"Product price must be positive, got {price}")

for p in [{"name": "Mug", "price": 12.50}, {"name": "", "price": -5}]:
    try:
        validate_product(p)
        print(f"  {p} -> VALID")
    except InvalidProductError as e:
        print(f"  {p} -> INVALID: {e}")
```

Output:

```
  {'name': 'Mug', 'price': 12.5} -> VALID
  {'name': '', 'price': -5} -> INVALID: Product name must be a non-empty string
```
