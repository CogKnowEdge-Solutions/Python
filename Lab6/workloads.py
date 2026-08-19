"""Pure-Python workloads for the lab.

Both functions live in their own module so `ProcessPoolExecutor` workers
(separate processes, started via "spawn" on Windows/macOS) can import them by
name. A function defined only in a notebook cell cannot be shipped to another
process - importing a module is the reliable way.
"""

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


# 100 small images, fixed count and order so every strategy does identical work.
IMAGES = [make_image(100) for _ in range(100)]
