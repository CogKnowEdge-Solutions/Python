"""Pure-Python workloads for the lab.

Every callable used by a pool lives in this module so `ProcessPoolExecutor`
workers (separate processes, started via "spawn" on Windows/macOS) can import
them by name. A function defined only in a notebook cell cannot be shipped to
another process - importing a module is the reliable way. The module-level
`COUNTER` also demonstrates the memory model: threads share the one object,
processes each get a private copy when they start.
"""

import os
import threading
import time


def make_image(size):
    """Create a fake 2D image: a size x size grid of pixel brightness values (0-255).

    The pattern is deterministic (row + column) so every strategy
    processes identical data and results are comparable.
    """
    return [[(r + c) % 256 for c in range(size)] for r in range(size)]


def blur(image):
    """A pure-Python box blur: every pixel becomes the average of its 3x3 neighbourhood.

    100% CPU-bound: no I/O, no C helper, so the GIL is never released
    while it runs. This is the workload that tests CPU parallelism.
    """
    size = len(image)
    out = [[0] * size for _ in range(size)]
    for r in range(size):
        for c in range(size):
            total = 0
            # Average the 3x3 neighbourhood around pixel (r, c)
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < size and 0 <= cc < size:
                        total += image[rr][cc]
            out[r][c] = total // 9
    return out


def fetch(n):
    """A fake network round trip: sleep 50 ms, then return n * 2.

    100% I/O-bound: the CPU is idle the whole time, and the GIL is released
    while the thread waits. This is the workload that tests I/O concurrency.
    """
    time.sleep(0.05)
    return n * 2


def probe_worker(label=""):
    """Pause 50 ms, then report who is executing. Returns a dict.

    Sent to raw threads, a thread pool and a process pool. In every thread
    case "pid" is the *same* (one interpreter, one GIL) and only "thread_id"
    changes; in the process-pool case each worker reports a *different* pid,
    because each is a separate interpreter with its own GIL.

    A dict rather than a tuple, so the notebook can ask for the field it wants
    by name (`row["pid"]`) instead of counting commas in `for pid, tid, name`.

    The pause is deliberate: under "spawn" a worker process needs a few hundred
    ms to boot, so instant tasks would all be handled by whichever worker
    finished booting first, and the pid count would lie.
    """
    time.sleep(0.05)
    return {
        "label": label,
        "pid": os.getpid(),
        "thread_id": threading.get_ident(),
        "thread_name": threading.current_thread().name,
    }


# One counter for the whole module. It is a dict holding a single number
# because that is what lets several threads reach the *same* mutable object
# without copying it. Under "spawn" a worker process imports this module fresh
# and gets its own COUNTER, which is exactly what the third measurement shows.
COUNTER = {"count": 0}
COUNTER_LOCK = threading.Lock()


def counter_total():
    """Read the counter from wherever you are: notebook, thread or process."""
    return COUNTER["count"]


def reset_counter():
    """Start again from zero, so one measurement cannot leak into the next."""
    COUNTER["count"] = 0


def bump_unlocked(steps):
    """Add `steps` to the counter with no lock. Returns this worker's total.

    Read the counter, hand the GIL over with `time.sleep(0)`, then write back
    the value we read. If another thread wrote in between, our stale value
    overwrites its update and that increment is lost.

    Real code opens the same window by doing *anything* between the read and
    the write: I/O, a C extension that releases the GIL, or simply enough
    bytecodes for the 5 ms switch timer to fire.
    """
    for _ in range(steps):
        mine = COUNTER["count"]
        time.sleep(0)  # the race window: another thread can take the GIL here
        COUNTER["count"] = mine + 1
    return counter_total()


def bump_locked(steps):
    """The same loop, but every read-modify-write happens under COUNTER_LOCK.

    Under a process pool no lock is even needed, because there is nothing left
    to share: each worker counts into its own copy and returns its own total.
    """
    for _ in range(steps):
        with COUNTER_LOCK:
            mine = COUNTER["count"]
            time.sleep(0)
            COUNTER["count"] = mine + 1
    return counter_total()


# 100 small images, fixed count and order so every strategy does identical work.
IMAGES = [make_image(100) for _ in range(100)]
