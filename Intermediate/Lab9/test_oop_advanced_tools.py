"""Tests for Lab 9 — OOP II: Advanced Class Tools.

Covers:
- Inner (nested) class: LineItem inside Order
- Static methods: discount calculator
- Class methods: from_dict constructor, get_order_count
- Properties: total_price computed property, customer setter validation
- Dunder methods: __str__, __repr__, __eq__, __len__, __add__
- Combined system: end-to-end ordering demo
"""
import inspect

import pytest


class Order:
    _id_counter = 0

    class LineItem:
        def __init__(self, name, quantity, price):
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            if price <= 0:
                raise ValueError("Price must be positive")
            self.name = name
            self.quantity = quantity
            self.price = price

        @property
        def total_price(self):
            return round(self.quantity * self.price, 2)

        def __str__(self):
            return f"  {self.name} x{self.quantity} @ ${self.price} = ${self.total_price}"

        def __repr__(self):
            return f"LineItem({self.name!r}, {self.quantity!r}, {self.price!r})"

        def __eq__(self, other):
            if not isinstance(other, Order.LineItem):
                return NotImplemented
            return (self.name == other.name
                    and self.quantity == other.quantity
                    and self.price == other.price)

        def __len__(self):
            return self.quantity

    @staticmethod
    def calculate_discount(amount, percent):
        return round(amount * percent / 100, 2)

    def __init__(self, customer):
        Order._id_counter += 1
        self.customer = customer
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    @classmethod
    def from_dict(cls, data):
        order = cls(data["customer"])
        for item in data["items"]:
            order.add_item(cls.LineItem(item["name"], item["quantity"], item["price"]))
        return order

    @classmethod
    def get_order_count(cls):
        return cls._id_counter

    @property
    def total_price(self):
        return round(sum(item.total_price for item in self.items), 2)

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, value):
        if not value or not value.strip():
            raise ValueError("Customer name cannot be empty")
        self._customer = value

    def __str__(self):
        lines = [f"Order for {self.customer}:"]
        for item in self.items:
            lines.append(str(item))
        lines.append(f"  Total: ${self.total_price}")
        return "\n".join(lines)

    def __repr__(self):
        return f"Order(customer={self.customer!r}, items={self.items!r})"

    def __eq__(self, other):
        if not isinstance(other, Order):
            return NotImplemented
        return self.customer == other.customer and self.items == other.items

    def __len__(self):
        return len(self.items)

    def __add__(self, other):
        if not isinstance(other, Order):
            return NotImplemented
        merged = Order(self.customer)
        for item in self.items:
            merged.add_item(Order.LineItem(item.name, item.quantity, item.price))
        for other_item in other.items:
            merged_line = None
            for line in merged.items:
                if line.name == other_item.name:
                    merged_line = line
                    break
            if merged_line is not None:
                merged_line.quantity += other_item.quantity
            else:
                merged.add_item(Order.LineItem(
                    other_item.name, other_item.quantity, other_item.price))
        return merged


class TestInnerClass:
    def test_inner_class_creates_through_outer(self):
        item = Order.LineItem("Coffee", 2, 5.0)
        assert item.name == "Coffee"

    def test_inner_class_has_own_attributes(self):
        item = Order.LineItem("Milk", 1, 8.0)
        assert item.quantity == 1
        assert item.price == 8.0

    def test_inner_class_represents_product_line(self):
        item = Order.LineItem("Bread", 3, 3.0)
        assert item.total_price == 9.0

    def test_inner_class_validates_quantity(self):
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Order.LineItem("X", 0, 5.0)

    def test_inner_class_validates_price(self):
        with pytest.raises(ValueError, match="Price must be positive"):
            Order.LineItem("X", 1, 0)


class TestStaticMethod:
    def test_callable_without_instance(self):
        result = Order.calculate_discount(100, 10)
        assert result == 10.0

    def test_works_on_class_directly(self):
        assert hasattr(Order, "calculate_discount")
        assert Order.calculate_discount(200, 25) == 50.0

    def test_no_self_parameter(self):
        sig = inspect.signature(Order.calculate_discount)
        params = list(sig.parameters.keys())
        assert "self" not in params
        assert "cls" not in params


class TestClassMethod:
    def test_from_dict_creates_order(self):
        order = Order.from_dict({
            "customer": "Carol",
            "items": [{"name": "Laptop", "quantity": 1, "price": 999.99}],
        })
        assert order.customer == "Carol"
        assert len(order.items) == 1

    def test_from_dict_populates_line_items(self):
        order = Order.from_dict({
            "customer": "Dave",
            "items": [
                {"name": "A", "quantity": 2, "price": 10.0},
                {"name": "B", "quantity": 1, "price": 5.0},
            ],
        })
        assert order.items[0].name == "A"
        assert order.items[1].name == "B"

    def test_class_level_state_shared(self):
        count_before = Order.get_order_count()
        Order("Shared1")
        Order("Shared2")
        assert Order.get_order_count() == count_before + 2


class TestProperties:
    def test_total_price_getter(self):
        order = Order("Eve")
        order.add_item(Order.LineItem("Cake", 2, 10.0))
        order.add_item(Order.LineItem("Juice", 3, 5.0))
        assert order.total_price == 35.0

    def test_total_price_read_only(self):
        order = Order("Ed")
        order.add_item(Order.LineItem("Cake", 2, 10.0))
        with pytest.raises(AttributeError):
            order.total_price = 0

    def test_customer_setter_updates(self):
        order = Order("Fay")
        order.customer = "  Fay  "
        assert order.customer == "  Fay  "

    def test_customer_setter_rejects_empty(self):
        order = Order("Grace")
        with pytest.raises(ValueError, match="Customer name cannot be empty"):
            order.customer = ""

    def test_customer_setter_rejects_blank(self):
        order = Order("Hank")
        with pytest.raises(ValueError, match="Customer name cannot be empty"):
            order.customer = "   "


class TestStrRepr:
    def test_str_is_human_readable(self):
        order = Order("Iris")
        order.add_item(Order.LineItem("Tea", 1, 4.0))
        s = str(order)
        assert "Order for Iris" in s
        assert "Tea x1" in s
        assert "Total: $4.0" in s

    def test_repr_shows_class_name_and_fields(self):
        order = Order("Jack")
        order.add_item(Order.LineItem("Pen", 2, 1.5))
        r = repr(order)
        assert "Order(" in r
        assert "customer='Jack'" in r
        assert "LineItem(" in r

    def test_repr_is_unambiguous(self):
        order = Order("Kim")
        order.add_item(Order.LineItem("Book", 1, 12.0))
        r = repr(order)
        assert "items=[" in r
        assert "LineItem('Book', 1, 12.0)" in r

    def test_lineitem_repr(self):
        item = Order.LineItem("Apple", 3, 2.0)
        assert repr(item) == "LineItem('Apple', 3, 2.0)"


class TestEqLen:
    def test_same_fields_equal(self):
        o1 = Order("Leo")
        o1.add_item(Order.LineItem("X", 1, 5.0))
        o2 = Order("Leo")
        o2.add_item(Order.LineItem("X", 1, 5.0))
        assert o1 == o2

    def test_different_quantity_not_equal(self):
        o1 = Order("Mia")
        o1.add_item(Order.LineItem("A", 1, 5.0))
        o2 = Order("Mia")
        o2.add_item(Order.LineItem("A", 2, 5.0))
        assert o1 != o2

    def test_different_items_not_equal(self):
        o1 = Order("Mia")
        o1.add_item(Order.LineItem("A", 1, 5.0))
        o2 = Order("Mia")
        o2.add_item(Order.LineItem("B", 1, 5.0))
        assert o1 != o2

    def test_len_number_of_line_items(self):
        order = Order("Nina")
        order.add_item(Order.LineItem("A", 1, 5.0))
        order.add_item(Order.LineItem("B", 2, 3.0))
        assert len(order) == 2

    def test_len_empty_order(self):
        order = Order("Oscar")
        assert len(order) == 0

    def test_eq_not_implemented_for_non_order(self):
        o = Order("Pat")
        assert o.__eq__("not an order") is NotImplemented


class TestAdd:
    def test_add_returns_combined_order(self):
        o1 = Order("Quinn")
        o1.add_item(Order.LineItem("A", 1, 5.0))
        o2 = Order("Quinn")
        o2.add_item(Order.LineItem("B", 1, 3.0))
        combined = o1 + o2
        assert isinstance(combined, Order)
        assert len(combined) == 2

    def test_add_merges_same_products(self):
        o1 = Order("Rosa")
        o1.add_item(Order.LineItem("Apple", 3, 2.0))
        o2 = Order("Rosa")
        o2.add_item(Order.LineItem("Apple", 1, 2.0))
        combined = o1 + o2
        assert combined.items[0].quantity == 4
        assert combined.items[0].total_price == 8.0

    def test_add_preserves_total(self):
        o1 = Order("Sam")
        o1.add_item(Order.LineItem("X", 2, 5.0))
        o2 = Order("Sam")
        o2.add_item(Order.LineItem("Y", 1, 10.0))
        combined = o1 + o2
        assert combined.total_price == 20.0

    def test_add_raises_type_error_with_non_order(self):
        o = Order("Tina")
        with pytest.raises(TypeError):
            o + "not an order"

    def test_add_does_not_mutate_originals(self):
        o1 = Order("Uma")
        o1.add_item(Order.LineItem("Z", 1, 1.0))
        o2 = Order("Uma")
        o2.add_item(Order.LineItem("Z", 1, 1.0))
        o1 + o2
        assert o1.items[0].quantity == 1
        assert o2.items[0].quantity == 1


class TestCombinedSystem:
    def test_combined_output(self):
        o1 = Order("Vince")
        o1.add_item(Order.LineItem("Coffee", 2, 5.0))
        o1.add_item(Order.LineItem("Milk", 1, 8.0))
        o2 = Order("Wendy")
        o2.add_item(Order.LineItem("Bread", 3, 3.0))
        o2.add_item(Order.LineItem("Tea", 1, 4.0))
        combined = o1 + o2
        assert len(combined) == 4
        assert combined.total_price == 31.0
        assert "Coffee" in repr(combined)
        assert "Bread" in repr(combined)