# Assignment: The Ultimate Async Data Stream (Capstone)

Answer these questions after finishing the lab. Try them **before** reading the
answer key. Suggested time: 20 minutes.

## Questions

**Q1.** A plain generator is lazy; an async generator adds one more capability.
Name that capability, point to the line in `stream_pages()` where it appears,
and say what the event loop does during that line.

**Q2.** The lazy-proof cell prints `consumed 2/10 pages in 0.12s`. Suppose you
replaced the async generator with an eager build:

```python
all_pages = [await fetch_page(p) for p in range(1, TOTAL_PAGES + 1)]
async for page in all_pages: ...
```

How much time would a loop that stops after two pages now have spent before its
first iteration, and why?

**Q3.** The Lab 4 `@timer` calls `func(*args, **kwargs)` and times it. Explain
exactly why that fails to time an `async def ingest()`, and state the two-line
shape of the fix (what changes about the wrapper).

**Q4.** `async with LocalStore("events.jsonl") as db:` guarantees something a
manual `db.file = open(...)` / `db.file.close()` pair cannot. Name the two
protocol methods `async with` calls, and the specific failure mode they cover
that manual close misses.

**Q5 (Code task).** Write a stricter cleaning pipeline `clean_high(events)` that
keeps only events with `amount >= 50` (same `price = amount * 1.08` mapping).
Consume the full stream with `async for`, count the survivors with the `clean`
function swapped for `clean_high`, and print the total. Expected: a single
number between 30 and 36.

**Q6 (Code task).** Write a one-off coroutine `first_purchase()` that consumes
`stream_pages()` and returns the first event whose `kind == "purchase"`, also
printing which page it was found on. The stream must be consumed lazily — no
calling `fetch_page` directly, and you may stop as soon as you find it.

**Q7 (Applied).** The store writes a page and flushes it immediately. Suppose a
page must be *all-or-nothing*: commit all of its events or none. Sketch how
you'd extend `LocalStore` so a page only lands in the file if every event in it
passes a validation, and explain which `__aexit__` behavior makes this safe when
the block raises halfway through a page.

**Q8 (Applied).** `@timer` prints each run's elapsed time. Adapt it so it
*records* every timing into a list `timings` instead of printing. State whether
the async branch changes, and if so, how.

**Q9 (Challenge).** The current stream is strictly sequential: page *N+1*
cannot be fetched until page *N* is consumed. Suppose the API exposed the total
page count up front and every page were independent. Sketch how you would fetch
all pages concurrently using `asyncio.gather` plus an `asyncio.Semaphore`
(see Lab 5), and name the trade-off you accept against the current lazy design.

---

## Answer Key

**Q1.** The extra capability is **non-blocking I/O between yields**: an async
generator can `await` while suspended. The line is `data = await
fetch_page(page)` — during it, the event loop runs other coroutines instead of
blocking on the network. The `yield` on the next line then hands the finished
page to the consumer. (Laziness alone — the ability to stop early — is shared
with plain generators.)

**Q2.** Roughly **0.5 s** (`10 × 50 ms`). The list comprehension eagerly awaits
*all ten* pages before the loop even starts, so the first iteration is delayed
by the full stream latency and all 100 events sit in memory. The generator
version pays only the 2 pages the consumer asked for — that is the whole
argument for keeping the source lazy.

**Q3.** Calling an `async def` function does **not run it** — it returns a
coroutine object. The naive wrapper would time the *creation* of that object
(microseconds) and return it unawaited, so nothing actually runs inside the
timed window. The fix: detect coroutine functions with
`asyncio.iscoroutinefunction(func)` and make the wrapper an `async def` that
`await`s the call — i.e., `async def wrapper(...)` with `result = await
func(*args, **kwargs)` inside the timed span.

**Q4.** `async with` calls **`__aenter__`** on entry and **`__aexit__`** on
exit. The guarantee is that `__aexit__` runs even when the block **raises** — a
crash inside the body cannot leak an open file handle or a half-flushed buffer.
A manual `close()` written after the block is skipped entirely if the block
raises; the context manager's `__aexit__` is invoked by the interpreter
regardless.

**Q5.**

```python
def clean_high(events):
    return list(map(
        lambda ev: {**ev, "price": round(ev["amount"] * 1.08, 2)},
        filter(lambda ev: ev["amount"] >= 50, events)))

stored = 0
async for page in stream_pages():
    stored += len(clean_high(page["events"]))
print(stored)  # 33
```

Amounts are `i * 7 + page`, so `amount >= 50` holds for 33 of the 100 events
(pages 1–7 keep the top 3, pages 8–10 keep the top 4).

**Q6.**

```python
async def first_purchase():
    async for page in stream_pages():
        for ev in page["events"]:
            if ev["kind"] == "purchase":
                print("found on page", page["page"])
                return ev

print(await first_purchase())
# found on page 1
# {'event_id': 0, 'kind': 'purchase', 'amount': 1, ...}
```

The generator is lazy, so returning as soon as the first purchase appears means
only page 1 is fetched. The `async for` still owns the pagination — you never
call `fetch_page` yourself.

**Q7.** Buffer the page's cleaned events and only write them after validation
passes:

```python
def write_checked(self, events):
    if not all(ev["amount"] > 0 for ev in events):  # any validation
        raise ValueError("page failed validation")
    self.write(events)
```

Safety comes from `__aexit__`: if the block raises (here, a failed page), the
interpreter still calls `__aexit__`, which closes the file and reports the
exception — so a partially written page can never leave a dangling open handle.
The rule is "nothing is final until `__aexit__` runs without an exception,"
exactly like Lab 2's commit-on-success / rollback-on-error.

**Q8.** Keep a shared list and append instead of print:

```python
timings = []

def timer(func):
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            timings.append(time.perf_counter() - start)
            return result
        return wrapper
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        timings.append(time.perf_counter() - start)
        return result
    return wrapper
```

Both branches change the same way — only the output step differs. The async
branch still needs to be a coroutine that `await`s the call; recording the time
does not alter that.

**Q9.** Once the page count is known, each page is an independent unit of work,
so you can run them in parallel:

```python
sem = asyncio.Semaphore(5)

async def get_page(p):
    async with sem:
        return await fetch_page(p)

async for page in await asyncio.gather(*[get_page(p) for p in range(1, 11)]):
    ...
```

The trade-off: `gather` collapses the ~0.5 s of sequential latency toward the
cost of one page, at the price of **memory and ordering** — all pages are now
in flight (bounded by the semaphore) instead of one at a time, and the results
arrive in request order, not completion order. The lazy generator is the right
tool for an *unbounded* stream; concurrent prefetch is the right tool when the
page count is known up front and latency is the bottleneck.
