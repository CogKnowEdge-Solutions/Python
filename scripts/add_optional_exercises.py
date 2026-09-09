"""Add optional exercise content to all lab notebooks."""
import json
import os

# Exercise content for each lab, keyed by notebook path
EXERCISES = {
    "Beginner/Lab1/lab-variables-data-types-operators.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Change the notebook so the program **asks the user for the purchase price instead of using a fixed number**. Replace the hardcoded `laptop_cost = 450` line with `laptop_cost = int(input(\"How much does the item cost? \"))`, then re-run all cells from Cell 4 onward. Verify that when you type a price larger than your balance, the line `Can I afford the laptop?` prints `False`. (Remember to re-run Cell 4 too, since the calculation depends on the new cost.)"
            ]
        }
    ],
    "Beginner/Lab2/lab-strings.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Use the **`title()`** method to turn `\"hello, data course\"` into title case (`\"Hello, Data Course\"`), then print it with an f-string. Next, use slicing to remove the first word of `cleaned`: save `cleaned[:cleaned.find(\" \")]` into `first_word`, save `cleaned[cleaned.find(\" \") + 1:]` into `rest_of_message`, and print both. Run the new cell to confirm each line prints as expected."
            ]
        }
    ],
    "Beginner/Lab3/lab-collections.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Add two new students to the `grades` dict — `\"Omar\"` with `73` and `\"Lena\"` with `96` — then re-run the class-average cell and report the new average. Next, collect every grade into a set with `set(grades.values())` and print the number of **distinct** grade values, which will be smaller than the number of students whenever two share a score."
            ]
        }
    ],
    "Beginner/Lab4/lab-control-flow.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Rewrite the **final report cell** to use a `while` loop instead of `for` + `zip`, driving both lists by a `cursor` index variable (starting at `0`). Inside the loop, `continue` past failing students and `break` once you have printed **three** passing students. Confirm the three printed names match the top three of the pass list (`Ana`, `Ben`, `Dina`)."
            ]
        }
    ],
    "Beginner/Lab5/lab-comprehensions.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Build a dict comprehension that maps every student name to the **square** of that student's score — e.g. `{\"Ana\": 92**2, \"Ben\": 67**2, ...}` — using `zip(student_names, scores)`. Then use a set comprehension to collect the **distinct** values from a `final_grades` dict built as `{name: final_grade_result(name) for name in ...}`, writing `{grade for grade in final_grades.values()}` to print the unique letter grades present."
            ]
        }
    ],
    "Beginner/Lab6/lab-student-report-generator.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Add an **honor roll** to the report: after the `Attendance:` line, append the line `Honor Roll` only if the student earned a grade of `A` **and** has attendance of `0.85` or higher. Modify `build_report()` to check `summary[\"grade\"] == \"A\" and info[\"attendance\"] >= 0.85`, conditionally appending `\"Honor Roll\"` to `lines`. Then re-run the generate cell and verify that only `Ana` receives the `Honor Roll` line."
            ]
        }
    ],
    "Intermediate/Lab1/lab-functions-scope.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Add a new parameter `tax_pct: float = 8.0` to `price_order`, applied *after* the discount (so the discount reduces the subtotal first, then tax is added on top of the discounted amount). Re-run Cell 7's three `print_receipt` calls and confirm every total is now slightly higher than before, since 8% tax is added by default."
            ]
        }
    ],
    "Intermediate/Lab2/lab-imports-modules.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Add a new sample list `sample_colors = [\"red\", \"blue\", \"green\", \"yellow\"]` and use `random.choice()` to pick a random color for each name in `sample_names`, printing a line like `\"Ana's color: blue\"` for every name. (Hint: loop over `sample_names` with a `for` loop, calling `random.choice(sample_colors)` once per name.)"
            ]
        }
    ],
    "Intermediate/Lab3/lab-functions-ii.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Add a `min_price: float = 0.0` keyword-only filter to the final pipeline: after filtering for `in_stock`, add a second `filter()` call that keeps only products with `\"price\"` greater than or equal to `10.0`, then re-run the `sorted()` and `map()` steps on the smaller list. Confirm the final printed list only contains `\"Backpack\"` (the only in-stock product at or above $10)."
            ]
        }
    ],
    "Intermediate/Lab8/lab-oop-core-concepts.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Add a fourth subclass, `Clothing(Product)`, with `size` and `material` attributes. Give it:\n",
                "\n",
                "- a `__str__` that extends `super().__str__()` with ` | size {size} ({material})`;\n",
                "- a `shipping_cost()` of `6%` of the price (round to two decimals);\n",
                "- a `category()` that returns `super().category() + \" -> Clothing\"`;\n",
                "- a constructor that calls `super().__init__(name, price, stock)` first, then stores `size` and `material`.\n",
                "\n",
                "Create a clothing item (e.g., `Clothing(\"T-Shirt\", 24.99, 40, \"M\", \"Cotton\")`), append it to the `inventory` list, and re-run the report. Confirm the total shipping now includes the clothing item's 6% charge (it should increase from `$15.25` to `$16.75`)."
            ]
        }
    ],
    "Intermediate/Lab9/lab-oop-advanced-tools.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Add a `remove_item(self, product_name)` method to `Order` that removes the first `LineItem` matching `product_name`. If the product is not found, raise a `ValueError` with the message `\"Product not found in order\"`.\n",
                "\n",
                "Then:\n",
                "\n",
                "1. Create an order with three line items.\n",
                "2. Print the order and confirm `len()` is 3.\n",
                "3. Remove the middle item.\n",
                "4. Print the order again and confirm `len()` is 2 and the total has updated."
            ]
        }
    ],
    "Advanced/Lab1/lab-functional-data-wrangling.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Swap the target currency: instead of euros, price everything in **pounds sterling** (rate `usd_to_gbp = 0.79`). Rename `usd_to_eur` to `usd_to_gbp`, the `price_eur` and `sale_eur` fields to `price_gbp` and `sale_gbp`, and update the table headers and print statements accordingly. Because the same rate multiplies every price, the Part 3 ranking order must stay identical — confirm that by comparing the order of the final table to the one in Section 5."
            ]
        }
    ],
    "Advanced/Lab2/lab-safe-resource-vault.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Rewrite the `DatabaseTransaction` **class** as a `@contextlib.contextmanager` generator function — no class, keeping the exact same behavior. The block should still be able to call `transaction.execute(...)`, and your function must print `BEGIN transaction` on entry, `COMMIT n statement(s)` when the block succeeds, and `ROLLBACK n statement(s)` (clearing the statements) plus re-raise when it fails. Prove the roll-back still happens by wrapping a raising block in `try/except` and confirming the statements list comes out empty. (Hint: a `try/except` with an `else` clause around the `yield` is the generator equivalent of checking `exc_type is None`.)"
            ]
        }
    ],
    "Advanced/Lab3/lab-memory-efficient-data-pipeline.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Rewrite the generator to yield **chunks of lines** instead of single lines:\n",
                "\n",
                "```python\n",
                "def read_log_chunks(path, chunk_size=1000):\n",
                "    with open(path, encoding=\"utf-8\") as f:\n",
                "        while True:\n",
                "            lines = []\n",
                "            for _ in range(chunk_size):\n",
                "                line = f.readline()\n",
                "                if not line:\n",
                "                    break\n",
                "                lines.append(line)\n",
                "            if not lines:\n",
                "                break\n",
                "            yield lines\n",
                "```\n",
                "\n",
                "Loop over `read_log_chunks(\"data/server.log\")`, counting total lines and `500` errors by iterating *inside* each chunk, and confirm the totals still match the answers from Part 1 (140,610 lines, 28,321 errors). Why might chunked reading be preferable to one-line-at-a-time on a slow disk? (Fewer round-trips to the filesystem.)"
            ]
        }
    ],
    "Advanced/Lab4/lab-metaprogramming-toolkit.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Extend `@cache` so keyword arguments are part of the cache key: replace `key = args` with `key = (args, frozenset(kwargs.items()))`. To prove it works, give `expensive` a keyword parameter — `def expensive(n, debug=False):` — then call `expensive(10)` twice, and between them call `expensive(10, debug=True)`. The `debug=True` call must compute again (its key differs), while the repeated `expensive(10)` must hit the cache (no `computing` line). This proves keyword arguments are now part of the cache key."
            ]
        }
    ],
    "Advanced/Lab5/lab-async-api-fetcher.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "**Experiment with Rate Limits.** Try `fetch_in_batches()` with different `batch_size` values and compare timing:\n",
                "\n",
                "- `batch_size=1` → rate limit 1, max 1 concurrent, slowest but safest\n",
                "- `batch_size=5` → rate limit 5, balanced speed and safety\n",
                "- `batch_size=10` → rate limit 10, faster, some throttling risk\n",
                "- `batch_size=30` → rate limit 30, same as unlimited gather, throttled\n",
                "\n",
                "**What to observe:**\n",
                "- How does total time change as batch_size increases?\n",
                "- At what batch_size does throttling start to appear?\n",
                "- What is the \"perfect\" batch_size for this API?\n",
                "\n",
                "Smaller batch_size = safer, slower. Larger batch_size = faster, riskier. The ideal value matches the API's documented concurrency limit."
            ]
        }
    ],
    "Advanced/Lab6/lab-concurrency-models.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "The process pool's startup cost hides inside the timings. Find it.\n",
                "\n",
                "1. Time a bare pool that runs a single trivial task to measure pure startup cost — e.g. `pool.map(abs, [1])`. (Not `lambda`: a lambda cannot be pickled across the process boundary, which is why the real work lives in `workloads.py` in the first place.)\n",
                "2. Subtract that constant from `cpu_proc` and `io_proc_elapsed` and re-read the ledgers.\n",
                "3. Question: with `os.cpu_count()` workers, what speedup does the CPU task approach once startup is removed? (Hint: near the core count, not beyond.)\n",
                "\n",
                "Why does this matter in production? If a call's real work is shorter than the pool's startup cost, multiprocessing is the wrong tool — the overhead can make it *slower* than sequential."
            ]
        }
    ],
    "Advanced/Lab7/lab-ultimate-async-data-stream.ipynb": [
        {
            "cell_type": "markdown",
            "id": "optional-exercise-desc",
            "metadata": {},
            "source": [
                "Make the pipeline resilient, then prove its crash guarantee.\n",
                "\n",
                "1. Swap the source for a flaky twin: redefine `fetch_page` to raise `RuntimeError(\"gateway timed out\")` on `page % 4 == 0`, but only the *first* time that page is requested — track already-failed pages in a set, so the failure is intermittent. (A guaranteed failure is a broken API; retrying it forever is pointless.)\n",
                "2. Make the generator resilient: replace the single `await fetch_page(page)` with a retry loop that tries up to 3 times, sleeping `await asyncio.sleep(0.02)` between attempts, and re-raises only after the budget is spent. (Lab 4's `@retry` idea, inlined because the loop must live inside the generator.)\n",
                "3. Re-run `ingest()`. Pages 4 and 8 must be recovered on the retry, the store must still print `committed 61 rows`, and `events.jsonl` must still hold all 61 lines.\n",
                "4. Prove the crash guarantee: raise a `ValueError` inside an `async with LocalStore(...)` block after writing a few rows, catch it, and confirm the exit message reports the crash and the file is still readable."
            ]
        }
    ],
    # Append-only notebooks (no existing Optional Exercise heading) — add heading + content at end
    "APPEND_Intermediate/Lab4/lab-miscellaneous-topics.ipynb": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Optional Exercise"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "**Extend the lab by adding a discount tier.**\n",
                "\n",
                "Modify the `classify_sale` function (from Step 2) so that it also accepts an optional `discount` parameter (a percentage, e.g. `10` for 10%). If the discount is not `None`, include it in the classification label:\n",
                "\n",
                "```\n",
                "cash with 10% discount -> \"Cash Payment (10% off)\"\n",
                "```\n",
                "\n",
                "Then update the receipt printing to show a \"Discounted\" column when a discount is present. Update the monthly summary to subtract discounts from the total.\n",
                "\n",
                "**Hints:**\n",
                "- Add `discount=None` to the function signature.\n",
                "- Use an `if discount is not None` check inside the `match`/`case` block.\n",
                "- For the receipt, use an f-string with a ternary: `f\"{d}%\" if d else \"-\"`."
            ]
        }
    ],
    "APPEND_Intermediate/Lab5/lab-error-handling.ipynb": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Optional Exercise"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Extend `validate_order` to also validate an optional `\"discount\"` field:\n",
                "\n",
                "- If `\"discount\"` is present, it must be a number between `0` and `50` (inclusive).\n",
                "- If it's missing, default to `0` (no discount).\n",
                "- If it's out of range, add an error to the errors list: `\"Discount must be 0-50, got {value}\"`.\n",
                "\n",
                "Test your updated function by adding a fifth order with `\"discount\": 75` and confirm the error message appears in the output."
            ]
        }
    ],
    "APPEND_Intermediate/Lab6/lab-recursion-algorithms.ipynb": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Optional Exercise"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Implement a **recursive function** called `count_stock(inventory, threshold)` that counts how many products in the inventory have a stock level greater than or equal to `threshold`. Use the same head/tail recursion pattern from Cell 4.\n",
                "\n",
                "Then, use binary search to find the product closest to a target price of `$65.00` in the sorted inventory (the product whose price differs least from the target).\n",
                "\n",
                "Test both with the existing inventory list and print the results."
            ]
        }
    ],
    "APPEND_Intermediate/Lab7/lab-file-handling.ipynb": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Optional Exercise"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Extend the pipeline to add a **fourth order** — a \"Mug\" with qty `4` and price `7.25` — before the export step. Rerun the pipeline and confirm the summary updates: it should report 4 records per format, a total of **10** items sold, and revenue of **$123.47**. Then, in the JSON cell, change the `json.dump` call to use `indent=4` instead of `indent=2` and confirm the file is written with 4-space indentation."
            ]
        }
    ],
    "APPEND_Intermediate/Lab10/lab-school-management-system.ipynb": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Optional Exercise"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Add a **`__add__` operator** to `Person` so that adding two people returns a `sorted` list joining them, and give `School` a `report()` method that prints every member's `role_info()` in every classroom.\n",
                "\n",
                "1. In `Person`, add:\n",
                "\n",
                "```python\n",
                "    def __add__(self, other):\n",
                "        return [str(self), str(other)]\n",
                "```\n",
                "\n",
                "2. In `School`, add a method that prints each person's polymorphic info:\n",
                "\n",
                "```python\n",
                "    def report(self):\n",
                "        for c in self.classrooms:\n",
                "            print(f\"--- {c.subject} ---\")\n",
                "            for p in c.roster:\n",
                "                print(\"  \" + p.role_info())\n",
                "```\n",
                "\n",
                "3. Build a small school, call `report()`, and confirm each line is type-specific (Student vs. Teacher). Then try `ana + mr_bell` and print the resulting two-element list. Verify the output is sensible for both."
            ]
        }
    ],
}


def add_exercise_to_notebook(nb_path, exercise_cells):
    """Add exercise content after the Optional Exercise heading in a notebook."""
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Find the Optional Exercise heading cell
    heading_idx = None
    for i, cell in enumerate(nb["cells"]):
        source = "".join(cell.get("source", []))
        if "Optional Exercise" in source and cell["cell_type"] == "markdown":
            heading_idx = i
            break

    # Idempotency guard: if a cell with our marker id already exists, skip
    if any(cell.get("id", "") == "optional-exercise-desc" for cell in nb["cells"]):
        print(f"  SKIP (already added)")
        return True

    if heading_idx is None:
        # Append at the end for notebooks without an existing heading
        for j, exc_cell in enumerate(exercise_cells):
            nb["cells"].append(exc_cell)
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print(f"  Appended {len(exercise_cells)} cell(s) at end (no heading found)")
        return True

    # Insert exercise cells after the heading
    for j, exc_cell in enumerate(exercise_cells):
        nb["cells"].insert(heading_idx + 1 + j, exc_cell)

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")

    print(f"  Added {len(exercise_cells)} cell(s) after heading at index {heading_idx}")
    return True


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    count = 0
    for rel_path, cells in EXERCISES.items():
        is_append = rel_path.startswith("APPEND_")
        clean_path = rel_path[len("APPEND_"):] if is_append else rel_path
        nb_path = os.path.join(base, clean_path.replace("/", os.sep))
        print(f"Processing {rel_path}...")
        if os.path.exists(nb_path):
            if add_exercise_to_notebook(nb_path, cells):
                count += 1
        else:
            print(f"  FILE NOT FOUND: {nb_path}")
    print(f"\nDone. Updated {count} notebooks.")


if __name__ == "__main__":
    main()
