# Assignment: The Metaprogramming Toolkit

Answer these questions after finishing the lab. Try them **before** reading the
answer key. Suggested time: 15 minutes.

## Questions

**Q1.** The statement `@timer` above a `def find_primes(limit):` is shorthand for
what assignment statement, and what does that assignment do to the name
`find_primes`?

**Q2.** In the `@timer` demo, `find_primes.__name__` still reports `find_primes`
even though the function that actually runs is the wrapper. What single line
inside the wrapper makes that true, and what would `__name__` be without it?

**Q3.** Explain in one sentence why `wrapper(*args, **kwargs)` — rather than
`wrapper()` or `wrapper(func)` — lets a single decorator wrap *any* function.

**Q4.** `@authenticate(role="admin")` works differently from `@timer`: there is a
function (`authenticate`) returning a function (`decorator`) returning a function
(`wrapper`). What does each of the three levels hold in its closure?

**Q5.** In `@retry`, the `raise RuntimeError(...)` happens *after* the `for` loop,
not inside the `except` block. Why is that the right place?

**Q6.** In `@cache`, `key = args` — a tuple. Why is using a tuple as a dict key
valid, while using a list would fail, and what does `args` actually contain for a
call like `expensive(10)`?

**Q7 (Code task).** Write a `@log` decorator that prints `calling <name>` before
running the function and `finished <name>` after it, preserving the wrapped
function's name with `functools.wraps`. Apply it to a function of your choice.

**Q8 (Challenge).** In `@cache`, `store` is created once, *inside* `cache`, and
shared by every call to the returned wrapper. What would break if two different
functions were decorated with a single shared dict instead of one closure-held
dict each? Hint: think about what happens when both functions receive the same
arguments.

---

## Answer Key

**A1.** `find_primes = timer(find_primes)`, run after the `def`. `timer` is called
with the original function and returns the wrapper, so the name `find_primes` now
points at the *wrapper* — every later call goes through it.

**A2.** `@functools.wraps(func)` (applied to the wrapper) copies the original
function's `__name__` and `__doc__` onto the wrapper. Without it, `__name__`
would be `wrapper` — exactly what the warm-up cell demonstrates.

**A3.** `*args` collects any positional arguments into a tuple and `**kwargs`
collects any keyword arguments into a dict, and `wrapper(*args, **kwargs)`
unpacks them back into the original call — so the wrapper can forward any
signature without ever knowing what arguments the function takes.

**A4.** `authenticate` holds the required `role`; `decorator` holds the wrapped
`func`; `wrapper` holds no persistent state for this lab but is the callable
returned to the caller. (In `@retry` the outermost level holds `max_attempts` and
the wrapper holds the running attempt state.)

**A5.** The loop must be allowed to run all `max_attempts` iterations before we
conclude failure. If the `raise` were inside the `except`, it would fire on the
*first* failure — turning a retry into a single attempt. Raising after the loop
guarantees the budget is fully spent first.

**A6.** `args` is a tuple (e.g. `(10,)`), and tuples are immutable and therefore
hashable, so they are valid dict keys. A list is mutable, so it cannot be hashed
and `store[key]` would raise `TypeError: unhashable type: 'list'`.

**A7.** Example solution:

```python
import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"finished {func.__name__}")
        return result
    return wrapper

@log
def greet(name):
    return f"hello {name}"

print(greet("team"))
```

Output: `calling greet`, `finished greet`, then `hello team`.

**A8.** The cache key is the arguments tuple, not the function. With one shared
dict, calling `expensive(10)` then `cheap(10)` would return `expensive(10)`'s
result for `cheap(10)` — a silently wrong answer. A per-function closure dict
(`store` created inside each `cache(func)` call) keeps each function's results
separate, which is exactly why `store` lives in the closure rather than at module
level.
