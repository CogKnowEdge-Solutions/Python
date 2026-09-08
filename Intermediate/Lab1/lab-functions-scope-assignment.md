# Lab 1 Assignment: Functions I & Scope

This assignment tests what you learned in **Lab 1: Functions I & Scope**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab1_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-functions-scope.md) and [Section 10 (Step-wise Instructions)](lab-functions-scope.md).

## Concept Questions

**1.** What keyword do you use to define a function, and what keyword do you use to hand a value back to the caller?

**2.** What is a type hint? Does Python enforce it at runtime?

**3.** What is the difference between a default argument and a keyword argument?

**4.** What is the difference between a local variable and a global variable?

## Short Code Tasks

**5.** Write a function `square(number: int) -> int` that returns the square of `number` (using `return`, not `print`). Call it with `square(6)` and print the result.

**6.** Write a function `greet(name: str, greeting: str = "Hello") -> str` that returns `f"{greeting}, {name}!"`. Call it twice: once with only `name`, and once supplying both arguments as keyword arguments in reverse order (`greeting=` before `name=`).

**7.** Without running it, predict what this code prints, then explain why:
```python
counter = 0

def increment():
    counter += 1
    return counter

increment()
```

## Applied Tasks

**8.** Fix the code from Question 7 so it correctly increments the global `counter` and returns the new value. Show the corrected function.

**9.** Write a function `apply_discount(price: float, discount_pct: float = 0.0) -> float` that returns `price` reduced by `discount_pct` percent, rounded to 2 decimal places. Call it once with just `price` and once with both arguments, and print both results.

**10.** Explain, in your own words, why the lab's `price_order` function returns a value instead of printing it directly inside the function. What would be lost if it only printed?

---

## Answer Key

**1.** `def` defines a function; `return` hands a value back to the caller.

**2.** A type hint (e.g., `price: float`) documents what type a parameter or return value is expected to be. Python does **not** enforce it at runtime — it's for readability and tooling, not validation.

**3.** A default argument (`discount_pct: float = 0.0`) is set in the function's *definition* and provides a fallback value when the caller omits that argument. A keyword argument (`price_order(cup_price=4.5)`) is used at the *call site* to name which parameter a value goes to, regardless of order.

**4.** A local variable is created inside a function and only exists while that function is running — it's invisible outside the function. A global variable is created at the top level of the script and is visible everywhere, including inside functions (for reading).

**5.**
```python
def square(number: int) -> int:
    return number * number

print(square(6))
```
This prints `36`.

**6.**
```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

print(greet("Sam"))
print(greet(greeting="Hi", name="Sam"))
```
This prints `Hello, Sam!` then `Hi, Sam!`. The second call works even with parameters supplied in reverse order because keyword arguments are matched by name, not position.

**7.** This raises an `UnboundLocalError`. Because `counter += 1` *assigns* to `counter` inside the function, Python treats `counter` as a local variable for the entire function body — including the read on the right-hand side of `+=`, which happens before any local `counter` has been created. Reading it before assignment fails.

**8.**
```python
counter = 0

def increment():
    global counter
    counter += 1
    return counter

increment()
```
Adding `global counter` tells Python that `counter` inside the function refers to the global variable, so `+= 1` updates the shared value instead of creating a broken local one.

**9.**
```python
def apply_discount(price: float, discount_pct: float = 0.0) -> float:
    return round(price * (1 - discount_pct / 100), 2)

print(apply_discount(50.0))
print(apply_discount(50.0, 25.0))
```
This prints `50.0` (no discount applied) then `37.5` (25% off `50.0`).

**10.** Returning the value lets the caller decide what to do with it — store it in a variable, pass it into another function (like `print_receipt` does by calling `price_order`), or combine it with other values before printing. If `price_order` only printed inside itself, its result couldn't be reused or combined with anything else; the function would only ever be useful for its side effect, not as a building block for other code.
