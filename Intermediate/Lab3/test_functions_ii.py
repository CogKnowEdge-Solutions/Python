"""Tests for Lab 3 — Functions II.

Covers:
- *args (variable positional arguments)
- **kwargs (variable keyword arguments)
- lambda expressions
- sorted(key=...)
- map() and filter()
"""
import pytest


def total_sales(*amounts: float) -> float:
    return sum(amounts)


def build_product_label(**details: str) -> str:
    parts = [f"{key}: {value}" for key, value in details.items()]
    return ", ".join(parts)


class TestArgs:
    """Test *args behavior."""

    def test_multiple_positional_args(self):
        assert total_sales(25.0, 40.0, 15.5) == 80.5

    def test_five_positional_args(self):
        assert total_sales(10, 20, 30, 40, 50) == 150

    def test_zero_args(self):
        assert total_sales() == 0

    def test_single_arg(self):
        assert total_sales(99.5) == 99.5


class TestKwargs:
    """Test **kwargs behavior."""

    def test_kwargs_collects_dict(self):
        label = build_product_label(name="Mug", color="Blue")
        assert "name: Mug" in label
        assert "color: Blue" in label

    def test_kwargs_different_field_sets(self):
        label_a = build_product_label(name="Mug", color="Blue", price="$8")
        label_b = build_product_label(name="Notebook", pages="200")
        assert "price: $8" in label_a
        assert "pages: 200" in label_b

    def test_kwargs_empty(self):
        assert build_product_label() == ""


class TestLambda:
    """Test lambda expressions."""

    def test_single_arg_lambda(self):
        square = lambda x: x ** 2
        assert square(5) == 25

    def test_multi_arg_lambda(self):
        add = lambda a, b: a + b
        assert add(3, 4) == 7

    def test_lambda_with_negation(self):
        negate = lambda n: -n
        assert negate(7) == -7


class TestSortedKey:
    """Test sorted() with a key= lambda."""

    def test_sort_dicts_by_field(self):
        products = [
            {"name": "Mug", "price": 8.0},
            {"name": "Notebook", "price": 3.5},
            {"name": "Pen", "price": 1.25},
        ]
        sorted_products = sorted(products, key=lambda item: item["price"])
        assert [p["name"] for p in sorted_products] == ["Pen", "Notebook", "Mug"]

    def test_sort_descending_via_negation(self):
        numbers = [4, 1, 7, 3]
        descending = sorted(numbers, key=lambda n: -n)
        assert descending == [7, 4, 3, 1]


class TestMapFilter:
    """Test map() and filter()."""

    def test_map_transforms_every_item(self):
        prices = [8.0, 3.5, 1.25, 12.0]
        discounted = list(map(lambda p: round(p * 0.9, 2), prices))
        assert discounted == [7.2, 3.15, 1.12, 10.8]

    def test_filter_keeps_matching_items(self):
        prices = [8.0, 3.5, 1.25, 12.0]
        affordable = list(filter(lambda p: p < 5.0, prices))
        assert affordable == [3.5, 1.25]

    def test_filter_then_map_chain(self):
        scores = [55, 92, 67, 81, 40]
        passing = list(filter(lambda s: s >= 60, scores))
        assert passing == [92, 67, 81]

    def test_map_and_filter_return_iterators(self):
        result = map(lambda x: x, [1, 2, 3])
        assert not isinstance(result, list)
        assert list(result) == [1, 2, 3]


class TestCombinedArgsKwargs:
    """Test a function combining *args and **kwargs."""

    def test_summarize_order(self):
        def summarize_order(*item_prices: float, **order_info: str) -> str:
            subtotal = sum(item_prices)
            customer = order_info.get("customer", "Guest")
            priority = order_info.get("priority", "standard")
            return f"Order for {customer} ({priority}): {len(item_prices)} item(s), subtotal ${subtotal:.2f}"

        result = summarize_order(8.0, 3.5, 1.25, customer="Ana", priority="rush")
        assert result == "Order for Ana (rush): 3 item(s), subtotal $12.75"

    def test_summarize_order_defaults(self):
        def summarize_order(*item_prices: float, **order_info: str) -> str:
            subtotal = sum(item_prices)
            customer = order_info.get("customer", "Guest")
            priority = order_info.get("priority", "standard")
            return f"Order for {customer} ({priority}): {len(item_prices)} item(s), subtotal ${subtotal:.2f}"

        result = summarize_order(12.0, customer="Ben")
        assert result == "Order for Ben (standard): 1 item(s), subtotal $12.00"
