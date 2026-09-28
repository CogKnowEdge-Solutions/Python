"""Tests for Lab 1 — Variables, Data Types & Operators.

Covers:
- Variable assignment and type inference
- Arithmetic operators
- Comparison operators
- Type conversion
- Type casting between str, int, float and bool
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


class TestTypeCasting:
    """Test casting between the core types (Section 7, "Type Casting")."""

    def test_number_to_text(self):
        result = str(28)
        assert result == "28"
        assert isinstance(result, str)

    def test_text_to_number(self):
        result = int("28")
        assert result == 28
        assert isinstance(result, int)

    def test_text_to_float(self):
        result = float("19.99")
        assert result == 19.99
        assert isinstance(result, float)

    def test_float_to_int_truncates_not_rounds(self):
        # int() drops the decimal part; it does not round to the nearest int.
        assert int(3.9) == 3
        assert int(3.1) == 3
        assert round(3.9) == 4

    def test_int_to_float(self):
        result = float(10)
        assert result == 10.0
        assert isinstance(result, float)

    def test_text_decimal_to_int_raises(self):
        # Casting text is stricter than casting a number: "3.9" is not a whole number.
        with pytest.raises(ValueError):
            int("3.9")

    def test_double_cast_text_decimal_to_int(self):
        assert int(float("3.9")) == 3

    def test_casting_returns_new_value(self):
        age = 28
        age_as_text = str(age)
        assert age == 28
        assert isinstance(age, int)
        assert age_as_text == "28"
        assert isinstance(age_as_text, str)

    def test_casting_does_not_modify_original(self):
        price_text = "450"
        price = int(price_text)
        assert price_text == "450"
        assert price == 450
        assert price_text + price_text == "450450"   # text is still text


    def test_bool_of_empty_and_zero(self):
        assert bool(0) is False
        assert bool(0.0) is False
        assert bool("") is False

    def test_bool_of_non_empty(self):
        assert bool("0") is True   # a non-empty string, even "0", is True
        assert bool("hello") is True
        assert bool([1]) is True

    def test_mixed_addition_raises(self):
        # The reason casting is needed: + refuses to mix str with int.
        with pytest.raises(TypeError):
            "I am " + 28

    def test_casting_fixes_mixed_addition(self):
        assert "I am " + str(28) + " years old" == "I am 28 years old"

    def test_adding_two_texts_joins_them(self):
        assert "2" + "3" == "23"

    def test_adding_two_numbers_adds_them(self):
        assert 2 + 3 == 5

    def test_input_always_returns_text(self):
        # Documented behaviour the optional exercise relies on: input() is a str,
        # so it must be cast before arithmetic.
        typed = "450"   # what input() would return
        assert isinstance(typed, str)
        assert typed + typed == "450450"           # joining, not adding
        assert int(typed) + int(typed) == 900      # cast first, then add


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
