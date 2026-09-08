# Assignment: The Safe Resource Vault — Context Managers

Work through these exercises after finishing the lab to test what you learned. Answer
them in your head first, then check the answer key at the bottom. For the code
exercises, write and run your answers in a scratch file or scratch cell — you do **not**
need to re-run the notebook. Several exercises reuse classes from the lab
(`DatabaseConnection`, `DatabaseTransaction`).

## Questions

**1. Concept — What does `with` guarantee?**
A file opened with `with open(...) as f:` never needs an explicit `f.close()`. Explain
what happens if the code inside the `with` block raises an exception before reaching the
end of the block — does the file still close? Why?

**2. Concept — The `__exit__` signature.**
`__exit__(self, exc_type, exc_value, traceback)` receives three arguments. What is
`exc_type` when the block succeeds, and what is it when the block raises? What does
returning `False` (instead of `True`) from `__exit__` mean for a raised exception?

**3. Concept — The secret inside `@contextlib.contextmanager`.**
In Part 2, the generator wraps its teardown in `try/finally`:

```python
@contextlib.contextmanager
def database_connection(db_name):
    print(f"Opening {db_name} connection...")
    try:
        yield
    finally:
        print(f"Closing {db_name} connection...")
```

Why is the `try/finally` necessary? What would go wrong if the teardown line were
written *without* the `finally`, just as a plain statement after the `yield`?

**4. Code — A class-based lock.**
Write a small class-based context manager `FileLock` that prints `Acquiring lock...` in
`__enter__` (and returns `self`) and prints `Releasing lock...` in `__exit__`. Use it
with a normal `with FileLock("config") as lock:` block, then run a second block that
`raise`s inside it (inside a `try/except`) and confirm both prints appear in both cases.

**5. Code — A timer context manager.**
Write a `@contextlib.contextmanager` generator `timed(name)` that records the wall-clock
time in `__enter__`-style setup (before the `yield`) and, in teardown (after the
`finally`/`yield`), prints `name took X seconds`. Use `time.time()`. Wrap a small
sleeping block (`import time; time.sleep(0.2)`) and check a sensible duration prints.
(Hint: store the start time in a local variable before the `yield`.)

**6. Applied — Roll back, don't hide.**
In Part 3 the transaction prints `ROLLBACK n statement(s)` and calls `self.statements.clear()`.
Why must the class clear the list on rollback — what would a user see if it didn't? And
why does `__exit__` return `False` rather than `True`, given the whole point of a
transaction is to recover from an error?

---

## Answer Key

**1.** The file still closes. `with` guarantees that `__exit__` runs when the block
ends *whether it finished normally or raised*. The file's `__exit__` closes the file
before the exception propagates to whatever is outside the block. (Section 7: "What the
`with` statement guarantees"; Section 10, Steps 2 and 4.)

**2.** On success, `exc_type` is `None` (along with `exc_value` and `traceback`). When
the block raises, `exc_type` is the exception's type (e.g., `ValueError`). Returning
`False` lets a raised exception keep propagating to the caller's `try/except`; returning
`True` would swallow it. Cleanup should not hide errors, so `False` is the right choice.
(Section 7: "The `__enter__` / `__exit__` protocol"; Section 10, Steps 3 and 8.)

**3.** The `finally` guarantees the teardown runs no matter how the block body exits —
success or exception. Without it, a plain statement after the `yield` runs only when
the block finishes *normally*: if the block raises, control jumps past it and the
connection would never be closed. `@contextmanager` is exactly a function that wraps
your teardown in `try/finally` for you — write the `finally` yourself to keep the
guarantee. (Section 7: "The `@contextlib.contextmanager` shortcut"; Section 10, Step 5.)

**4.**
```python
class FileLock:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        print(f"Acquiring lock... {self.path}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Releasing lock... {self.path}")
        return False


with FileLock("config") as lock:
    print("Critical section running.")

try:
    with FileLock("config") as lock:
        raise RuntimeError("crash inside the critical section")
except RuntimeError as error:
    print("Caught outside:", error)
```
Output shows `Acquiring lock...` and `Releasing lock...` in *both* blocks — the release
happens before the error reaches the `try/except`. (Section 10, Step 4 pattern.)

**5.**
```python
import contextlib
import time

@contextlib.contextmanager
def timed(name):
    start = time.time()
    try:
        yield
    finally:
        print(f"{name} took {round(time.time() - start, 3)} seconds")

with timed("sleep"):
    time.sleep(0.2)
```
Prints roughly `sleep took 0.2 seconds`. The start time is captured before the `yield`
(setup), the elapsed time is computed in the `finally` (teardown), so the duration is
measured even if the block raises. (Section 10, Step 5 pattern.)

**6.** If the list weren't cleared, a caller reading `transaction.statements` after a
failed block would still see the doomed statements and might mistakenly "commit" or
report work that was never applied — exactly the half-written transaction state a
rollback exists to prevent. Returning `False` re-raises the original error so the
caller knows the transaction failed and can react (retry, alert, etc.); returning
`True` would hide the failure and make it look like everything succeeded. (Section 10,
Steps 7–8; Section 12.)
