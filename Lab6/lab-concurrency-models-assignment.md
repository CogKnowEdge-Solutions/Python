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
process computes the expensive part while coroutines manage all the I/O.
