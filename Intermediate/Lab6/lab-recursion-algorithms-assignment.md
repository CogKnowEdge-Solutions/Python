# Lab 6 — Recursion & Algorithms: Assignment

---

## Concept Questions

**1.** What are the two essential components of every recursive function? What
happens if you forget the base case?

**2.** Why does the naive recursive Fibonacci function have exponential time
complexity? What technique eliminates the repeated work?

**3.** Explain the difference between linear search and binary search in terms
of time complexity and the data requirements of each.

**4.** In bubble sort, why does the inner loop's range shrink by one after each
pass? What is the time complexity of bubble sort?

---

## Code Tasks

**Task 1 — Recursive power function.**

Write a recursive function `power(base, exp)` that returns `base` raised to the
power `exp`. Do not use `**` or `pow()`. Treat `exp = 0` as the base case
(returning `1`).

Test with `power(2, 5)` — expected output: `32`.

**Task 2 — Find the maximum in a list recursively.**

Write a recursive function `recursive_max(lst)` that returns the largest element
in a list. Use the head/tail pattern: compare `lst[0]` to `recursive_max(lst[1:])`.
Base case: a single-element list returns that element.

Test with `[3, 7, 2, 9, 4]` — expected output: `9`.

**Task 3 — Reverse a string recursively.**

Write a recursive function `reverse_string(s)` that returns the string reversed.
Base case: an empty string returns `""`. Recursive case: last character +
`reverse_string` of the rest.

Test with `"shop"` — expected output: `"pohs"`.

**Task 4 — Improve bubble sort to stop early.**

Modify the `bubble_sort` function from the lab to track whether any swaps
occurred during a pass. If a full pass completes with zero swaps, the list is
already sorted — break out early. Print the number of passes completed.

**Task 5 — Recursive countdown with accumulation.**

Write a function `countdown_with_list(n)` that recursively builds and returns a
list `[n, n-1, n-2, ..., 1]`. Base case: `n == 0` returns `[]`. Print the
list at each recursive call to show the build-up.

Test with `countdown_with_list(5)`.

**Task 6 — Search inventory by price range.**

Write a function `search_by_price(inventory, min_price, max_price)` that uses a
loop to find all products whose price falls within the range (inclusive). Return
a list of matching product names.

Test with the inventory from the lab and the range `$30.00–$80.00`. Expected
output: `['Hoodie', 'Sneakers']`.

---

## Answer Key

### Concept Questions

**1.** Every recursive function needs a **base case** (the simplest input that
can be answered directly, stopping recursion) and a **recursive case** (the
function calls itself with a smaller or simpler argument). Without a base case,
the function calls itself indefinitely until Python's recursion limit is hit,
raising a `RecursionError`.

**2.** The naive Fibonacci function branches into two calls per frame (`fib(n-1)`
and `fib(n-2)`), causing the same subproblem to be solved many times. For
example, `fib(3)` is computed multiple times when calculating `fib(5)`. This
creates an exponential number of calls — O(2^n). **Memoization** (storing
previously computed results in a dictionary or using `functools.lru_cache`)
eliminates the repeated work, reducing time complexity to O(n).

**3.** **Linear search** checks each element one by one — O(n) time — and works
on any unsorted data. **Binary search** halves the search space each step —
O(log n) time — but requires the data to be **sorted** beforehand. For small
datasets the difference is negligible; for large datasets binary search is
dramatically faster.

**4.** After each pass, the largest unsorted element has "bubbled up" to its
correct position at the end. The inner loop shrinks because those final
positions are already sorted and don't need re-checking. Bubble sort has
**O(n^2)** time complexity in the average and worst case, and **O(n)** in the
best case (already sorted data with early-exit optimisation).

### Code Tasks

**Task 1**

```python
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

print(power(2, 5))  # 32
```

**Task 2**

```python
def recursive_max(lst):
    if len(lst) == 1:
        return lst[0]
    rest_max = recursive_max(lst[1:])
    return lst[0] if lst[0] > rest_max else rest_max

print(recursive_max([3, 7, 2, 9, 4]))  # 9
```

**Task 3**

```python
def reverse_string(s):
    if s == "":
        return ""
    return s[-1] + reverse_string(s[:-1])

print(reverse_string("shop"))  # "pohs"
```

**Task 4**

```python
def bubble_sort_optimised(inventory):
    arr = [item["price"] for item in inventory]
    n = len(arr)
    passes = 0
    for pass_num in range(n - 1):
        swapped = False
        for j in range(n - 1 - pass_num):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        passes += 1
        print(f"Pass {pass_num + 1}: {arr} (swaps: {swapped})")
        if not swapped:
            print(f"  Early exit after {passes} passes — already sorted")
            break
    print(f"Total passes: {passes}")
    return arr
```

**Task 5**

```python
def countdown_with_list(n):
    if n == 0:
        print(f"  base case: []")
        return []
    rest = countdown_with_list(n - 1)
    result = [n] + rest
    print(f"  n={n}: {result}")
    return result

print(countdown_with_list(5))
```

**Task 6**

```python
def search_by_price(inventory, min_price, max_price):
    matches = []
    for item in inventory:
        if min_price <= item["price"] <= max_price:
            matches.append(item["name"])
    return matches

inventory = [
    {"name": "T-Shirt",  "price": 29.99, "stock": 12},
    {"name": "Hoodie",   "price": 49.99, "stock": 8},
    {"name": "Jacket",   "price": 99.99, "stock": 3},
    {"name": "Cap",      "price": 14.99, "stock": 20},
    {"name": "Sneakers", "price": 79.99, "stock": 5},
]

result = search_by_price(inventory, 30.00, 80.00)
print(result)  # ['Hoodie', 'Sneakers']
```
