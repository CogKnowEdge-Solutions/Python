# Assignment: Functional Data Wrangling with Lambda Functions

Work through these exercises after finishing the lab to test what you learned.
Answer them in your head first, then check the answer key at the bottom. For the
code exercises, write and run your answers in a scratch file or scratch cell — you
do **not** need to re-run the notebook. Several exercises reuse the `catalog` list
loaded in Section 10, Step 2 of the lab.

## Questions

**1. Concept — Two defensive tricks.**
Part 1's filter lambda uses `.get("stock", product.get("qty", 0))`. Explain what
happens when a product has **no** `stock` or `qty` key at all, and why the final
`... is not None` check on the price matters.

**2. Concept — Why filter before map?**
The lab filters the messy catalog *before* running `map()`. What goes wrong if you
ran Part 2's `map()` lambda on the raw `catalog` first (before filtering)? Name at
least one concrete failure.

**3. Concept — The minus sign in a tuple key.**
`key=lambda p: (p["category"], -p["price_eur"])` sorts category A–Z but price
high-to-low. Why does negating the price work, and what happens to the price column
values themselves when you negate them (do the products' stored prices change)?

**4. Code — Filter with a lambda.**
Write a one-line `filter()` expression that keeps only the products in `catalog`
that are **not discontinued** and have a usable (non-`None`) price under `50.0`,
using `float()` to handle string prices. It must not crash on string prices like
`"34.99"` — and it must skip the products whose price is `null`.

**5. Code — Map with a lambda.**
Write a one-line `map()` expression that turns `priced` (from the lab) into a list of
just the `"name"` strings, in the same order.

**6. Code — Sorted with a key.**
Given `scores = [{"name": "Ana", "points": 84}, {"name": "Bo", "points": 97},
{"name": "Cid", "points": 84}]`, write a `sorted()` call with a lambda key that ranks
them highest points first. For ties (Ana and Cid), break the tie alphabetically by
name.

**7. Applied — Rank by sale price.**
Write a single pipeline (compose `filter`, `map`, and `sorted`) that, from `catalog`,
keeps only in-stock, non-discontinued products with a usable price, produces
`(name, sale_eur)` pairs (using the lab's `usd_to_eur = 0.92` and
`discount_rate = 0.10`), and orders the pairs cheapest first.

**8. Applied — Clean a messy predicate.**
Part 1's predicate is dense. Write a named `def is_active(product)` version, then use
it with `filter()` to reproduce the `active` list exactly (21 products). This is the
"when a lambda is the wrong tool" pattern from Section 10, Step 10.

---

## Answer Key

**1.** `product.get("stock", product.get("qty", 0))` returns the `stock` value if it
exists, otherwise checks `qty`, and only returns `0` when both keys are missing — the
three records with no stock field at all (109, 207, 406) therefore compare `0 > 0`,
fail the predicate, and get dropped without a `KeyError`. The `... is not None` check
matters because a JSON `null` decodes to Python `None`; `float(None)` (or multiplying
it) would crash, so products whose price is `null` (108, 306, 506) must be filtered
out before any arithmetic happens. (Section 7: "Defending against messy data";
Section 10, Step 4.)

**2.** Part 2's `map()` lambda calls `to_usd()`, which reads the price from either
location. On the raw catalog that alone mostly works, but the real failure is that it
would happily process discontinued and out-of-stock products — a Mechanical Keyboard
with `stock: 0`, five discontinued items, and three unpriced records would still get
priced and ranked, which is exactly what the business question forbids. (Deeper: on
the three products whose price is `null`, `to_usd()` would crash with a `KeyError`
reading the missing `pricing` dict.) Filtering first guarantees every product that
reaches `map()` is well-formed. (Section 10, Steps 4–5.)

**3.** `sorted()` compares tuple keys element by element: first `category`, and only
when categories are equal, the second element. Negating the price turns, say, `59.79`
into `-59.79`; Python sorts ascending, so a *more negative* value (larger original
price) comes first — that gives high-to-low. Negating affects only the **key values**
used for comparison; the products' stored `price_eur` values are untouched. (Section 7:
"Multi-key sorting with a tuple key"; Section 10, Step 6.)

**4.**
```python
def price_of(p):
    return p.get("price", p.get("pricing", {}).get("base"))

cheap = list(filter(lambda p: not p["discontinued"]
                             and price_of(p) is not None
                             and float(price_of(p)) < 50.0, catalog))
# -> 19 products
```
`float()` coerces `"34.99"` and `"17.5"` to numbers before the comparison, the
`not p["discontinued"]` guard drops the five discontinued records, and the
`is not None` check skips the three `null`-price records that would crash
`float()`. (Section 10, Step 4 pattern.)

**5.**
```python
names = list(map(lambda p: p["name"], priced))
# -> ['Wireless Mouse', 'USB-C Hub', 'Bluetooth Earbuds', 'Portable SSD 1TB',
#     'Gaming Monitor 27in', ...]  (21 names, same order as `priced`)
```

**6.**
```python
sorted(scores, key=lambda s: (-s["points"], s["name"]))
# -> Bo (97), Ana (84), Cid (84)
```
Negating points makes the sort descending; on ties the tuple's second element sorts
alphabetically, so Ana comes before Cid. (Section 7: "Multi-key sorting with a tuple
key".)

**7.**
```python
cheapest = sorted(
    map(
        lambda p: (p["name"], round(to_usd(p) * usd_to_eur * (1 - discount_rate), 2)),
        filter(
            lambda p: not p["discontinued"]
                      and p.get("stock", p.get("qty", 0)) > 0
                      and p.get("price", p.get("pricing", {}).get("base")) is not None,
            catalog,
        ),
    ),
    key=lambda pair: pair[1],
)
# -> [('Cotton T-Shirt', 8.27), ('Wool Beanie', 10.76), ('Bestselling Novel', 10.76),
#     ..., ('Gaming Monitor 27in', 206.99)]  (21 pairs)
```
Order matters: filter first (including the `None`-price guard so `to_usd()` never sees
an unpriced product), then map, then sort — and the key here is the tuple's second
element (the sale price), not the name. (Section 10, Step 8.)

**8.**
```python
def is_active(product):
    stock = product.get("stock", product.get("qty", 0))
    price = product.get("price", product.get("pricing", {}).get("base"))
    return not product["discontinued"] and stock > 0 and price is not None

active = list(filter(is_active, catalog))   # 21 products
```
The named function makes the three conditions (discontinued flag, missing stock
across two keys, `null` price check) readable at a glance, and it can be reused
without re-typing the lambda. (Section 10, Step 10.)
