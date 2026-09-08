"""Tests for Lab 5 — Comprehensions.

Covers:
- List comprehensions (with conditions)
- Dict comprehensions (with conditions)
- Set comprehensions
- Nested comprehensions
- Generator expressions
"""
import pytest


class TestListComprehensions:
    """Test list comprehension operations."""

    def test_squares(self):
        result = [x ** 2 for x in range(1, 6)]
        assert result == [1, 4, 9, 16, 25]

    def test_even_numbers(self):
        result = [x for x in range(1, 11) if x % 2 == 0]
        assert result == [2, 4, 6, 8, 10]

    def test_uppercase_words(self):
        words = ["hello", "world", "python"]
        result = [w.upper() for w in words]
        assert result == ["HELLO", "WORLD", "PYTHON"]

    def test_grade_threshold(self):
        scores = [88, 92, 79, 93, 85]
        result = [s for s in scores if s >= 90]
        assert result == [92, 93]

    def test_transform_and_filter(self):
        scores = [88, 92, 79, 93, 85]
        result = [s * 2 for s in scores if s >= 90]
        assert result == [184, 186]

    def test_nested_list_flatten(self):
        matrix = [[1, 2], [3, 4], [5, 6]]
        flat = [val for row in matrix for val in row]
        assert flat == [1, 2, 3, 4, 5, 6]


class TestDictComprehensions:
    """Test dictionary comprehension operations."""

    def test_squares_dict(self):
        result = {x: x**2 for x in range(1, 6)}
        assert result == {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

    def test_names_to_uppercase(self):
        names = ["ana", "ben", "clara"]
        result = {n: n.upper() for n in names}
        assert result == {"ana": "ANA", "ben": "BEN", "clara": "CLARA"}

    def test_filter_dict(self):
        scores = {"Ana": 92, "Ben": 75, "Clara": 88}
        result = {k: v for k, v in scores.items() if v >= 80}
        assert result == {"Ana": 92, "Clara": 88}

    def test_score_to_grade(self):
        students = {"Ana": 92, "Ben": 75, "Clara": 88}
        result = {}
        for name, score in students.items():
            if score >= 90:
                result[name] = "A"
            elif score >= 80:
                result[name] = "B"
            elif score >= 70:
                result[name] = "C"
            else:
                result[name] = "F"
        assert result == {"Ana": "A", "Ben": "C", "Clara": "B"}

    def test_swap_keys_values(self):
        original = {"a": 1, "b": 2, "c": 3}
        swapped = {v: k for k, v in original.items()}
        assert swapped == {1: "a", 2: "b", 3: "c"}


class TestSetComprehensions:
    """Test set comprehension operations."""

    def test_unique_lengths(self):
        words = ["hi", "hello", "hey", "hola"]
        result = {len(w) for w in words}
        assert result == {2, 3, 4, 5}

    def test_distinct_grades(self):
        students = {
            "Ana": "A",
            "Ben": "C",
            "Clara": "B",
            "Dan": "A",
            "Eve": "A"
        }
        result = {v for v in students.values()}
        assert result == {"A", "B", "C"}

    def test_even_squares(self):
        result = {x**2 for x in range(1, 11) if x % 2 == 0}
        assert result == {4, 16, 36, 64, 100}


class TestGenerators:
    """Test generator expressions."""

    def test_sum_generator(self):
        result = sum(x ** 2 for x in range(1, 6))
        assert result == 55

    def test_min_from_generator(self):
        scores = [88, 92, 79, 93, 85]
        result = min(s for s in scores if s >= 85)
        assert result == 85

    def test_any_even(self):
        nums = [1, 3, 5, 7, 8]
        assert any(n % 2 == 0 for n in nums) is True

    def test_all_positive(self):
        nums = [1, 2, 3, 4, 5]
        assert all(n > 0 for n in nums) is True

    def test_all_not_all_positive(self):
        nums = [1, -2, 3, 4, 5]
        assert all(n > 0 for n in nums) is False
