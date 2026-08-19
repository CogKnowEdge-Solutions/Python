# Assignment: The Async API Fetcher

Answer these questions after finishing the lab. Try them **before** reading the
answer key. Suggested time: 15 minutes.

## Questions

**Q1.** The synchronous version (Step 4) takes roughly 15 s for 30 requests even
though each request's *work* is trivial. Where does the time actually go?

**Q2.** In Step 5, one thread runs every coroutine. While one coroutine is
`await`-ing its HTTP response, what is that single thread doing?

**Q3.** What exactly does `asyncio.gather(*coros)` return, and under what
condition does it finish? Why does the total time stay near one round trip
(~0.5 s) instead of 30 round trips?

**Q4.** In Step 6, some results come back with `temp_c: None`. What caused those
failures, and how does this prove that unlimited concurrency is risky?

**Q5.** The `fetch_in_batches` function in Step 7 uses `batch_size=5`. What
happens to the timing if you change it to `batch_size=1`? What about
`batch_size=30`? Explain the trade-off in terms of speed and API safety.

**Q6.** Why does `batch_size` serve as a rate limit? Walk through what happens
inside the `for` loop for the first two batches — how many coroutines are in
flight at the moment the loop transitions from batch 1 to batch 2?

**Q7 (Code task).** Write an async function `fetch_with_retry(cities, max_retries=2)`
that calls `fetch_weather` for every city, catches any result where `temp_c is
None`, and retries those cities up to `max_retries` times. Run it on `CITIES[:10]`
and print how many cities succeeded on the first attempt versus after retries.

**Q8 (Challenge).** In the notebook, each call to `fetch_in_batches` opens a
new `aiohttp.ClientSession()` and closes it when done. What would happen if you
moved the `async with aiohttp.ClientSession()` *inside* the `for` loop —
creating and closing a session per batch instead of per run? Would it still
work? What would be the performance cost?

**Q9 (Challenge).** Batch processing waits for each batch to finish before
starting the next. Propose a sliding-window approach: as soon as one coroutine in
batch N finishes, start the next waiting coroutine from the queue, keeping at
most `batch_size` coroutines in flight at all times. How would the timing compare
to the batch approach for 30 cities with `batch_size=5`?

---

## Answer Key

**A1.** The time is idle time: every `requests.get()` blocks the thread for the
full ~500 ms network latency, so 30 requests serialize their waits to roughly
30 × 500 ms ≈ 15 s. No CPU is busy; the program is stuck waiting on a socket.

**A2.** The thread is *not* idle. The event loop resumes whatever other
coroutine is ready — starting new requests, processing completed ones. The wait
of one coroutine is filled with the work of others; the thread never blocks.

**A3.** `gather` returns a list of results in **argument order**, completing
only when every coroutine has finished. Because the waits overlap, the 30 round
trips share one latency window (~500 ms) instead of stacking 30 × 500 ms.

**A4.** Open-Meteo throttles clients that exceed its concurrency limit (~10–15
simultaneous connections). When all 30 fire at once, the API rejects or drops
some — they return no temperature data (`None`). This proves the API enforces
real limits and that unlimited `gather` is unsafe in production.

**A5.** `batch_size=1` means one request at a time — identical to the
synchronous baseline (~15 s). `batch_size=30` means all 30 at once — identical
to the unlimited gather (~0.5 s, but throttled). The trade-off: smaller batches
are safer (no throttling) but slower; larger batches are faster but risk
throttling. The optimal `batch_size` matches the API's documented concurrency
limit.

**A6.** `batch_size` caps concurrency because the `for` loop only creates
`batch_size` coroutines per iteration and `await`s them all before starting the
next batch. At the moment batch 1 finishes, all 5 coroutines from batch 1 have
completed and 0 from batch 2 have started — there are exactly 0 in flight
during the gap. Max in-flight during any batch = `batch_size`.

**A7.** Example solution:

```python
async def fetch_with_retry(cities, session, max_retries=2):
    results = []
    for city in cities:
        for attempt in range(max_retries + 1):
            result = await fetch_weather(city, session)
            if result["temp_c"] is not None:
                results.append(result)
                if attempt > 0:
                    print(f"  {city['name']}: succeeded on attempt {attempt + 1}")
                break
        else:
            results.append(result)  # still None after all retries
            print(f"  {city['name']}: failed after {max_retries + 1} attempts")
    first_try = sum(1 for r in results if r["temp_c"] is not None)
    print(f"First-attempt successes: {first_try}/{len(cities)}")
    return results
```

Output: varies per run, but most cities succeed on the first attempt; throttled
cities may need 1–2 retries.

**A8.** It would still work, but each batch would pay the TCP + TLS setup cost
again — DNS lookup, connection handshake, and connection pool creation repeated
per batch. With 6 batches of 5 cities, that's 6 connection setups instead of 1.
The session is lightweight to keep open, so creating it once before the loop and
letting it close after the loop finishes is the standard pattern.

**A9.** A sliding window keeps exactly `batch_size` coroutines in flight at all
times by starting a new one as soon as any finishes. For 30 cities with
`batch_size=5`, the window slides continuously instead of pausing between
batches. The total time would be roughly `ceil(30 / 5) × 500 ms ≈ 3 s` — same
wall time as batch processing, but with no idle gap between batches. In practice
the difference is small for 30 cities but becomes significant at larger scales
where the batch-boundary pause adds up.
