"""Tests for Lab 1 — Variables, Data Types & Operators.

Covers:
- Variable assignment and type inference
- Arithmetic operators
- Comparison operators
- Type conversion
- Operator precedence
"""
import pytest


class TestVariableAssignment:
    """Test basic variable assignment."""

    def test_string_assignment(self):
        name = "Ana"
        assert name == "Ana"
        assert isinstance(name, str)

    def test_int_assignment(self):
        age = 22
        assert age == 22
        assert isinstance(age, int)

    def test_float_assignment(self):
        pi = 3.14159
        assert pi == 3.14159
        assert isinstance(pi, float)

    def test_bool_assignment(self):
        is_enrolled = True
        assert is_enrolled is True
        assert isinstance(is_enrolled, bool)

    def test_none_assignment(self):
        address = None
        assert address is None


class TestArithmeticOperators:
    """Test arithmetic operators."""

    def test_addition(self):
        assert 2 + 3 == 5

    def test_subtraction(self):
        assert 10 - 4 == 6

    def test_multiplication(self):
        assert 3 * 4 == 12

    def test_division(self):
        assert 15 / 4 == 3.75

    def test_floor_division(self):
        assert 15 // 4 == 3

    def test_modulo(self):
        assert 17 % 3 == 2

    def test_exponentiation(self):
        assert 2 ** 5 == 32

    def test_combined_expression(self):
        total = 2 * 50 + 100 - 50
        assert total == 150

    def test_celsius_to_fahrenheit(self):
        celsius = 100
        fahrenheit = celsius * 9 / 5 + 32
        assert fahrenheit == 212.0


class TestComparisonOperators:
    """Test comparison operators."""

    def test_equal_to(self):
        assert 5 == 5
        assert 5 == 5.0

    def test_not_equal_to(self):
        assert 5 != 3

    def test_greater_than(self):
        assert 10 > 5

    def test_less_than(self):
        assert 3 < 8

    def test_greater_or_equal(self):
        assert 7 >= 7
        assert 8 >= 7

    def test_less_or_equal(self):
        assert 4 <= 4
        assert 3 <= 4


class TestTypeConversion:
    """Test type conversion operations."""

    def test_int_to_float(self):
        result = float(10)
        assert result == 10.0
        assert isinstance(result, float)

    def test_float_to_int(self):
        result = int(3.9)
        assert result == 3
        assert isinstance(result, int)

    def test_string_to_int(self):
        result = int("15")
        assert result == 15
        assert isinstance(result, int)

    def test_int_to_string(self):
        result = str(42)
        assert result == "42"
        assert isinstance(result, str)

    def test_float_rounding(self):
        assert round(3.14159, 2) == 3.14
        assert round(3.14159, 4) == 3.1416

    def test_boolean_to_int(self):
        assert int(True) == 1
        assert int(False) == 0


class TestVariableUpdates:
    """Test variable reassignment."""

    def test_reassignment(self):
        x = 10
        x = x + 5
        assert x == 15

    def test_counter_pattern(self):
        count = 0
        count += 1
        count += 1
        count += 1
        assert count == 3

    def test_swap_values(self):
        a = 10
        b = 20
        a, b = b, a
        assert a == 20
        assert b == 10


class TestOperatorPrecedence:
    """Test operator precedence rules."""

    def test_multiply_before_add(self):
        assert 2 + 3 * 4 == 14

    def test_parentheses_override(self):
        assert (2 + 3) * 4 == 20

    def test_divide_before_subtract(self):
        assert 20 - 8 / 2 == 16.0

    def test_exponent_before_multiply(self):
        assert 2 * 3 ** 2 == 18
