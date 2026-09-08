"""Tests for Lab 8 — OOP I: Core Concepts.

Covers:
- Product: constructor, public attributes, methods, __str__
- Encapsulation: _price private-by-convention, property validation
- Name mangling: double-underscore attribute renamed by Python
- Inheritance: Book/Electronics inherit parent behavior, super().__init__
- Polymorphism: same method name with different behavior per class
- Inventory report: combined polymorphic pipeline
"""
import pytest


class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self._price = price
        self.stock = stock

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    def category(self):
        return "General merchandise"

    def shipping_cost(self):
        return round(self.price * 0.08, 2)

    def __str__(self):
        return f"{self.name} - ${self.price:.2f} (x{self.stock})"


class Password:
    def __init__(self, value):
        self.__value = value

    def reveal(self):
        return self.__value


class Book(Product):
    def __init__(self, name, price, stock, author, pages):
        super().__init__(name, price, stock)
        self.author = author
        self.pages = pages

    def shipping_cost(self):
        return round(self.price * 0.05, 2)

    def __str__(self):
        return super().__str__() + f" | by {self.author} ({self.pages}p)"

    def category(self):
        return super().category() + " -> Books"


class Electronics(Product):
    def __init__(self, name, price, stock, brand, warranty_months):
        super().__init__(name, price, stock)
        self.brand = brand
        self.warranty_months = warranty_months

    def shipping_cost(self):
        return round(self.price * 0.12, 2)

    def __str__(self):
        return super().__str__() + f" | {self.brand} ({self.warranty_months}mo warranty)"

    def category(self):
        return super().category() + " -> Electronics"


class TestProduct:
    def test_constructor_sets_attributes(self):
        p = Product("Cap", 14.99, 20)
        assert p.name == "Cap"
        assert p.price == 14.99
        assert p.stock == 20

    def test_default_category(self):
        p = Product("Generic", 5.0, 1)
        assert p.category() == "General merchandise"

    def test_default_shipping_cost(self):
        p = Product("Generic", 100.0, 1)
        assert p.shipping_cost() == 8.0

    def test_str_output(self):
        p = Product("Cap", 14.99, 20)
        assert str(p) == "Cap - $14.99 (x20)"


class TestEncapsulation:
    def test_price_getter(self):
        p = Product("Cap", 14.99, 20)
        assert p.price == 14.99

    def test_price_stored_privately_by_convention(self):
        p = Product("Cap", 14.99, 20)
        assert p._price == 14.99

    def test_price_setter(self):
        p = Product("Cap", 14.99, 20)
        p.price = 19.99
        assert p.price == 19.99

    def test_price_cannot_be_negative(self):
        p = Product("Cap", 14.99, 20)
        with pytest.raises(ValueError):
            p.price = -5

    def test_invalid_value_not_stored(self):
        p = Product("Cap", 14.99, 20)
        with pytest.raises(ValueError):
            p.price = -5
        assert p.price == 14.99


class TestNameMangling:
    def test_reveal_works_inside_class(self):
        password = Password("s3cr3t")
        assert password.reveal() == "s3cr3t"

    def test_direct_access_fails(self):
        password = Password("s3cr3t")
        with pytest.raises(AttributeError):
            password.__value

    def test_mangled_name_is_reachable(self):
        password = Password("s3cr3t")
        assert password._Password__value == "s3cr3t"


class TestInheritance:
    def test_book_sets_parent_attributes(self):
        b = Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544)
        assert b.name == "Python Crash Course"
        assert b.price == 44.99
        assert b.stock == 15

    def test_book_specific_attributes(self):
        b = Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544)
        assert b.author == "Eric Matthes"
        assert b.pages == 544

    def test_electronics_specific_attributes(self):
        e = Electronics("Wireless Mouse", 29.99, 30, "LogiTech", 24)
        assert e.brand == "LogiTech"
        assert e.warranty_months == 24

    def test_book_is_instance_of_product(self):
        b = Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544)
        assert isinstance(b, Product) is True

    def test_book_is_instance_of_book(self):
        b = Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544)
        assert isinstance(b, Book) is True

    def test_category_override_extends_super(self):
        b = Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544)
        assert b.category() == "General merchandise -> Books"

    def test_electronics_category_override(self):
        e = Electronics("Wireless Mouse", 29.99, 30, "LogiTech", 24)
        assert e.category() == "General merchandise -> Electronics"


class TestPolymorphism:
    def test_book_shipping_cost_differs_from_parent(self):
        b = Book("Python Crash Course", 100.0, 1, "Eric Matthes", 544)
        assert b.shipping_cost() == 5.0

    def test_electronics_shipping_cost_differs_from_parent(self):
        e = Electronics("Wireless Mouse", 100.0, 1, "LogiTech", 24)
        assert e.shipping_cost() == 12.0

    def test_shared_method_different_results(self):
        b = Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544)
        e = Electronics("Wireless Mouse", 29.99, 30, "LogiTech", 24)
        p = Product("Cap", 14.99, 20)
        assert b.shipping_cost() != e.shipping_cost()
        assert e.shipping_cost() != p.shipping_cost()

    def test_loop_over_mixed_list_calls_right_version(self):
        b = Book("Python Crash Course", 100.0, 1, "Eric Matthes", 544)
        e = Electronics("Wireless Mouse", 100.0, 1, "LogiTech", 24)
        p = Product("Generic", 100.0, 1)
        results = [item.shipping_cost() for item in [b, e, p]]
        assert results == [5.0, 12.0, 8.0]

    def test_str_override_uses_super(self):
        b = Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544)
        assert str(b) == "Python Crash Course - $44.99 (x15) | by Eric Matthes (544p)"


class TestInventoryReport:
    def test_report_builds_inventory(self):
        inventory = [
            Product("Cap", 14.99, 20),
            Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544),
            Electronics("Wireless Mouse", 29.99, 30, "LogiTech", 24),
        ]
        assert len(inventory) == 3

    def test_report_total_shipping(self):
        inventory = [
            Product("Cap", 19.99, 20),
            Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544),
            Electronics("Wireless Mouse", 29.99, 30, "LogiTech", 24),
        ]
        total = sum(item.shipping_cost() for item in inventory)
        expected = round(19.99 * 0.08 + 44.99 * 0.05 + 29.99 * 0.12, 2)
        assert total == expected

    def test_every_item_stringifies(self):
        inventory = [
            Product("Cap", 14.99, 20),
            Book("Python Crash Course", 44.99, 15, "Eric Matthes", 544),
            Electronics("Wireless Mouse", 29.99, 30, "LogiTech", 24),
        ]
        for item in inventory:
            assert str(item) != ""