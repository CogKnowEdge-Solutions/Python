"""Tests for Lab 1 (Intermediate) — Functions I & Scope.

Covers:
- Function definition, parameters, and return values
- Default arguments
- Keyword arguments
- Local vs. global scope
- The global keyword
"""
import pytest


def price_order(cup_price: float, quantity: int, discount_pct: float = 0.0) -> float:
    subtotal = cup_price * quantity
    discounted = subtotal * (1 - discount_pct / 100)
    return round(discounted, 2)


class TestFunctionBasics:
    """Test basic function definition and return values."""

    def test_returns_value_not_none(self):
        result = price_order(4.5, 2)
        assert result is not None

    def test_simple_multiplication(self):
        assert price_order(4.5, 2) == 9.0

    def test_function_is_reusable(self):
        assert price_order(2.0, 5) == 10.0
        assert price_order(3.0, 4) == 12.0

    def test_return_type_is_float(self):
        assert isinstance(price_order(4.5, 2), float)


class TestDefaultArguments:
    """Test default argument behavior."""

    def test_discount_defaults_to_zero(self):
        assert price_order(10.0, 1) == price_order(10.0, 1, 0.0)

    def test_discount_applied_when_given(self):
        assert price_order(10.0, 1, 10.0) == 9.0

    def test_discount_rounds_to_two_places(self):
        result = price_order(4.5, 3, 10.0)
        assert result == 12.15


class TestKeywordArguments:
    """Test keyword argument behavior."""

    def test_keyword_args_match_positional(self):
        by_position = price_order(4.5, 3, 10.0)
        by_keyword = price_order(cup_price=4.5, quantity=3, discount_pct=10.0)
        assert by_position == by_keyword

    def test_keyword_args_out_of_order(self):
        result = price_order(quantity=1, cup_price=5.0, discount_pct=20.0)
        assert result == 4.0

    def test_partial_keyword_args(self):
        result = price_order(4.5, quantity=2)
        assert result == 9.0


class TestLocalScope:
    """Test that local variables don't leak outside their function."""

    def test_local_variable_not_visible_outside(self):
        def compute():
            local_value = 42
            return local_value

        compute()
        assert "local_value" not in dir()

    def test_same_name_different_scopes(self):
        subtotal = "outer value"

        def compute():
            subtotal = "inner value"
            return subtotal

        assert compute() == "inner value"
        assert subtotal == "outer value"


class TestGlobalScope:
    """Test reading and modifying global variables."""

    def test_read_global_without_keyword(self):
        total_orders_today = 5

        def describe():
            return f"Orders: {total_orders_today}"

        assert describe() == "Orders: 5"

    def test_global_keyword_updates_shared_variable(self):
        global _global_counter
        _global_counter = 0

        def log_order():
            global _global_counter
            _global_counter += 1

        log_order()
        log_order()
        log_order()
        assert _global_counter == 3

    def test_assignment_without_global_raises(self):
        counter = 0

        def broken_increment():
            counter += 1
            return counter

        with pytest.raises(UnboundLocalError):
            broken_increment()
