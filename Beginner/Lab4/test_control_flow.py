"""Tests for Lab 4 — Control Flow.

Covers:
- if/elif/else branches (final_grade function)
- for loops (break, continue, enumerate)
- while loops
- Branch coverage: every grade threshold exercised
"""
import pytest


def final_grade(exam_score, assignments_completed):
    """Re-implementation of the Lab 4 final_grade function for testing."""
    if exam_score >= 90 and assignments_completed:
        return "A"
    elif exam_score >= 80 and assignments_completed:
        return "B"
    elif exam_score >= 70 and assignments_completed:
        return "C"
    elif exam_score >= 60 and assignments_completed:
        return "D"
    else:
        return "F"


class TestFinalGradeBranches:
    """Test every branch of final_grade."""

    def test_grade_a_with_assignments(self):
        assert final_grade(95, True) == "A"

    def test_grade_a_boundary(self):
        assert final_grade(90, True) == "A"

    def test_grade_a_without_assignments(self):
        assert final_grade(95, False) == "F"

    def test_grade_b_with_assignments(self):
        assert final_grade(85, True) == "B"

    def test_grade_b_boundary(self):
        assert final_grade(80, True) == "B"

    def test_grade_b_without_assignments(self):
        assert final_grade(85, False) == "F"

    def test_grade_c_with_assignments(self):
        assert final_grade(75, True) == "C"

    def test_grade_c_boundary(self):
        assert final_grade(70, True) == "C"

    def test_grade_c_without_assignments(self):
        assert final_grade(75, False) == "F"

    def test_grade_d_with_assignments(self):
        assert final_grade(65, True) == "D"

    def test_grade_d_boundary(self):
        assert final_grade(60, True) == "D"

    def test_grade_d_without_assignments(self):
        assert final_grade(65, False) == "F"

    def test_grade_f_low_score(self):
        assert final_grade(50, True) == "F"

    def test_grade_f_no_assignments(self):
        assert final_grade(90, False) == "F"

    def test_grade_f_zero_score(self):
        assert final_grade(0, False) == "F"


class TestGradeConsistency:
    """Test that grade logic is deterministic."""

    def test_same_input_same_result(self):
        args = (85, True)
        assert final_grade(*args) == final_grade(*args)

    def test_no_mixup_between_b_and_c(self):
        b_result = final_grade(82, True)
        c_result = final_grade(72, True)
        assert b_result == "B"
        assert c_result == "C"
        assert b_result != c_result


class TestForLoopBehavior:
    """Test loop patterns taught in Lab 4."""

    def test_enumerate(self):
        students = ["Ana", "Ben", "Clara"]
        result = []
        for i, name in enumerate(students):
            result.append(f"{i+1}. {name}")
        assert result == ["1. Ana", "2. Ben", "3. Clara"]

    def test_break_exits_early(self):
        nums = [10, 20, 30, 40, 50]
        total = 0
        for n in nums:
            if n == 30:
                break
            total += n
        assert total == 30

    def test_continue_skips(self):
        nums = [1, 2, 3, 4, 5]
        evens = []
        for n in nums:
            if n % 2 != 0:
                continue
            evens.append(n)
        assert evens == [2, 4]

    def test_range_loop(self):
        result = []
        for i in range(5):
            result.append(i * 2)
        assert result == [0, 2, 4, 6, 8]


class TestWhileLoopBehavior:
    """Test while loop patterns."""

    def test_while_countdown(self):
        count = 5
        result = []
        while count > 0:
            result.append(count)
            count -= 1
        assert result == [5, 4, 3, 2, 1]

    def test_while_search(self):
        data = [1, 3, 5, 7, 9]
        target = 5
        index = 0
        found = False
        while index < len(data):
            if data[index] == target:
                found = True
                break
            index += 1
        assert found is True
        assert index == 2
