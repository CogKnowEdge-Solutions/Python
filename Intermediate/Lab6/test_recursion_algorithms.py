"""Tests for Lab 6 — Recursion & Algorithms.

Covers:
- Recursive factorial
- Recursive Fibonacci
- Recursive sum
- Linear search
- Bubble sort
- Palindrome check (recursive)
"""
import pytest


def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def recursive_sum(lst):
    if len(lst) == 0:
        return 0
    return lst[0] + recursive_sum(lst[1:])


def linear_search(lst, target):
    for i, val in enumerate(lst):
        if val == target:
            return i
    return -1


def bubble_sort(lst):
    arr = lst[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def is_palindrome(s):
    s = s.lower().replace(" ", "")
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])


class TestFactorial:
    def test_base_case_zero(self):
        assert factorial(0) == 1

    def test_base_case_one(self):
        assert factorial(1) == 1

    def test_five(self):
        assert factorial(5) == 120

    def test_ten(self):
        assert factorial(10) == 3628800

    def test_negative_raises_error(self):
        with pytest.raises(ValueError):
            factorial(-1)


class TestFibonacci:
    def test_zero(self):
        assert fibonacci(0) == 0

    def test_one(self):
        assert fibonacci(1) == 1

    def test_six(self):
        assert fibonacci(6) == 8

    def test_ten(self):
        assert fibonacci(10) == 55


class TestRecursiveSum:
    def test_empty_list(self):
        assert recursive_sum([]) == 0

    def test_three_elements(self):
        assert recursive_sum([1, 2, 3]) == 6

    def test_with_negatives(self):
        assert recursive_sum([10, -5, 3]) == 8

    def test_single_element(self):
        assert recursive_sum([42]) == 42

    def test_large_list(self):
        assert recursive_sum(list(range(1, 101))) == 5050


class TestLinearSearch:
    def test_found_returns_index(self):
        assert linear_search([10, 20, 30, 40], 30) == 2

    def test_not_found_returns_minus_one(self):
        assert linear_search([10, 20, 30], 99) == -1

    def test_first_occurrence_returned(self):
        assert linear_search([5, 3, 5, 7, 5], 5) == 0

    def test_empty_list(self):
        assert linear_search([], 1) == -1

    def test_found_at_end(self):
        assert linear_search([1, 2, 3, 4, 5], 5) == 4

    def test_found_at_start(self):
        assert linear_search([1, 2, 3, 4, 5], 1) == 0


class TestBubbleSort:
    def test_unsorted(self):
        assert bubble_sort([64, 34, 25, 12, 22]) == [12, 22, 25, 34, 64]

    def test_already_sorted(self):
        assert bubble_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert bubble_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_empty(self):
        assert bubble_sort([]) == []

    def test_single_element(self):
        assert bubble_sort([42]) == [42]

    def test_duplicates(self):
        assert bubble_sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]

    def test_does_not_mutate_original(self):
        original = [5, 3, 1]
        bubble_sort(original)
        assert original == [5, 3, 1]

    def test_negatives_and_positives(self):
        assert bubble_sort([-3, 5, -1, 0, 2]) == [-3, -1, 0, 2, 5]


class TestPalindrome:
    def test_racecar(self):
        assert is_palindrome("racecar") is True

    def test_hello(self):
        assert is_palindrome("hello") is False

    def test_empty_string(self):
        assert is_palindrome("") is True

    def test_single_char(self):
        assert is_palindrome("a") is True

    def test_case_insensitive(self):
        assert is_palindrome("Racecar") is True

    def test_two_chars_same(self):
        assert is_palindrome("aa") is True

    def test_two_chars_different(self):
        assert is_palindrome("ab") is False

    def test_longer_not_palindrome(self):
        assert is_palindrome("programming") is False

    def test_sentence_with_spaces(self):
        assert is_palindrome("nurses run") is True
