# -*- coding: utf-8 -*-
"""
Tests for the namedzip.namedzip module.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.
"""
import types
import pytest
from collections import namedtuple
from namedzip import namedzip, namedzip_longest


@pytest.fixture()
def sample_iterables():
    """Test fixture to provide sample iterables."""
    letters = ["A", "B", "C", "D"]
    numbers = [1, 2, 3, 4]
    return letters, numbers


class TestNamedzip:
    """Collection of tests for `namedzip.namedzip`."""

    def test_namedzip_smoke(self, sample_iterables):
        """Check that a `namedzip` generator can be initialized and iterated through."""
        pairs = namedzip(
            *sample_iterables, typename="Pair", field_names=["letter", "number"]
        )
        for pair in pairs:
            pass

    def test_namedzip_type(self, sample_iterables):
        """Verify that `namedzip()` returns a generator object."""
        pairs = namedzip(
            *sample_iterables, typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_yields_namedtuple(self):
        """Verify that `namedzip` generates named tuples."""
        pair_tuple = namedtuple("Pair", ["letter", "number"])
        expected_pair = pair_tuple("A", 1)
        pairs = namedzip(
            ("A",), (1,), typename="Pair", field_names=["letter", "number"]
        )
        generated_pair = next(pairs)
        assert generated_pair == expected_pair

    def test_namedzip_iterables_fieldnames_mismatch(self, sample_iterables):
        """ValueError is raiesd for non-equal number of iterables and field names"""
        with pytest.raises(ValueError):  # Two iterabes, three field names.
            namedzip(
                *sample_iterables,
                typename="Pair",
                field_names=["letter", "number", "extra"]
            )
        with pytest.raises(ValueError):  # Two iterabes, one field name.
            namedzip(*sample_iterables, typename="Pair", field_names=["letter"])

    def test_namedzip_non_iterable_arg(self):
        """TypeError is raised for non-iterable object."""
        # Unnecessary since it's raised by zip()?
        with pytest.raises(TypeError):
            namedzip("A", 1, typename="Pair", field_names=["letter", "number"])


class TestNamedziplongest:
    """Collection of tests for `namedzip.namedzip_longest`."""

    def test_namedzip_longest_smoke(self, sample_iterables):
        """Check that a `namedzip_longest` generator can be initialized and iterated."""
        pairs = namedzip_longest(
            *sample_iterables, typename="Pair", field_names=["letter", "number"]
        )
        for pair in pairs:
            pass

    def test_namedzip_longest_type(self, sample_iterables):
        """Verify that `namedzip()` returns a generator object."""
        pairs = namedzip_longest(
            *sample_iterables, typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_longest_yields_namedtuple(self):
        """Verify that `namedzip_longest` generates named tuple."""
        pair_tuple = namedtuple("Pair", ["letter", "number"])
        expected_pair = pair_tuple("A", 1)
        pairs = namedzip_longest(
            ("A",), (1,), typename="Pair", field_names=["letter", "number"]
        )
        generated_pair = next(pairs)
        assert generated_pair == expected_pair

    def test_namedzip_longest_iterables_fieldnames_mismatch(self, sample_iterables):
        """ValueError is raiesd for non-equal number of iterables and field names"""
        with pytest.raises(ValueError):  # Two iterabes, three field names.
            namedzip_longest(
                *sample_iterables,
                typename="Pair",
                field_names=["letter", "number", "extra"]
            )
        with pytest.raises(ValueError):  # Two iterabes, one field name.
            namedzip_longest(*sample_iterables, typename="Pair", field_names=["letter"])

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
        letters = ["A", "B", "C"]
        numbers = [1, 2, 3, 4]
        symbols = [".", "?", "!"]
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
