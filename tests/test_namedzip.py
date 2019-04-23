# -*- coding: utf-8 -*-
"""Tests for the namedzip.namedzip module.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.

"""

import types
from collections import namedtuple
from itertools import zip_longest

import pytest

from namedzip import namedzip, namedzip_longest
from namedzip.namedzip import (
    _compare_iterables_to_fields,
    _create_zip,
    _namedzip_v1,
    _namedzip_generator,
    _namedzip_longest_v1,
)


@pytest.fixture()
def two_iterables():
    """Test fixture to provide sample iterables."""
    letters = ["A", "B", "C", "D"]
    numbers = [1, 2, 3, 4]
    return letters, numbers


class TestNamedzipV1Smoke:
    """Smoke tests for `namedzip.namedzip.namedzip`."""

    def test_namedzip_v1_generator_smoke(self, two_iterables):
        """Smoke test for `namedzip` called with iterable positional arguments."""
        pairs = _namedzip_v1(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        for pair in pairs:
            pass

    def test_namedzip_v1_factory_smoke(self, two_iterables):
        """Smoke test for `namedzip` called without iterable positional arguments."""
        zip_pairs = _namedzip_v1(typename="Pair", field_names=["letter", "number"])
        pairs = zip_pairs(*two_iterables)
        for pair in pairs:
            pass


class TestUnitNamedzipV1:
    """Collection of tests for `namedzip.namedzip.namedzip`."""

    def test_namedzip_v1_generator_type(self, two_iterables):
        """`namedzip` returns a generator when called with positional arguments."""
        pairs = _namedzip_v1(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_v1_factory_type(self):
        """`namedzip` returns a function when called without positional arguments."""
        zip_pairs = _namedzip_v1(typename="Pair", field_names=["letter", "number"])
        assert isinstance(zip_pairs, types.FunctionType)

    def test_namedzip_v1_required_keyword_args(self):
        """`namedzip` requires `typename` and `field_names` keyword arguments."""
        with pytest.raises(TypeError):
            _namedzip_v1()
        with pytest.raises(TypeError):
            _namedzip_v1(typename="Pair")
        with pytest.raises(TypeError):
            _namedzip_v1(field_names=["letter", "number"])

    def test_namedzip_v1_yields_namedtuple(self):
        """Verify that `namedzip` generates named tuples."""
        pair_tuple = namedtuple("Pair", ["letter", "number"])
        expected_pair = pair_tuple("A", 1)
        pairs = _namedzip_v1(
            ("A",), (1,), typename="Pair", field_names=["letter", "number"]
        )
        generated_pair = next(pairs)
        assert generated_pair == expected_pair

    def test_namedzip_v1_iterables_fieldnames_mismatch(self):
        """ValueError is raiesd for non-equal number of iterables and field names"""
        iterables = (["A", "B"], [1, 2])
        with pytest.raises(ValueError):  # Two iterabes, three field names.
            _namedzip_v1(
                *iterables, typename="Pair", field_names=["letter", "number", "extra"]
            )
        with pytest.raises(ValueError):  # Two iterabes, one field name.
            _namedzip_v1(*iterables, typename="Pair", field_names=["letter"])

    def test_namedzip_v1_non_iterable_arg(self):
        """TypeError is raised for non-iterable object."""
        # Unnecessary since it's raised by zip()?
        with pytest.raises(TypeError):
            _namedzip_v1("A", 1, typename="Pair", field_names=["letter", "number"])


class TestNamedziplongestV1Smoke:
    """Smoke tests for `namedzip.namedzip.namedzip_longest`."""

    def test_namedzip_longest_v1_generator_smoke(self, two_iterables):
        """Smoke test for `namedzip_longest` called with iterable positional args."""
        pairs = _namedzip_longest_v1(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        for pair in pairs:
            pass

    def test_namedzip_longest_v1_factory_smoke(self, two_iterables):
        """Smoke test for `namedzip_longest` called without iterable positional args."""
        zip_pairs = _namedzip_longest_v1(
            typename="Pair", field_names=["letter", "number"]
        )
        pairs = zip_pairs(*two_iterables)
        for pair in pairs:
            pass


class TestNamedziplongestV1:
    """Collection of tests for `namedzip.namedzip.namedzip_longest`."""

    def test_namedzip_longest_v1_generator_type(self, two_iterables):
        """`namedzip_longest` returns a generator when called with positional args."""
        pairs = _namedzip_longest_v1(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_longest_v1_factory_type(self):
        """`namedzip_longest` returns a function when called without positional args."""
        zip_pairs = _namedzip_longest_v1(
            typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(zip_pairs, types.FunctionType)

    def test_namedzip_longest_v1_required_keyword_args(self):
        """`namedzip` requires `typename` and `field_names` keyword arguments."""
        with pytest.raises(TypeError):
            _namedzip_longest_v1()
        with pytest.raises(TypeError):
            _namedzip_longest_v1(typename="Pair")
        with pytest.raises(TypeError):
            _namedzip_longest_v1(field_names=["letter", "number"])

    def test_namedzip_longest_v1_yields_namedtuple(self):
        """Verify that `namedzip_longest` generates named tuple."""
        pair_tuple = namedtuple("Pair", ["letter", "number"])
        expected_pair = pair_tuple("A", 1)
        pairs = _namedzip_longest_v1(
            ("A",), (1,), typename="Pair", field_names=["letter", "number"]
        )
        generated_pair = next(pairs)
        assert generated_pair == expected_pair

    def test_namedzip_longest_v1_iterables_fieldnames_mismatch(self, two_iterables):
        """ValueError is raiesd for non-equal number of iterables and field names"""
        iterables = (["A", "B"], [1, 2])
        with pytest.raises(ValueError):  # Two iterabes, three field names.
            _namedzip_longest_v1(
                *iterables, typename="Pair", field_names=["letter", "number", "extra"]
            )
        with pytest.raises(ValueError):  # Two iterabes, one field name.
            _namedzip_longest_v1(*iterables, typename="Pair", field_names=["letter"])

    def test_namedzip_longest_v1_non_iterable_arg(self):
        """TypeError is raised for non-iterable object."""
        # Unnecessary since it's raised by zip_longest()?
        with pytest.raises(TypeError):
            _namedzip_longest_v1(
                "A", 1, typename="Pair", field_names=["letter", "number"]
            )

    def test_namedzip_longest_v1_fillvalue(self):
        """Veryfy that the `fillvalue` parameter works."""
        letters = ["A", "B", "C", "D"]
        numbers = [1, 2, 3]
        pairs = _namedzip_longest_v1(
            letters,
            numbers,
            typename="Pair",
            field_names=["letter", "number"],
            fillvalue=99,
        )
        for pair in pairs:
            if pair.letter == "D":
                assert pair.number == 99
                break
        else:
            raise AssertionError("Value assertions were not executed.")

    def test_namedzip_longest_v1_defaults(self):
        """Veryfy that the `defaults` parameter works.

        Includes override of specified `fillvalue`.
        """
        letters = ["A", "B", "C"]  # len = 3
        numbers = [1, 2, 3, 4]  # len = 4
        symbols = [".", "?", "!"]  # len = 3
        groups = _namedzip_longest_v1(
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
                break
        else:
            raise AssertionError("Value assertions were not executed.")

    def test_namedzip_longest_v1_defaults_none_value_not_repalced(self):
        """Veryfy that the `defaults` do not replace None values."""
        letters = ["A", "B", None]
        numbers = [1, 2, 3]
        symbols = [".", "?", None]
        groups = _namedzip_longest_v1(
            letters,
            numbers,
            symbols,
            typename="Group",
            field_names=["letter", "number", "symbol"],
            defaults=["X", 99, "#"],
        )
        for group in groups:
            if group.number == 3:
                assert group.letter is None
                assert group.symbol is None
                break
        else:
            raise AssertionError("Value assertions were not executed.")

    def test_namedzip_longest_v1_fieldnames_defaults_mismatch(self, two_iterables):
        """ValueError is raiesd for non-equal number of field names and defaults"""
        with pytest.raises(ValueError):  # Three field names, two default values.
            _namedzip_longest_v1(
                typename="ABC", field_names=["A", "B", "C"], defaults=[1, 2]
            )
        with pytest.raises(ValueError):  # Three field names, four default values.
            _namedzip_longest_v1(
                typename="ABC", field_names=["A", "B", "C"], defaults=[1, 2, 3, 4]
            )


class TestCompareIterablesToFieldsUnit:
    """Collection of tests for `namedzip.namedzip._compare_iterables_to_fields`."""

    def test__compare_iterables_to_fields_equal(self):
        "No exception is raised when passed two equal integers."
        _compare_iterables_to_fields(2, 2)
        _compare_iterables_to_fields(100, 100)

    def test__compare_iterables_to_fields_unequal(self):
        "ValueError is raised when passed two unequal integers."

        with pytest.raises(ValueError):
            _compare_iterables_to_fields(1, 2)
        with pytest.raises(ValueError):
            _compare_iterables_to_fields(1, 0)


class TestCreateZipUnit:
    """Collection of tests for `namedzip.namedzip._create_zip`."""

    def test__create_zip_defaults(self, two_iterables):
        "Returns instance of `zip` when used with defaults."

        zipped = _create_zip(*two_iterables)
        assert isinstance(zipped, zip)

    def test__create_zip_type_longest_false(self, two_iterables):
        "Returns instance of `zip` when `type_longest` is False."

        zipped = _create_zip(*two_iterables, type_longest=False)
        assert isinstance(zipped, zip)

    def test__create_zip_type_longest_true(self, two_iterables):
        "Returns instance of `zip_longest` when `type_longest` is True."

        zipped = _create_zip(*two_iterables, type_longest=True)
        assert isinstance(zipped, zip_longest)

    def test__create_zip_default_fillvalue_none(self):
        "Defalut `fillvalue` should be None when not specified."

        iterables = (("A", "B", "C"), (1, 2))
        zipped = _create_zip(*iterables, type_longest=True)
        for z in zipped:
            pairs = z
        assert pairs[-1] is None

    def test__create_zip_custom_fillvalue(self):
        "Custom `fillvalue` should replace missing value."

        iterables = (("A", "B", "C"), (1, 2))
        zipped = _create_zip(*iterables, fillvalue=99, type_longest=True)
        for z in zipped:
            pairs = z
        assert pairs[-1] == 99


class TestNamedzipGeneratorUnit:
    """Collection of tests for `namedzip.namedzip._namedzip_generator`."""

    def test__namedzip_generator_return_type(self):
        """Should return a generator object."""

        zipped = zip(("A", "B", "C"), (1, 2, 3))
        named_tuple = namedtuple("Pair", ["letter", "number"])
        nz_generator = _namedzip_generator(zipped, named_tuple)
        assert isinstance(nz_generator, types.GeneratorType)

    def test__namedzip_generator_yields_named_tuple(self):
        """Returned object should yield named tuples."""

        zipped = zip(("A", "B", "C"), (1, 2, 3))
        named_tuple = namedtuple("Pair", ["letter", "number"])
        expected = named_tuple("A", 1)
        nz_generator = _namedzip_generator(zipped, named_tuple)
        yielded = next(nz_generator)
        assert yielded == expected
