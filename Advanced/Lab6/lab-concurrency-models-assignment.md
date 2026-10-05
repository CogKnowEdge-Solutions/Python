# Assignment: Threading vs Multiprocessing vs asyncio

Answer these questions after finishing the lab. Try them **before** reading the
answer key. Suggested time: 15 minutes.

## Questions

**Q1.** In the CPU ledger, threads take about the same time as the sequential
baseline. The OS can schedule four threads onto four cores at once — so why
doesn't anything actually run in parallel?

**Q2.** asyncio is also "concurrent," yet it shows no CPU speedup either.
What exactly is missing from the CPU coroutine that the I/O coroutine has?

**Q3.** The process speedup (≈3.4x on a 4-core machine) is real but less than
4x. Name two costs that explain the gap.

**Q4.** In the I/O ledger, threads jump from ~1.0x to ~8x. What property does
`time.sleep(0.05)` have that `blur` does not?

**Q5.** Processes finish the 100 fake requests *slower* than threads do. Why
is multiprocessing wasteful for I/O-bound work?

**Q6.** The lab hides the spawn cost inside the timings. If a function's real
work takes 20 ms and the pool startup costs 500 ms, what is the right tool —
and why?

**Q7 (Code task).** Write code that times a `ProcessPoolExecutor` with
`max_workers=os.cpu_count()` running `blur` over `IMAGES` and prints the
speedup versus `cpu_seq`. You may reuse the notebook's variables.

**Q8 (Challenge).** A workload is 50 ms of pure computation followed by 50 ms
of network wait, repeated 200 times. Which single strategy do you expect to
win, and what would a hybrid look like? (Hint: split the work — which part is
CPU-bound and which is I/O-bound?)

**Q9.** In the race demo, four threads ran the same
read-read-modify-write loop with no lock and lost thousands of updates. But a
bare `counter += 1` from several threads usually survives intact on CPython
3.13. Why the difference, and what is the safe rule to take away?

**Q10.** On Windows `mp.get_start_method()` returns `'spawn'`, while Linux
defaults to `'fork'`. Name two practical consequences of the difference for a
production worker pool, and say which one bit you in this lab.

**Q11 (Code task).** Write a `threading.Thread`-based version of the race demo
that is *safe* without using a `Lock` — by giving each thread its own counter —
and print the total. Then explain in two sentences why that design scales
happily to processes but not to threads sharing one object.

---

## Answer Key

**Q1.** The GIL (Global Interpreter Lock). CPython allows at most one thread to
execute Python bytecode at a time per process. The other threads sit at the
lock waiting for their turn, so wall-clock time stays ≈ baseline. The cost is
in the lock, not in the pool.

**Q2.** The missing piece is `await`. `await` is the only place a coroutine
hands control back to the event loop. The CPU coroutine never awaits (blur is
pure computation), so the loop has nothing to switch to — the coroutine runs
start to finish exactly like the sequential loop.

**Q3.** (1) Process startup (spawn) cost — each worker is a fresh Python
interpreter that must be booted. (2) Pickling the images and results across
process boundaries. Both land inside `cpu_proc`. The Optional Exercise
isolates the first one.

**Q4.** `time.sleep` releases the GIL while the thread is parked. The lock is
free during the entire wait, so many threads can sleep simultaneously and wake
up for only the trivial `n * 2` work. `blur` never releases the lock, because
it is always busy computing.

**Q5.** Each worker process costs time to spawn and to shuttle tasks/results
through pickling — overhead that buys nothing for pure waiting. Threads hide
the same waits at a fraction of the cost. Multiprocessing pays a heavy
startup fee for a CPU benefit the I/O task never uses.

**Q6.** Threads, or asyncio. The pool startup (500 ms) dwarfs the 20 ms of
real work, so running it in processes would be *slower* than sequential even
if the parallel part were perfect. Multiprocessing pays off only when the
CPU work is large enough to amortize the startup.

**Q7.**

```python
from concurrent.futures import ProcessPoolExecutor
import os

start = time.perf_counter()
with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
    blurs = list(pool.map(blur, IMAGES))
elapsed = time.perf_counter() - start
print(f"speedup vs sequential: {cpu_seq / elapsed:.2f}x")
```

**Q8.** On average, asyncio should win for the repeated 50 ms waits, since the
compute portion (50 ms) is single-threaded anyway and the waits are asyncio's
strength. A hybrid splits the workload: hand the CPU-heavy chunks to a
`ProcessPoolExecutor` and keep the waiting parts on asyncio — e.g., a worker
process computes the expensive part while coroutines manage all the I/O. That
is exactly what `loop.run_in_executor(pool, ...)` does (Section 7.9).

**Q9.** `counter += 1` is a very short read-modify-write, and on CPython 3.13 it
usually completes inside a single 5 ms switch window, so no other thread ever
gets the GIL in the middle — it *looks* atomic. The lab's loop puts a yield
point (`time.sleep(0)`, i.e. anything at all) between the read and the write, so
the GIL is handed over mid-update and one thread's write is overwritten by
another's stale value. The safe rule: never rely on an operation being atomic "in
practice" — if the value is read, transformed, and written, guard it with a
`Lock` (or make the update a single atomic operation such as
`itertools.count`, a `queue`, or `dict.setdefault` semantics).

**Q10.** `spawn` starts a brand-new interpreter that re-imports the parent's
`__main__` by name; `fork` clones the parent, so memory (and open files,
sockets, locks) is inherited. Consequences: (1) `spawn` is far slower to start
and re-executes module-level code, which is why scripts need an
`if __name__ == "__main__":` guard; (2) with `spawn` only importable,
picklable callables and arguments can cross the boundary, and inherited
descriptors can be a liability with `fork`. The one that bit this lab is the
second: the `lambda` in Section 10, Step 5 could not be pickled, so all the work
had to live at module level in `workloads.py`.

**Q11.** Give each thread its own counter and sum them afterwards:

```python
import threading

def bump_local(steps, results, slot):
    total = 0
    for _ in range(steps):
        total += 1          # local variable - not shared state
    results[slot] = total

results = [0] * 4
threads = [threading.Thread(target=bump_local, args=(2000, results, i)) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(sum(results))        # always 8000, no lock required
```

Two sentences: with one counter *per* worker, nothing is shared, so there is no
interleaving to protect — the same trick works for processes (each already has
its own heap, which is why `COUNTER` stayed at 0 in the lab), but threads
that genuinely need to *share* one object (a cache, a connection pool, a
request counter) cannot opt out of sharing, so they still need a `Lock`.
