"""Tests for Lab 2 — Imports & Modules.

Covers:
- math module usage
- datetime module usage
- random module usage (property-based, not exact-value)
- Import style equivalence
"""
import math
import random
from datetime import date, timedelta

import pytest


class TestMathModule:
    """Test math module functions and constants."""

    def test_pi_constant(self):
        assert round(math.pi, 2) == 3.14

    def test_sqrt(self):
        assert math.sqrt(16) == 4.0

    def test_ceil(self):
        assert math.ceil(7.2) == 8

    def test_floor(self):
        assert math.floor(7.8) == 7

    def test_circle_area(self):
        radius = 4
        area = math.pi * radius ** 2
        assert round(area, 2) == 50.27

    def test_pythagorean_hypotenuse(self):
        hypotenuse = math.sqrt(3 ** 2 + 4 ** 2)
        assert hypotenuse == 5.0


class TestDatetimeModule:
    """Test datetime date and timedelta behavior."""

    def test_date_creation(self):
        today = date(2026, 9, 1)
        assert today.year == 2026
        assert today.month == 9
        assert today.day == 1

    def test_timedelta_addition(self):
        today = date(2026, 9, 1)
        due_date = today + timedelta(days=14)
        assert due_date == date(2026, 9, 15)

    def test_date_subtraction_gives_timedelta(self):
        start = date(2026, 9, 1)
        end = date(2026, 9, 15)
        delta = end - start
        assert delta.days == 14

    def test_strftime_weekday(self):
        today = date(2026, 9, 1)
        assert today.strftime("%A") == "Tuesday"

    def test_timedelta_subtraction(self):
        christmas = date(2026, 12, 25)
        ten_days_before = christmas - timedelta(days=10)
        assert ten_days_before == date(2026, 12, 15)


class TestRandomModule:
    """Test random module — property-based since exact values vary."""

    def test_randint_within_range(self):
        for _ in range(50):
            roll = random.randint(1, 6)
            assert 1 <= roll <= 6

    def test_choice_is_from_list(self):
        options = ["Ana", "Ben", "Clara", "Dina", "Eli"]
        for _ in range(50):
            chosen = random.choice(options)
            assert chosen in options

    def test_shuffle_preserves_elements(self):
        original = ["Ana", "Ben", "Clara", "Dina", "Eli"]
        shuffled = original.copy()
        random.shuffle(shuffled)
        assert sorted(shuffled) == sorted(original)
        assert len(shuffled) == len(original)

    def test_shuffle_copy_does_not_mutate_original(self):
        original = ["Ana", "Ben", "Clara", "Dina", "Eli"]
        original_snapshot = original.copy()
        shuffled = original.copy()
        random.shuffle(shuffled)
        assert original == original_snapshot


class TestImportStyleEquivalence:
    """Test that different import styles reach the same underlying code."""

    def test_module_prefix_and_direct_import_agree(self):
        from math import sqrt as direct_sqrt
        assert math.sqrt(16) == direct_sqrt(16)

    def test_aliased_import_agrees_with_direct(self):
        import datetime as dt
        assert dt.date(2027, 1, 1) == date(2027, 1, 1)
