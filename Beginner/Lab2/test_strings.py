"""Tests for Lab 2 — Strings.

Covers:
- String indexing and slicing
- String methods (upper, lower, split, strip, etc.)
- f-strings and format()
- String concatenation and repetition
- Membership and length checks
"""
import pytest


class TestStringBasics:
    """Test string indexing and slicing."""

    def test_indexing_first_char(self):
        name = "Python"
        assert name[0] == "P"

    def test_indexing_last_char(self):
        name = "Python"
        assert name[-1] == "n"

    def test_slicing_first_three(self):
        word = "abcdefghij"
        assert word[:3] == "abc"

    def test_slicing_middle(self):
        word = "abcdefghij"
        assert word[2:5] == "cde"

    def test_slicing_from_end(self):
        word = "abcdefghij"
        assert word[-3:] == "hij"

    def test_stride(self):
        word = "abcdefghij"
        assert word[::2] == "acegi"

    def test_reverse_string(self):
        word = "Python"
        assert word[::-1] == "nohtyP"


class TestStringMethods:
    """Test built-in string methods."""

    def test_upper(self):
        assert "hello".upper() == "HELLO"

    def test_lower(self):
        assert "HELLO".lower() == "hello"

    def test_title(self):
        assert "hello world".title() == "Hello World"

    def test_capitalize(self):
        assert "hello world".capitalize() == "Hello world"

    def test_strip_whitespace(self):
        assert "  hello  ".strip() == "hello"

    def test_strip_specific_char(self):
        assert "###hello###".strip("#") == "hello"

    def test_replace(self):
        sentence = "I love cats"
        assert sentence.replace("cats", "dogs") == "I love dogs"

    def test_count(self):
        sentence = "banana"
        assert sentence.count("a") == 3

    def test_find(self):
        assert "hello world".find("world") == 6

    def test_find_not_present(self):
        assert "hello world".find("xyz") == -1

    def test_startswith(self):
        assert "Hello, World!".startswith("Hello")

    def test_endswith(self):
        assert "Hello, World!".endswith("World!")

    def test_join(self):
        words = ["Hello", "Python"]
        assert " ".join(words) == "Hello Python"

    def test_split(self):
        sentence = "I love Python"
        result = sentence.split()
        assert result == ["I", "love", "Python"]

    def test_split_with_separator(self):
        csv_line = "apple,banana,cherry"
        result = csv_line.split(",")
        assert result == ["apple", "banana", "cherry"]


class TestFStrings:
    """Test f-string formatting."""

    def test_basic_fstring(self):
        name = "Ana"
        result = f"My name is {name}"
        assert result == "My name is Ana"

    def test_fstring_with_expression(self):
        x = 5
        y = 3
        result = f"{x} + {y} = {x + y}"
        assert result == "5 + 3 = 8"

    def test_fstring_decimal_format(self):
        pi = 3.14159
        result = f"{pi:.2f}"
        assert result == "3.14"

    def test_fstring_padding(self):
        name = "Ana"
        result = f"{name:>10}"
        assert result == "       Ana"

    def test_format_method(self):
        template = "Hello, {}! You are {} years old."
        result = template.format("Ana", 22)
        assert result == "Hello, Ana! You are 22 years old."

    def test_format_with_names(self):
        result = "{greeting}, {name}!".format(greeting="Hello", name="World")
        assert result == "Hello, World!"


class TestConcatenationAndRepetition:
    """Test string concatenation and repetition."""

    def test_concatenation(self):
        result = "Hello" + " " + "World"
        assert result == "Hello World"

    def test_repetition(self):
        result = "ha" * 3
        assert result == "hahaha"

    def test_string_with_number_error(self):
        name = "Ana"
        age = 22
        with pytest.raises(TypeError):
            result = name + " is " + age + " years old"

    def test_string_with_number_correct(self):
        name = "Ana"
        age = 22
        result = name + " is " + str(age) + " years old"
        assert result == "Ana is 22 years old"


class TestMembershipAndLength:
    """Test membership and length checks."""

    def test_length(self):
        assert len("Python") == 6

    def test_empty_string_length(self):
        assert len("") == 0

    def test_membership_true(self):
        assert "Py" in "Python"

    def test_membership_false(self):
        assert "xyz" not in "Python"

    def test_comparison(self):
        assert "abc" == "abc"
        assert "abc" != "ABC"
