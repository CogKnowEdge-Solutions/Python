# Assignment: The Memory-Efficient Data Pipeline

Answer these questions after finishing the lab. Try them **before** reading the
answer key. Suggested time: 15 minutes.

## Questions

**Q1.** What does `iter([10, 20, 30])` return, and what does calling `next()`
on it repeatedly do when the values run out?

**Q2.** A class-based iterator needs two special methods. Name them and state
the single responsibility of each.

**Q3.** What is the purpose of `raise StopIteration` inside `__next__()`, and
who usually catches it?

**Q4.** What does the `yield` keyword do inside a function, and how is that
different from `return`?

**Q5.** The generator function below is written to read a file line by line.
Explain in one sentence why it never holds the whole file in memory:

```python
def read_log_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line
```

**Q6.** `itertools.groupby` requires the input to be sorted by the grouping
key. Why does that property let the memory-efficient spike detection work
without loading the file?

**Q7.** Explain why the `max()` call below needs a *generator* as its argument
rather than a list, and what happens to the generator after the call.

```python
max(seconds_and_counts(read_log_lines("data/server.log")), key=lambda kv: kv[1])
```

**Q8.** In the lab, `sys.getsizeof(lines_list)` was ~1,140,568 bytes and
`sys.getsizeof(gen)` was 232 bytes. Give one reason this understates the real
memory saving of the generator.

**Q9 (Challenge).** Rewrite `read_log_lines` as `read_log_chunks(path,
chunk_size=1000)` that yields a *list* of up to `chunk_size` lines at a time,
and then count `500`-error lines by looping over the chunks. What is the one
conceptual difference between yielding single lines and yielding chunks?

---

## Answer Key

**A1.** `iter()` returns an *iterator* object for the list. `next()` returns
`10`, `20`, `30` in order; the fourth call raises `StopIteration`, which signals
that the iterator is exhausted.

**A2.** `__iter__` (returns an iterator — usually `self`) and `__next__`
(returns the next value or raises `StopIteration`). `__iter__` sets the stream
up; `__next__` advances it one item.

**A3.** `StopIteration` tells the caller the stream is empty. `for` loops catch
it internally to exit the loop — your code normally never sees it.

**A4.** `yield` hands back a value *and suspends* the function, remembering its
position and local variables; the next `next()` resumes right after the `yield`.
`return` ends the function entirely and hands back a value (or `None`) without
resuming.

**A5.** Because `for line in f` reads the file lazily and `yield` hands each
line out one at a time, so only one line lives in memory at any moment.

**A6.** `groupby` only compares each item against its *neighbor*: it can group
consecutive equal keys while holding just one group at a time. If the keys
weren't sorted, equal keys would be split into multiple groups, so the log's
time-sorted order is what lets one lazy pass produce correct per-second counts.

**A7.** The argument is a generator (lazy, one-pass), so `max` inspects each
`(timestamp, count)` pair as it is produced and keeps only the running maximum —
it never needs the whole list. After the call, the generator is exhausted and
must be re-created to be used again.

**A8.** `sys.getsizeof(list)` counts the array of *pointers* (8 bytes per line),
not the string objects they point to; the list is truly holding far more than
~1.1 MB of data, so the generator's saving is even larger than measured.

**A9.** Example solution:

```python
def read_log_chunks(path, chunk_size=1000):
    with open(path, encoding="utf-8") as f:
        while True:
            lines = []
            for _ in range(chunk_size):
                line = f.readline()
                if not line:
                    break
                lines.append(line)
            if not lines:
                break
            yield lines

total = 0
errors = 0
for chunk in read_log_chunks("data/server.log"):
    total += len(chunk)
    errors += sum(1 for line in chunk if line.split()[-1] == "500")
print(total, errors)  # 140610 28321
```

The difference: yielding a single line streams one item per step (smallest
memory, most round-trips), while yielding a chunk batches filesystem reads
(fewer I/O calls, slightly more memory — `chunk_size` lines at a time). Both
still avoid loading the whole file.
