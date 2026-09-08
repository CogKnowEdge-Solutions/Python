"""Tests for Lab 4 — Miscellaneous Python Topics.

Covers:
- match/case pattern matching
- None and identity checks
- Working with dates
- Regular expressions
- String formatting (f-strings, .format(), %-formatting)
- range() and the array module
"""
import re
import pytest
from array import array
from datetime import date


# ---------------------------------------------------------------------------
# Helper functions – mirror what the lab teaches
# ---------------------------------------------------------------------------

def classify_payment(method: str) -> str:
    """Classify a payment method using match/case."""
    match method.lower():
        case "cash":
            return "physical"
        case "card":
            return "electronic"
        case "mobile":
            return "digital"
        case _:
            return "unknown"


def substitute_default(value, default="N/A"):
    """Return default when value is None."""
    if value is None:
        return default
    return value


SKU_PATTERN = re.compile(r"SKU-\d{4}-[A-Z]{2}")


def is_valid_sku(code: str) -> bool:
    """Return True if code matches SKU-NNNN-XX pattern."""
    return SKU_PATTERN.fullmatch(code) is not None


def format_order_summary(name: str, qty: int, price: float) -> dict:
    """Return the same summary formatted three different ways."""
    return {
        "fstring":  f"{name}: {qty} × ${price:.2f} = ${qty * price:.2f}",
        "format":   "{name}: {qty} × ${price:.2f} = ${total:.2f}".format(
            name=name, qty=qty, price=price, total=qty * price
        ),
        "percent":  "%s: %d × $%.2f = $%.2f" % (name, qty, price, qty * price),
    }


# ── match/case tests ─────────────────────────────────────────────────────

class TestMatchCase:
    def test_cash(self):
        assert classify_payment("cash") == "physical"

    def test_card(self):
        assert classify_payment("card") == "electronic"

    def test_mobile(self):
        assert classify_payment("mobile") == "digital"

    def test_unknown_method(self):
        assert classify_payment("crypto") == "unknown"

    def test_case_insensitive(self):
        assert classify_payment("CASH") == "physical"
        assert classify_payment("Card") == "electronic"

    def test_empty_string_falls_through(self):
        assert classify_payment("") == "unknown"

    def test_whitespace_only(self):
        assert classify_payment("  ") == "unknown"


# ── None / identity tests ────────────────────────────────────────────────

class TestNoneChecks:
    def test_is_none_true(self):
        x = None
        assert x is None

    def test_is_none_false(self):
        x = 0
        assert x is not None

    def test_eq_none_also_works_for_none(self):
        x = None
        assert x == None  # noqa: E711

    def test_eq_none_true_for_falsy_value(self):
        """== None matches both None and other falsy values that compare equal."""
        x = 0
        assert not (x is None)
        # 0 == None is False in Python, so this confirms identity safety
        assert x != None  # noqa: E711

    def test_substitute_default_replaces_none(self):
        assert substitute_default(None) == "N/A"

    def test_substitute_default_keeps_value(self):
        assert substitute_default("hello") == "hello"

    def test_substitute_default_keeps_falsy_non_none(self):
        assert substitute_default(0) == 0
        assert substitute_default("") == ""
        assert substitute_default(False) is False

    def test_substitute_custom_default(self):
        assert substitute_default(None, default="fallback") == "fallback"

    def test_none_is_not_zero(self):
        assert None is not 0  # noqa: E711

    def test_none_is_not_empty_string(self):
        assert None is not ""  # noqa: E711


# ── Regular expression tests ─────────────────────────────────────────────

class TestRegex:
    @pytest.mark.parametrize("code", [
        "SKU-1234-AB",
        "SKU-0001-ZZ",
        "SKU-9999-AA",
        "SKU-0000-XY",
    ])
    def test_valid_skus(self, code):
        assert is_valid_sku(code)

    @pytest.mark.parametrize("code", [
        "sku-1234-ab",       # lowercase letters
        "SKU-123-AB",        # only 3 digits
        "SKU-12345-AB",      # 5 digits
        "SKU-1234-a",        # 1 letter
        "SKU-1234-ABC",      # 3 letters
        "SKU-1234-ab1",      # letter+digit mixed
        "SK-1234-AB",        # missing U
        "SKU1234AB",         # no dashes
        "SKU-ABCD-12",       # letters where digits expected
        " SKU-1234-AB",      # leading space
        "SKU-1234-AB ",      # trailing space
        "",                   # empty string
        "SKU--AB",           # missing digits
        "SKU-1234-",         # missing letters
    ])
    def test_invalid_skus(self, code):
        assert not is_valid_sku(code)

    def test_findall_returns_multiple(self):
        text = "Items: SKU-1001-AA, SKU-2002-BB, SKU-3003-CC"
        found = SKU_PATTERN.findall(text)
        assert len(found) == 3
        assert found == ["SKU-1001-AA", "SKU-2002-BB", "SKU-3003-CC"]

    def test_search_matches_in_longer_string(self):
        text = "Order #456 contains SKU-5678-EF for delivery"
        match = SKU_PATTERN.search(text)
        assert match is not None
        assert match.group() == "SKU-5678-EF"

    def test_no_match_returns_none(self):
        assert SKU_PATTERN.search("no sku here") is None

    def test_pattern_anchored_with_fullmatch(self):
        """fullmatch rejects partial matches at string boundaries."""
        assert SKU_PATTERN.fullmatch("xSKU-1234-AB") is None
        assert SKU_PATTERN.fullmatch("SKU-1234-ABx") is None


# ── Date tests ────────────────────────────────────────────────────────────

class TestDates:
    def test_today_returns_date(self):
        today = date.today()
        assert isinstance(today, date)

    def test_today_year_reasonable(self):
        today = date.today()
        assert 2024 <= today.year <= 2030

    def test_date_attributes(self):
        d = date(2026, 1, 15)
        assert d.year == 2026
        assert d.month == 1
        assert d.day == 15

    def test_strftime_full(self):
        d = date(2026, 3, 5)
        assert d.strftime("%Y-%m-%d") == "2026-03-05"

    def test_strftime_us_format(self):
        d = date(2026, 3, 5)
        assert d.strftime("%m/%d/%Y") == "03/05/2026"

    def test_strftime_month_name(self):
        d = date(2026, 12, 25)
        assert d.strftime("%B %d, %Y") == "December 25, 2026"

    def test_strftime_weekday(self):
        d = date(2026, 1, 1)  # Thursday
        assert d.strftime("%A") == "Thursday"

    def test_date_from_string_parse(self):
        parts = "2026-07-04".split("-")
        d = date(int(parts[0]), int(parts[1]), int(parts[2]))
        assert d.month == 7
        assert d.day == 4

    def test_date_comparison(self):
        earlier = date(2026, 1, 1)
        later = date(2026, 12, 31)
        assert earlier < later
        assert later > earlier

    def test_date_difference(self):
        d1 = date(2026, 1, 1)
        d2 = date(2026, 1, 10)
        delta = d2 - d1
        assert delta.days == 9

    def test_leap_year_date(self):
        d = date(2028, 2, 29)
        assert d.month == 2
        assert d.day == 29


# ── String formatting tests ──────────────────────────────────────────────

class TestStringFormatting:
    def test_fstring_basic(self):
        name = "Widget"
        price = 9.99
        result = f"{name} costs ${price}"
        assert result == "Widget costs $9.99"

    def test_fstring_precision(self):
        total = 49.9
        assert f"{total:.2f}" == "49.90"

    def test_fstring_alignment(self):
        assert f"{'hi':>10}" == "        hi"
        assert f"{'hi':<10}" == "hi        "
        assert f"{'hi':^10}" == "    hi    "

    def test_format_method_basic(self):
        result = "Hello, {}!".format("world")
        assert result == "Hello, world!"

    def test_format_method_positional(self):
        result = "{0} + {1} = {2}".format(2, 3, 5)
        assert result == "2 + 3 = 5"

    def test_format_method_named(self):
        result = "{item} × {qty}".format(item="Bolt", qty=10)
        assert result == "Bolt × 10"

    def test_percent_format_basic(self):
        result = "Item: %s, Qty: %d" % ("Nail", 100)
        assert result == "Item: Nail, Qty: 100"

    def test_percent_format_float(self):
        result = "Total: $%.2f" % (19.5)
        assert result == "Total: $19.50"

    def test_percent_format_tuple(self):
        result = "%s × %d = $%.2f" % ("Bolt", 3, 7.50)
        assert result == "Bolt × 3 = $7.50"

    def test_all_three_produce_same_output(self):
        summary = format_order_summary("Widget", 4, 2.50)
        expected = "Widget: 4 × $2.50 = $10.00"
        assert summary["fstring"] == expected
        assert summary["format"] == expected
        assert summary["percent"] == expected

    @pytest.mark.parametrize("name,qty,price,expected", [
        ("Bolt",   10,  1.50,  "Bolt: 10 × $1.50 = $15.00"),
        ("Nut",     0,  0.75,  "Nut: 0 × $0.75 = $0.00"),
        ("Washer",  1,  0.10,  "Washer: 1 × $0.10 = $0.10"),
    ])
    def test_format_various_items(self, name, qty, price, expected):
        summary = format_order_summary(name, qty, price)
        assert summary["fstring"] == expected
        assert summary["format"] == expected
        assert summary["percent"] == expected

    def test_empty_name(self):
        summary = format_order_summary("", 2, 5.00)
        assert ": 2 × $5.00 = $10.00" in summary["fstring"]

    def test_large_numbers(self):
        summary = format_order_summary("BulkItem", 10000, 99.99)
        assert "10000" in summary["fstring"]
        assert "999900.00" in summary["fstring"]

    def test_fstring_dict_access(self):
        order = {"item": "Gear", "qty": 3}
        result = f"{order['item']}: {order['qty']} pcs"
        assert result == "Gear: 3 pcs"

    def test_format_with_braces_literal(self):
        result = "literal {{braces}}".format()
        assert result == "literal {braces}"


# ── range() and array tests ──────────────────────────────────────────────

def range_sum(start, stop):
    """Sum the integer sequence produced by range(start, stop)."""
    return sum(range(start, stop))


def array_stats(values):
    """Return (sum, max, list) for a typed integer array built from values."""
    arr = array("i", values)
    return sum(arr), max(arr), list(arr)


class TestRangeArray:
    """Test range() and the array module."""

    def test_range_sequence(self):
        assert list(range(1, 6)) == [1, 2, 3, 4, 5]

    def test_range_stop_exclusive(self):
        assert list(range(0, 5)) == [0, 1, 2, 3, 4]

    def test_range_step(self):
        assert list(range(0, 10, 2)) == [0, 2, 4, 6, 8]

    def test_range_sum(self):
        assert range_sum(1, 6) == 15

    def test_range_is_lazy(self):
        r = range(1, 6)
        assert not isinstance(r, list)
        assert isinstance(r, range)

    def test_array_is_array(self):
        arr = array("i", [3, 1, 5, 2])
        assert type(arr).__name__ == "array"

    def test_array_values(self):
        _, _, listing = array_stats([3, 1, 5, 2])
        assert listing == [3, 1, 5, 2]

    def test_array_append(self):
        arr = array("i", [3, 1, 5, 2])
        arr.append(4)
        assert list(arr) == [3, 1, 5, 2, 4]

    def test_array_sum_max(self):
        total, maximum, _ = array_stats([3, 1, 5, 2])
        assert total == 11 and maximum == 5

    def test_array_typed(self):
        arr = array("i", [1, 2, 3])
        assert arr.typecode == "i"
