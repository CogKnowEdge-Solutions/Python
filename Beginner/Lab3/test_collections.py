"""Tests for Lab 3 — Collections.

Covers:
- Lists: creation, indexing, slicing, methods, nesting
- Dictionaries: creation, access, update, methods, nesting
- Sets: creation, operations (union, intersection, difference)
- Tuples: creation, immutability, packing/unpacking
"""
import pytest


class TestLists:
    """Test list operations."""

    def test_create_list(self):
        scores = [88, 92, 79, 93, 85]
        assert scores == [88, 92, 79, 93, 85]

    def test_indexing(self):
        scores = [88, 92, 79, 93, 85]
        assert scores[0] == 88
        assert scores[-1] == 85

    def test_slicing(self):
        scores = [88, 92, 79, 93, 85]
        assert scores[1:3] == [92, 79]

    def test_append(self):
        scores = [88, 92, 79]
        scores.append(95)
        assert scores[-1] == 95
        assert len(scores) == 4

    def test_extend(self):
        scores = [88, 92]
        scores.extend([79, 93])
        assert scores == [88, 92, 79, 93]

    def test_insert(self):
        scores = [88, 92, 79]
        scores.insert(1, 95)
        assert scores[1] == 95

    def test_remove(self):
        scores = [88, 92, 79]
        scores.remove(92)
        assert 92 not in scores

    def test_pop(self):
        scores = [88, 92, 79]
        last = scores.pop()
        assert last == 79
        assert len(scores) == 2

    def test_sort_ascending(self):
        scores = [88, 92, 79, 93, 85]
        scores.sort()
        assert scores == [79, 85, 88, 92, 93]

    def test_sort_descending(self):
        scores = [88, 92, 79, 93, 85]
        scores.sort(reverse=True)
        assert scores == [93, 92, 88, 85, 79]

    def test_min_max_sum(self):
        scores = [88, 92, 79, 93, 85]
        assert min(scores) == 79
        assert max(scores) == 93
        assert sum(scores) == 437

    def test_list_comprehension(self):
        squares = [x ** 2 for x in range(1, 6)]
        assert squares == [1, 4, 9, 16, 25]

    def test_nesting(self):
        matrix = [[1, 2], [3, 4], [5, 6]]
        assert matrix[1][0] == 3
        assert len(matrix) == 3


class TestDictionaries:
    """Test dictionary operations."""

    def test_create_dict(self):
        person = {"name": "Ana", "age": 22, "gpa": 3.8}
        assert person["name"] == "Ana"

    def test_access_with_get(self):
        person = {"name": "Ana"}
        assert person.get("age") is None
        assert person.get("age", 0) == 0

    def test_add_entry(self):
        person = {"name": "Ana"}
        person["age"] = 22
        assert person["age"] == 22

    def test_update_entry(self):
        person = {"name": "Ana", "age": 22}
        person["age"] = 23
        assert person["age"] == 23

    def test_keys_values_items(self):
        person = {"name": "Ana", "age": 22}
        assert "name" in person.keys()
        assert 22 in person.values()
        assert ("name", "Ana") in person.items()

    def test_remove_entry(self):
        person = {"name": "Ana", "age": 22}
        del person["age"]
        assert "age" not in person

    def test_merge_dicts(self):
        defaults = {"color": "blue", "size": "medium"}
        custom = {"color": "red"}
        result = {**defaults, **custom}
        assert result["color"] == "red"
        assert result["size"] == "medium"

    def test_nested_dict(self):
        students = {
            "Ana": {"math": 95, "science": 88},
            "Ben": {"math": 78, "science": 92}
        }
        assert students["Ana"]["math"] == 95
        assert students["Ben"]["science"] == 92

    def test_dict_comprehension(self):
        squares = {x: x**2 for x in range(1, 6)}
        assert squares == {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}


class TestSets:
    """Test set operations."""

    def test_create_set(self):
        grades = {"A", "B", "C", "D", "F"}
        assert len(grades) == 5

    def test_add_remove(self):
        grades = {"A", "B"}
        grades.add("C")
        assert "C" in grades
        grades.remove("B")
        assert "B" not in grades

    def test_membership(self):
        grades = {"A", "B", "C", "D", "F"}
        assert "A" in grades
        assert "Z" not in grades

    def test_union(self):
        a = {1, 2, 3}
        b = {3, 4, 5}
        assert a | b == {1, 2, 3, 4, 5}

    def test_intersection(self):
        a = {1, 2, 3, 4}
        b = {3, 4, 5, 6}
        assert a & b == {3, 4}

    def test_difference(self):
        a = {1, 2, 3, 4}
        b = {3, 4, 5, 6}
        assert a - b == {1, 2}
        assert b - a == {5, 6}

    def test_symmetric_difference(self):
        a = {1, 2, 3}
        b = {2, 3, 4}
        assert a ^ b == {1, 4}

    def test_set_from_list(self):
        items = [1, 2, 2, 3, 3, 3]
        unique = set(items)
        assert unique == {1, 2, 3}


class TestTuples:
    """Test tuple operations."""

    def test_create_tuple(self):
        point = (3, 4)
        assert point[0] == 3
        assert point[1] == 4

    def test_immutable(self):
        point = (3, 4)
        with pytest.raises(TypeError):
            point[0] = 5

    def test_unpacking(self):
        coords = (10, 20, 30)
        x, y, z = coords
        assert x == 10
        assert y == 20
        assert z == 30

    def test_tuple_from_list(self):
        items = [1, 2, 3]
        t = tuple(items)
        assert t == (1, 2, 3)
        with pytest.raises(TypeError):
            t[0] = 99

    def test_tuple_count(self):
        t = (1, 2, 2, 3, 2)
        assert t.count(2) == 3

    def test_tuple_index(self):
        t = (10, 20, 30)
        assert t.index(20) == 1
