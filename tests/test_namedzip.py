# -*- coding: utf-8 -*-
"""
Tests for the namedzip.namedzip module.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.
"""
import types
from collections import namedtuple

import pytest
from namedzip import namedzip, namedzip_longest


@pytest.fixture()
def two_iterables():
    """Test fixture to provide sample iterables."""
    letters = ["A", "B", "C", "D"]
    numbers = [1, 2, 3, 4]
    return letters, numbers


class TestNamedzip:
    """Collection of tests for `namedzip.namedzip`."""

    def test_namedzip_generator_smoke(self, two_iterables):
        """Smoke test for `namedzip` called with iterable positional arguments."""
        pairs = namedzip(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        for pair in pairs:
            pass

    def test_namedzip_factory_smoke(self, two_iterables):
        """Smoke test for `namedzip` called without iterable positional arguments."""
        zip_pairs = namedzip(typename="Pair", field_names=["letter", "number"])
        pairs = zip_pairs(*two_iterables)
        for pair in pairs:
            pass

    def test_namedzip_generator_type(self, two_iterables):
        """`namedzip` returns a generator when called with positional arguments."""
        pairs = namedzip(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_factory_type(self):
        """`namedzip` returns a function when called without positional arguments."""
        zip_pairs = namedzip(typename="Pair", field_names=["letter", "number"])
        assert isinstance(zip_pairs, types.FunctionType)

    def test_namedzip_required_keyword_args(self):
        """`namedzip` requires `typename` and `field_names` keyword arguments."""
        with pytest.raises(TypeError):
            namedzip()
        with pytest.raises(TypeError):
            namedzip(typename="Pair")
        with pytest.raises(TypeError):
            namedzip(field_names=["letter", "number"])

    def test_namedzip_yields_namedtuple(self):
        """Verify that `namedzip` generates named tuples."""
        pair_tuple = namedtuple("Pair", ["letter", "number"])
        expected_pair = pair_tuple("A", 1)
        pairs = namedzip(
            ("A",), (1,), typename="Pair", field_names=["letter", "number"]
        )
        generated_pair = next(pairs)
        assert generated_pair == expected_pair

    def test_namedzip_iterables_fieldnames_mismatch(self):
        """ValueError is raiesd for non-equal number of iterables and field names"""
        iterables = (["A", "B"], [1, 2])
        with pytest.raises(ValueError):  # Two iterabes, three field names.
            namedzip(
                *iterables, typename="Pair", field_names=["letter", "number", "extra"]
            )
        with pytest.raises(ValueError):  # Two iterabes, one field name.
            namedzip(*iterables, typename="Pair", field_names=["letter"])

    def test_namedzip_non_iterable_arg(self):
        """TypeError is raised for non-iterable object."""
        # Unnecessary since it's raised by zip()?
        with pytest.raises(TypeError):
            namedzip("A", 1, typename="Pair", field_names=["letter", "number"])


class TestNamedziplongest:
    """Collection of tests for `namedzip.namedzip_longest`."""

    def test_namedzip_longest_generator_smoke(self, two_iterables):
        """Smoke test for `namedzip_longest` called with iterable positional args."""
        pairs = namedzip_longest(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        for pair in pairs:
            pass

    def test_namedzip_longest_factory_smoke(self, two_iterables):
        """Smoke test for `namedzip_longest` called without iterable positional args."""
        zip_pairs = namedzip_longest(typename="Pair", field_names=["letter", "number"])
        pairs = zip_pairs(*two_iterables)
        for pair in pairs:
            pass

    def test_namedzip_longest_generator_type(self, two_iterables):
        """`namedzip_longest` returns a generator when called with positional args."""
        pairs = namedzip_longest(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_longest_factory_type(self):
        """`namedzip_longest` returns a function when called without positional args."""
        zip_pairs = namedzip_longest(typename="Pair", field_names=["letter", "number"])
        assert isinstance(zip_pairs, types.FunctionType)

    def test_namedzip_longest_required_keyword_args(self):
        """`namedzip` requires `typename` and `field_names` keyword arguments."""
        with pytest.raises(TypeError):
            namedzip_longest()
        with pytest.raises(TypeError):
            namedzip_longest(typename="Pair")
        with pytest.raises(TypeError):
            namedzip_longest(field_names=["letter", "number"])

    def test_namedzip_longest_yields_namedtuple(self):
        """Verify that `namedzip_longest` generates named tuple."""
        pair_tuple = namedtuple("Pair", ["letter", "number"])
        expected_pair = pair_tuple("A", 1)
        pairs = namedzip_longest(
            ("A",), (1,), typename="Pair", field_names=["letter", "number"]
        )
        generated_pair = next(pairs)
        assert generated_pair == expected_pair

    def test_namedzip_longest_iterables_fieldnames_mismatch(self, two_iterables):
        """ValueError is raiesd for non-equal number of iterables and field names"""
        iterables = (["A", "B"], [1, 2])
        with pytest.raises(ValueError):  # Two iterabes, three field names.
            namedzip_longest(
                *iterables, typename="Pair", field_names=["letter", "number", "extra"]
            )
        with pytest.raises(ValueError):  # Two iterabes, one field name.
            namedzip_longest(*iterables, typename="Pair", field_names=["letter"])

    def test_namedzip_longest_non_iterable_arg(self):
        """TypeError is raised for non-iterable object."""
        # Unnecessary since it's raised by zip_longest()?
        with pytest.raises(TypeError):
            namedzip_longest("A", 1, typename="Pair", field_names=["letter", "number"])

    def test_namedzip_longest_fillvalue(self):
        """Veryfy that the `fillvalue` parameter works."""
        letters = ["A", "B", "C", "D"]
        numbers = [1, 2, 3]
        pairs = namedzip_longest(
            letters,
            numbers,
            typename="Pair",
            field_names=["letter", "number"],
            fillvalue=99,
        )
        for pair in pairs:
            if pair.letter == "D":
                assert pair.number == 99

    def test_namedzip_longest_defaults(self):
        """Veryfy that the `defaults` parameter works.

        Includes override of specified `fillvalue`.
        """
        letters = ["A", "B", "C"]  # len = 3
        numbers = [1, 2, 3, 4]  # len = 4
        symbols = [".", "?", "!"]  # len = 3
        groups = namedzip_longest(
            letters,
            numbers,
            symbols,
            typename="Group",
            field_names=["letter", "number", "symbol"],
            fillvalue="Missing",  # Should be overridden by defaults parameter.
            defaults=["X", 99, "#"],
        )
        for group in groups:
            if group.number == 4:
                assert group.letter == "X"
                assert group.symbol == "#"

    def test_namedzip_longest_fieldnames_defaults_mismatch(self, two_iterables):
        """ValueError is raiesd for non-equal number of field names and defaults"""
        with pytest.raises(ValueError):  # Three field names, two default values.
            namedzip_longest(
                typename="ABC", field_names=["A", "B", "C"], defaults=[1, 2]
            )
        with pytest.raises(ValueError):  # Three field names, four default values.
            namedzip_longest(
                typename="ABC", field_names=["A", "B", "C"], defaults=[1, 2, 3, 4]
            )
