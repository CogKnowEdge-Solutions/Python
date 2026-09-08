"""Tests for Lab 5 — Error Handling.

Covers:
- try/except basic pattern
- Multiple specific exceptions
- try/finally cleanup
- Custom exceptions (InvalidOrderError)
- Re-raising errors
- Robust order validation
"""
import pytest
import io


class InvalidOrderError(Exception):
    """Custom exception from the lab."""
    def __init__(self, field, value, message):
        super().__init__(message)
        self.field = field
        self.value = value


def parse_price(price_str):
    """Convert a price string to float. Returns None on failure."""
    try:
        return float(price_str)
    except (ValueError, TypeError):
        return None


def process_quantity(value):
    """Validate and return an integer quantity.

    Returns the integer if valid, None if zero, raises TypeError otherwise.
    """
    try:
        qty = int(value)
    except (ValueError, TypeError):
        raise TypeError(f"Cannot convert {value!r} to an integer quantity")
    if qty == 0:
        return None
    return qty


def validate_order(product_name, quantity, price):
    """Validate an order and raise InvalidOrderError on the first problem found.

    Returns a dict of the validated order if everything is fine.
    """
    errors = []

    if not isinstance(product_name, str) or not product_name.strip():
        errors.append(("product_name", product_name, "Product name must be a non-empty string"))

    if not isinstance(quantity, (int, float)):
        errors.append(("quantity", quantity, "Quantity must be a number"))
    elif quantity < 1:
        errors.append(("quantity", quantity, "Quantity must be at least 1"))

    if isinstance(price, str):
        price = parse_price(price)
        if price is None:
            errors.append(("price", price, "Price must be a valid number"))

    if isinstance(price, (int, float)) and price < 0:
        errors.append(("price", price, "Price cannot be negative"))

    if errors:
        raise InvalidOrderError(*errors[0])

    return {"product": product_name, "quantity": int(quantity), "price": float(price)}


def validate_order_collect(product_name, quantity, price):
    """Validate an order collecting ALL errors, raise InvalidOrderError with first.

    Demonstrates the multi-error collection pattern from the lab.
    """
    errors = []

    if not isinstance(product_name, str) or not product_name.strip():
        errors.append(("product_name", product_name, "Product name must be a non-empty string"))

    if not isinstance(quantity, (int, float)):
        errors.append(("quantity", quantity, "Quantity must be a number"))
    elif quantity < 1:
        errors.append(("quantity", quantity, "Quantity must be at least 1"))

    if isinstance(price, str):
        price = parse_price(price)
        if price is None:
            errors.append(("price", price, "Price must be a valid number"))

    if isinstance(price, (int, float)) and price < 0:
        errors.append(("price", price, "Price cannot be negative"))

    if errors:
        first = errors[0]
        err = InvalidOrderError(*first)
        err.all_errors = errors
        raise err

    return {"product": product_name, "quantity": int(quantity), "price": float(price)}


def read_with_cleanup(filepath):
    """Read a file using try/finally to guarantee cleanup.

    Returns the content string if the file could be read, raises FileNotFoundError otherwise.
    """
    handle = io.StringIO()
    try:
        handle.write("resource opened\n")
        content = None
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filepath} not found")
        handle.write("resource read\n")
        return content
    finally:
        handle.write("resource closed\n")
        handle.close()


# ---------------------------------------------------------------------------
# Test Classes
# ---------------------------------------------------------------------------

class TestBasicTryExcept:
    """Tests for parse_price — basic try/except pattern."""

    def test_valid_price_string(self):
        assert parse_price("19.99") == 19.99

    def test_valid_integer_string(self):
        assert parse_price("25") == 25.0

    def test_invalid_string_returns_none(self):
        assert parse_price("not-a-number") is None

    def test_empty_string_returns_none(self):
        assert parse_price("") is None

    def test_none_input_returns_none(self):
        assert parse_price(None) is None

    def test_list_input_returns_none(self):
        assert parse_price([1, 2, 3]) is None


class TestMultipleExceptions:
    """Tests for process_quantity — handling multiple exception types."""

    def test_valid_int_string(self):
        assert process_quantity("5") == 5

    def test_float_string_raises_type_error(self):
        with pytest.raises(TypeError, match="Cannot convert"):
            process_quantity("3.7")

    def test_valid_int(self):
        assert process_quantity(10) == 10

    def test_zero_returns_none(self):
        assert process_quantity(0) is None

    def test_non_numeric_string_raises_type_error(self):
        with pytest.raises(TypeError, match="Cannot convert"):
            process_quantity("abc")

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError, match="Cannot convert"):
            process_quantity(None)

    def test_list_raises_type_error(self):
        with pytest.raises(TypeError):
            process_quantity([1, 2])


class TestFinally:
    """Tests for try/finally — cleanup pattern."""

    def test_finally_runs_even_after_exception(self):
        handle = io.StringIO()
        try:
            handle.write("before error\n")
            raise ValueError("boom")
        except ValueError:
            handle.write("caught error\n")
        finally:
            handle.write("finally block ran\n")

        output = handle.getvalue()
        assert "before error" in output
        assert "caught error" in output
        assert "finally block ran" in output

    def test_finally_runs_when_no_exception(self):
        handle = io.StringIO()
        try:
            handle.write("no error\n")
        finally:
            handle.write("finally block ran\n")

        output = handle.getvalue()
        assert "no error" in output
        assert "finally block ran" in output

    def test_cleanup_pattern_with_stringio(self, tmp_path):
        missing = tmp_path / "missing.txt"
        with pytest.raises(FileNotFoundError):
            read_with_cleanup(str(missing))

    def test_cleanup_reads_existing_file(self, tmp_path):
        good = tmp_path / "order.txt"
        good.write_text("Widget, 2, 9.99")
        assert "Widget, 2, 9.99" in read_with_cleanup(str(good))


class TestCustomException:
    """Tests for InvalidOrderError."""

    def test_inherits_from_exception(self):
        assert issubclass(InvalidOrderError, Exception)

    def test_carries_field_value_message(self):
        err = InvalidOrderError("price", -5, "Price cannot be negative")
        assert err.field == "price"
        assert err.value == -5
        assert str(err) == "Price cannot be negative"

    def test_can_be_raised_and_caught(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            raise InvalidOrderError("quantity", "abc", "Quantity must be numeric")
        assert exc_info.value.field == "quantity"
        assert exc_info.value.value == "abc"

    def test_exception_message_accessible(self):
        err = InvalidOrderError("product", "", "Name required")
        assert "Name required" in str(err)


class TestReRaise:
    """Tests for re-raising errors while preserving type."""

    def test_reraise_preserves_exception_type(self):
        with pytest.raises(ValueError):
            try:
                raise ValueError("original")
            except ValueError:
                raise

    def test_logging_pattern_with_reraise(self):
        log = []
        with pytest.raises(TypeError):
            try:
                raise TypeError("bad type")
            except TypeError as e:
                log.append(f"Logged: {e}")
                raise

        assert "Logged: bad type" in log

    def test_custom_exception_reraise_preserves_fields(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            try:
                raise InvalidOrderError("qty", 0, "Qty must be positive")
            except InvalidOrderError:
                raise

        assert exc_info.value.field == "qty"
        assert exc_info.value.value == 0


class TestValidateOrder:
    """Tests for validate_order — robust order validation."""

    def test_valid_order_passes(self):
        result = validate_order("Widget", 3, 9.99)
        assert result == {"product": "Widget", "quantity": 3, "price": 9.99}

    def test_valid_order_with_string_price(self):
        result = validate_order("Gadget", 1, "14.50")
        assert result == {"product": "Gadget", "quantity": 1, "price": 14.5}

    def test_quantity_zero_raises_invalid_order_error(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            validate_order("Widget", 0, 5.0)
        assert exc_info.value.field == "quantity"

    def test_quantity_negative_raises_invalid_order_error(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            validate_order("Widget", -1, 5.0)
        assert exc_info.value.field == "quantity"

    def test_price_negative_raises_invalid_order_error(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            validate_order("Widget", 1, -10.0)
        assert exc_info.value.field == "price"

    def test_empty_product_name_raises_invalid_order_error(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            validate_order("", 1, 5.0)
        assert exc_info.value.field == "product_name"

    def test_whitespace_only_product_name_raises(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            validate_order("   ", 1, 5.0)
        assert exc_info.value.field == "product_name"

    def test_non_numeric_price_raises_invalid_order_error(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            validate_order("Widget", 1, "free")
        assert exc_info.value.field == "price"

    def test_non_string_product_name_raises(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            validate_order(123, 1, 5.0)
        assert exc_info.value.field == "product_name"

    def test_first_error_returned_for_multiple_problems(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            validate_order("", -1, "bad")
        assert exc_info.value.field in ("product_name", "quantity", "price")

    def test_validate_order_collect_shows_all_errors(self):
        with pytest.raises(InvalidOrderError) as exc_info:
            validate_order_collect("", -1, "bad")
        err = exc_info.value
        assert hasattr(err, "all_errors")
        assert len(err.all_errors) >= 2

    def test_price_string_of_zero_is_valid(self):
        result = validate_order("Widget", 1, "0")
        assert result["price"] == 0.0

    def test_quantity_float_valid(self):
        result = validate_order("Widget", 2.5, 10.0)
        assert result["quantity"] == 2
