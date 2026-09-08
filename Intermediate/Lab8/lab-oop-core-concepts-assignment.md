# Lab 8 — OOP I: Core Concepts: Assignment

---

## Concept Questions

**1.** What is the difference between a class and an object? What does the
`self` parameter represent, and why do you need it in every instance method?

**2.** Explain the difference between `_price` (single underscore) and
`__value` (double underscore) in Python. What is "name mangling" and what
problem does it solve?

**3.** Why is a property (getter + setter) better than letting code read and
write an attribute like `obj.price = ...` directly? Give one example of
validation a setter can perform.

**4.** What does `super()` do? Describe two distinct uses of `super()` shown in
the lab: in `__init__` and in an overridden method like `category()` or
`__str__`.

---

## Code Tasks

**Task 1 — Default shipping behavior.**

Create a `Product` named `"Notebook"` with price `12.50` and stock `50`. Print
its string output and compute its shipping cost using the default rule. What
value does the string show, and how much is the shipping cost?

**Task 2 — Validation via setter.**

Create a `Product` with price `9.99`. Attempt to set its `price` to `-3` inside
a `try/except` block and print the error message. Then print the price again and
confirm it is still `9.99` (the invalid value was never stored).

**Task 3 — Build a Book and an Electronics object.**

Using the classes from the lab, create:
- a `Book("Clean Code", 42.50, 18, "Robert C. Martin", 464)`
- an `Electronics("Keyboard", 59.99, 25, "LogiTech", 36)`

Print both objects, then print the result of `isinstance(book, Product)` and
`isinstance(keyboard, Product)` for each.

**Task 4 — Compute polymorphic shipping.**

Put one `Product`, one `Book`, and one `Electronics` (all with price `100.00`
and stock `1`) into a list. Loop over the list and print each object's shipping
cost. Explain in a comment why the three printed values are different despite
using the same method name.

**Task 5 — Name mangling in action.**

Create a `Password` object holding `"topsecret"`. Inside a `try/except` block,
try to read `password.__value` and print the error. Then read
`password._Password__value` directly and print it. Explain in a comment why the
second line works.

**Task 6 — Extend `__str__` with `super()` in a report.**

Write a `Clothing` subclass of `Product` with `size` and `material` attributes,
a `shipping_cost()` of 6% of price, a `category()` of
`super().category() + " -> Clothing"`, and a `__str__` that extends
`super().__str__()` with ` | size {size} ({material})`. Build a small inventory
with one `Product`, one `Book`, and one `Clothing`, then use a loop to print a
report. Confirm each line shows the shared `name - $price (xstock)` portion plus
the object-specific part.

---

## Answer Key

### Concept Questions

**1.** A **class** is a blueprint (a template describing attributes and methods);
an **object** / instance is a concrete realisation made by calling the class.
`self` refers to the specific object on which a method is being called — it lets
the method access and mutate that object's own attributes, and is why `self`
must be the first parameter of every instance method.

**2.** `_price` is a single underscore — a naming **convention** signalling
"internal, don't touch from outside", but it is still directly accessible.
`__value` (double underscore) triggers **name mangling**: Python internally
renames the attribute to `_ClassName__value` (e.g., `_Password__value`), so a
direct reference like `obj.__value` raises `AttributeError`. Mangling prevents
accidental name collisions in subclasses and discourages direct access, forcing
callers to go through the public interface (here, the `reveal()` method).

**3.** A property centralises read and write logic in one place. The setter can
**validate** input, so an object can never hold invalid data. For example, the
price setter rejects negative values with `raise ValueError("Price cannot be
negative")` — if code assigned `obj.price` directly, nothing could stop a
negative price from being stored.

**4.** `super()` returns the parent class, letting the child call the parent's
version of a method. Two uses in the lab:
   - In `__init__`: `super().__init__(name, price, stock)` runs the parent
     constructor so the child does not re-implement setting shared attributes.
   - In an overridden method: `super().__str__()` / `super().category()` reuse
     the parent's logic and then **extend** it (e.g., appending author/pages or
     a category label), instead of replacing the parent's behaviour entirely.

### Code Tasks

**Task 1**

```python
p = Product("Notebook", 12.50, 50)
print(p)                   # Notebook - $12.50 (x50)
print(p.shipping_cost())   # 1.0  (12.50 * 0.08 = 1.0)
```

`str(p)` shows `Notebook - $12.50 (x50)`, and shipping is `round(12.50 * 0.08,
2) = 1.0`.

**Task 2**

```python
p = Product("Generic", 9.99, 5)
try:
    p.price = -3                     # setter rejects the negative value
except ValueError as e:
    print(e)                         # Price cannot be negative
print(p.price)                       # 9.99 -- still the original value
```

Because assignment goes through the validating setter, the invalid `-3` raised
`ValueError` and was never stored — the object keeps its valid state.

**Task 3**

```python
book = Book("Clean Code", 42.50, 18, "Robert C. Martin", 464)
keyboard = Electronics("Keyboard", 59.99, 25, "LogiTech", 36)
print(book)        # Clean Code - $42.50 (x18) | by Robert C. Martin (464p)
print(keyboard)    # Keyboard - $59.99 (x25) | LogiTech (36mo warranty)
print(isinstance(book, Product))      # True
print(isinstance(keyboard, Product))  # True
```

`super().__init__` sets `name`, `price`, and `stock` for both, so both are
recognised as `Product` instances.

**Task 4**

```python
items = [
    Product("Generic", 100, 1),
    Book("Book", 100, 1, "Author", 100),
    Electronics("Gadget", 100, 1, "Brand", 12),
]
for item in items:
    print(item.shipping_cost())   # 8.0, 5.0, 12.0
# The three values differ because each class overrides shipping_cost()
# with a different rate (8%, 5%, 12%) while keeping the same method name —
# that is polymorphism.
```

**Task 5**

```python
password = Password("topsecret")
try:
    print(password.__value)            # AttributeError
except AttributeError as e:
    print(e)                           # 'Password' object has no attribute '__value'
print(password._Password__value)       # topsecret -- the mangled name still works
```

`__value` was renamed to `_Password__value` by name mangling, so the plain name
fails but the mangled name is reachable from outside.

**Task 6**

```python
class Clothing(Product):
    def __init__(self, name, price, stock, size, material):
        super().__init__(name, price, stock)
        self.size = size
        self.material = material

    def shipping_cost(self):
        return round(self.price * 0.06, 2)

    def category(self):
        return super().category() + " -> Clothing"

    def __str__(self):
        return super().__str__() + f" | size {self.size} ({self.material})"

inventory = [
    Product("Cap", 14.99, 20),
    Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544),
    Clothing("T-Shirt", 24.99, 40, "M", "Cotton"),
]
for item in inventory:
    print(item)
```

Each line includes the shared `name - $price (xstock)` prefix (from the parent's
`__str__` via `super()`) plus the child-specific suffix (author/pages or
size/material).