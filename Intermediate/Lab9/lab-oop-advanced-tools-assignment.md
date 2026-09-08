# Lab 9 — OOP II: Advanced Class Tools: Assignment

---

## Concept Questions

**1.** What is the difference between a static method and a class method?  When
would you use each one, and what arguments do they receive?

**2.** Why does `LineItem.__eq__` return `NotImplemented` when the other object
is not a `LineItem`, instead of raising `TypeError` or returning `False`?

**3.** Explain how an inner class (`LineItem` inside `Order`) differs from a
standalone top-level class.  What does the nesting communicate about the
relationship between the two?

**4.** What is the difference between `__str__` and `__repr__`?  Give an example
of what each should return for the same object, and explain who uses each one.

---

## Code Tasks

**Task 1 — Static discount method.**

Using `Order.calculate_discount(amount, percent)`, compute the discount on a
`$250` purchase at `20%` off.  Print the result.  Then compute the discounted
final price (`amount - discount`) and print that too.

**Task 2 — Class method alternative constructor.**

Create an order using `Order.from_dict` with the following data:

```python
data = {
    "customer": "Diana",
    "items": [
        {"name": "Notebook", "quantity": 3, "price": 4.50},
        {"name": "Pen", "quantity": 10, "price": 1.20},
    ],
}
```

Print the resulting order, then print the return value of
`Order.get_order_count()`.

**Task 3 — Validation.**

Create a `LineItem` with name `"Shirt"`, quantity `2`, and price `15.0` but
place the constructor call inside a `try/except` block, change `quantity` to
`0` and print the error message.  Do the same with `price` set to `-5`.

**Task 4 — `__len__` and `__eq__`.**

Build two orders for the same customer with identical line items.  Print
`order1 == order2`.  Print `len(order1)` and `len(order2)`.  Then build a third
order with a different line item, and confirm it is *not* equal to the first.

**Task 5 — `__add__` with overlapping products.**

Create `order_a` with `LineItem("Apple", 3, 2.0)` and `LineItem("Banana", 2,
1.5)`.  Create `order_b` with `LineItem("Apple", 1, 2.0)` and
`LineItem("Cherry", 4, 0.75)`.  Add the two orders.  Print the combined order.
Verify that the Apple line item has quantity `4` and the total is correct.

**Task 6 — Inner class access pattern.**

Explain in a comment why `Order.LineItem(...)` is used instead of a standalone
`LineItem(...)` at the top level.  What happens if someone tries to create a
`LineItem` outside the `Order` class namespace?  Write a short code snippet
demonstrating this, and explain the result.

---

## Answer Key

### Concept Questions

**1.** A **static method** (`@staticmethod`) receives no implicit first
argument — it is a plain function that lives on the class namespace.  Use it for
utility logic that logically belongs to the class but does not need access to
instance state (`self`) or class state (`cls`).  A **class method**
(`@classmethod`) receives `cls` as its first argument — the class itself.  Use
it for alternative constructors (so `cls(...)` creates the right type even in
subclasses) or to read/modify class-level state shared across instances.

**2.** Returning `NotImplemented` tells Python "I don't know how to compare
these two types" and lets Python fall back to the other object's `__eq__` or the
default identity comparison.  If you raised `TypeError`, Python could never try
the other side.  If you returned `False`, you would mask cases where the other
object *could* provide a meaningful comparison.

**3.** An inner class communicates **ownership** — `LineItem` has no meaning
without its `Order`, so it lives inside the class that owns it.  It is accessed
as `Order.LineItem(...)`, which makes the dependency explicit.  A standalone
top-level class would imply `LineItem` is independent and usable on its own.

**4.** `__str__` produces a **human-readable** string (e.g., `Order for Alice:`),
intended for end users and `print()`.  `__repr__` produces an
**unambiguous, developer-facing** string (e.g.,
`Order(customer='Alice', items=[LineItem('Coffee', 2, 5.0), ...])`), intended
for debugging and the REPL.  `__repr__` should contain enough information to
recreate the object.  When `__str__` is not defined, Python falls back to
`__repr__`.

### Code Tasks

**Task 1**

```python
discount = Order.calculate_discount(250, 20)
print(discount)                # 50.0
final_price = 250 - discount
print(final_price)             # 200.0
```

**Task 2**

```python
data = {
    "customer": "Diana",
    "items": [
        {"name": "Notebook", "quantity": 3, "price": 4.50},
        {"name": "Pen", "quantity": 10, "price": 1.20},
    ],
}
order = Order.from_dict(data)
print(order)
# Order for Diana:
#   Notebook x3 @ $4.5 = $13.5
#   Pen x10 @ $1.2 = $12.0
#   Total: $25.5
print(Order.get_order_count())  # N (includes all orders created so far)
```

`from_dict` uses `cls(data["customer"])` so it creates an `Order` instance.  If
`Order` were subclassed, `cls` would point to the subclass.

**Task 3**

```python
try:
    item = Order.LineItem("Shirt", 0, 15.0)
except ValueError as e:
    print(e)                    # Quantity must be positive
try:
    item = Order.LineItem("Shirt", 2, -5.0)
except ValueError as e:
    print(e)                    # Price must be positive

# A valid item is fine:
item = Order.LineItem("Shirt", 2, 15.0)
print(item.total_price)         # 30.0
```

`LineItem.__init__` validates that quantity and price stay positive, so invalid
items can never exist.

**Task 4**

```python
order1 = Order("Eve")
order1.add_item(Order.LineItem("Cake", 1, 20.0))
order1.add_item(Order.LineItem("Juice", 2, 5.0))

order2 = Order("Eve")
order2.add_item(Order.LineItem("Cake", 1, 20.0))
order2.add_item(Order.LineItem("Juice", 2, 5.0))

print(order1 == order2)  # True  (same customer + same items)
print(len(order1))       # 2
print(len(order2))       # 2

order3 = Order("Eve")
order3.add_item(Order.LineItem("Cake", 1, 20.0))
print(order1 == order3)  # False (different items)
```

`__eq__` compares customer name and all line items.  `__len__` returns the
number of line items in the order.

**Task 5**

```python
order_a = Order("Frank")
order_a.add_item(Order.LineItem("Apple", 3, 2.0))
order_a.add_item(Order.LineItem("Banana", 2, 1.5))

order_b = Order("Frank")
order_b.add_item(Order.LineItem("Apple", 1, 2.0))
order_b.add_item(Order.LineItem("Cherry", 4, 0.75))

combined = order_a + order_b
print(combined)
# Combined Apple: qty 3+1=4, unit price stays 2.0
# Banana: qty 2, Cherry: qty 4
# Total: 4*2.0 + 2*1.5 + 4*0.75 = 8.0 + 3.0 + 3.0 = 14.0
```

Items with the same product name are merged inside `Order.__add__`.
`LineItem` has no `__add__` of its own — the merge logic lives on the outer
order, which loops over the copied lines and sums quantities.

**Task 6**

```python
# LineItem is defined inside Order, so it lives in the Order namespace.
# A standalone reference to LineItem would fail:
try:
    item = LineItem("Test", 1, 5.0)  # NameError — LineItem is not defined here
except NameError as e:
    print(e)  # name 'LineItem' is not defined
```

`Order.LineItem` is the fully qualified name.  The nesting enforces that
`LineItem` is logically owned by `Order` — you must know the parent to access
the child, which keeps the global namespace clean and communicates the
ownership relationship.
