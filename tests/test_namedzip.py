# -*- coding: utf-8 -*-
"""Tests for the namedzip.namedzip module.

TODO: Clean up and reorganize module.
      Move more boilerplate setup into fixtures.

copyright: (c) 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.

"""

import types
from collections import namedtuple
from itertools import zip_longest
import sys

import pytest

from namedzip import namedzip, namedzip_longest
from namedzip.namedzip import (
    _compare_iterables_to_fields,
    _create_zip,
    _namedzip_v1,
    _namedzip_generator,
    _namedzip_longest_v1,
    _set_defaults,
    _verify_named_tuple,
)


@pytest.fixture()
def two_iterables():
    """Test fixture to provide sample iterables."""

    letters = ["A", "B", "C", "D"]
    numbers = [1, 2, 3, 4]
    return letters, numbers


@pytest.fixture()
def pair_named_tuple():
    """Test fixture to provide sample named tuple."""

    return namedtuple("Pair", ["letter", "number"])


class TestNamedzipSmoke:
    """Smoke tests for `namedzip.namedzip.namedzip`."""

    def test_namedzip_generator_smoke(self, two_iterables):
        """Smoke test for `namedzip` called with iterables."""

        named_tuple = namedtuple("Pair", ["letter", "number"])
        pairs = namedzip(named_tuple, *two_iterables)
        for pair in pairs:
            pair.letter
            pair.number

    def test_namedzip_factory_smoke(self, two_iterables):
        """Smoke test for `namedzip` called without iterables."""

        named_tuple = namedtuple("Pair", ["letter", "number"])
        zip_pairs = namedzip(named_tuple)
        pairs = zip_pairs(*two_iterables)
        for pair in pairs:
            pair.letter
            pair.number


class TestNamedzipIntegration:
    """Collection for `namedzip.namedzip.namedzip`."""

    def test_namedzip_generator_type(self, pair_named_tuple, two_iterables):
        """Returns a generator when called with iterables."""

        pairs = namedzip(pair_named_tuple, *two_iterables)
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_factory_type(self, pair_named_tuple):
        """Returns a function when called without iterables."""

        zip_pairs = namedzip(pair_named_tuple)
        assert isinstance(zip_pairs, types.FunctionType)

    def test_namedzip_yields_namedtuple(self):
        """Verify that `namedzip` generates named tuples."""

        pair_tuple = namedtuple("Pair", ["letter", "number"])
        expected_pair = pair_tuple("A", 1)
        pairs = namedzip(pair_tuple, ("A",), (1,))
        generated_pair = next(pairs)
        assert generated_pair == expected_pair

    @pytest.mark.parametrize(
        "fields, iterables",
        [
            (["letter", "number", "extra"], (["A", "B"], [1, 2])),
            (["letter"], (["A", "B"], [1, 2])),
        ],
    )
    def test_namedzip_iterables_fieldnames_mismatch(self, fields, iterables):
        """Call with non-equal number of iterables and field names.

        Should raise ValueError

        """

        named_tuple = namedtuple("Group", fields)
        with pytest.raises(ValueError):
            namedzip(named_tuple, *iterables)


class TestNamedziplongestSmoke:
    """Smoke tests for `namedzip.namedzip.namedzip_longest`."""

    def test_namedzip_longest_generator_smoke(self, two_iterables):
        """`namedzip_longest` called with iterables."""

        named_tuple = namedtuple("Pair", ["letter", "number"])
        pairs = namedzip_longest(named_tuple, *two_iterables)
        for pair in pairs:
            pair.letter
            pair.number

    def test_namedzip_longest_factory_smoke(self, two_iterables):
        """`namedzip_longest` called without iterables."""

        named_tuple = namedtuple("Pair", ["letter", "number"])
        zip_pairs = namedzip_longest(named_tuple)
        pairs = zip_pairs(*two_iterables)
        for pair in pairs:
            pair.letter
            pair.number


class TestNamedziplongestIntegration:
    """Collection for `namedzip.namedzip.namedzip_longest`."""

    def test_namedzip_longest_generator_type(self, pair_named_tuple, two_iterables):
        """Returns a generator when called with positional args."""

        pairs = namedzip_longest(pair_named_tuple, *two_iterables)
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_longest_factory_type(self, pair_named_tuple):
        """Returns a function when called without positional args."""

        zip_pairs = namedzip_longest(pair_named_tuple)
        assert isinstance(zip_pairs, types.FunctionType)

    def test_namedzip_longest_yields_namedtuple(self, pair_named_tuple):
        """Verify that `namedzip_longest` generates named tuple."""

        expected_pair = pair_named_tuple("A", 1)
        pairs = namedzip_longest(pair_named_tuple, ("A",), (1,))
        generated_pair = next(pairs)
        assert generated_pair == expected_pair

    @pytest.mark.parametrize(
        "fields, iterables",
        [
            (["letter", "number", "extra"], (["A", "B"], [1, 2])),
            (["letter"], (["A", "B"], [1, 2])),
        ],
    )
    def test_namedzip_longest_iterables_fieldnames_mismatch(self, fields, iterables):
        """Call with non-equal number of iterables and field names.

        Should raise ValueError

        """

        named_tuple = namedtuple("Group", fields)
        with pytest.raises(ValueError):
            namedzip_longest(named_tuple, *iterables)

    def test_namedzip_longest_fillvalue(self):
        """Veryfy that the `fillvalue` parameter works."""

        named_tuple = namedtuple("Pair", ["letter", "number"])
        letters = ["A", "B", "C", "D"]
        numbers = [1, 2, 3]
        pairs = namedzip_longest(named_tuple, letters, numbers, fillvalue=99)
        for pair in pairs:
            if pair.letter == "D":
                assert pair.number == 99
                break
        else:
            raise AssertionError("Value assertions were not executed.")

    def test_namedzip_longest_defaults(self):
        """Veryfy that the `defaults` parameter works.

        Includes override of specified `fillvalue`.

        """

        named_tuple = namedtuple("Group", ["letter", "number", "symbol"])
        letters = ["A", "B", "C"]  # len = 3
        numbers = [1, 2, 3, 4]  # len = 4
        symbols = [".", "?", "!"]  # len = 3
        groups = namedzip_longest(
            named_tuple,
            letters,
            numbers,
            symbols,
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

    def test_namedzip_longest_defaults_none_value_not_repalced(self):
        """Veryfy that the `defaults` do not replace None values."""

        named_tuple = namedtuple("Group", ["letter", "number", "symbol"])
        letters = ["A", "B", None]
        numbers = [1, 2, 3]
        symbols = [".", "?", None]
        groups = namedzip_longest(
            named_tuple, letters, numbers, symbols, defaults=["X", 99, "#"]
        )
        for group in groups:
            if group.number == 3:
                assert group.letter is None
                assert group.symbol is None
                break
        else:
            raise AssertionError("Value assertions were not executed.")

    def test_namedzip_longest_too_many_defaults(self):
        """Raises ValueError when too many defaults are specified."""

        named_tuple = namedtuple("Group", ["letter", "number", "symbol"])
        defaults = ("X", 99, "#", "$")
        with pytest.raises(ValueError):
            namedzip_longest(named_tuple, defaults)


class TestDeprecationWarnings:
    """Verify that warnings are issued for deprecated parameters."""

    def test_deprecation_warning_namedzip(self):
        """DeprecationWarning for typename & field_names kwargs."""

        with pytest.warns(DeprecationWarning):
            namedzip(typename="Pair", field_names=("letter", "number"))

    def test_deprecation_warning_namedzip_longest(self):
        """DeprecationWarning for typename & field_names kwargs."""

        with pytest.warns(DeprecationWarning):
            namedzip_longest(typename="Pair", field_names=("letter", "number"))


class TestNamedzipV1Smoke:
    """Smoke tests for `namedzip.namedzip._namedzip_v1`."""

    def test_namedzip_v1_generator_smoke(self, two_iterables):
        """Smoke test for `_namedzip_v1` called with iterables."""

        pairs = _namedzip_v1(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        for pair in pairs:
            pass

    def test_namedzip_v1_factory_smoke(self, two_iterables):
        """Smoke test for `_namedzip_v1` called without iterables."""

        zip_pairs = _namedzip_v1(typename="Pair", field_names=["letter", "number"])
        pairs = zip_pairs(*two_iterables)
        for pair in pairs:
            pass


class TestNamedzipV1Integration:
    """Collection for `namedzip.namedzip._namedzip_v1`."""

    def test_namedzip_v1_generator_type(self, two_iterables):
        """Returns a generator when called with iterables."""

        pairs = _namedzip_v1(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_v1_factory_type(self):
        """`Returns a function when called without iterables."""

        zip_pairs = _namedzip_v1(typename="Pair", field_names=["letter", "number"])
        assert isinstance(zip_pairs, types.FunctionType)

    def test_namedzip_v1_required_keyword_args(self):
        """Requires `typename` and `field_names` keyword arguments."""

        with pytest.raises(TypeError):
            _namedzip_v1()
        with pytest.raises(TypeError):
            _namedzip_v1(typename="Pair")
        with pytest.raises(TypeError):
            _namedzip_v1(field_names=["letter", "number"])

    def test_namedzip_v1_yields_namedtuple(self):
        """Verify that `_namedzip_v1` generates named tuples."""

        pair_tuple = namedtuple("Pair", ["letter", "number"])
        expected_pair = pair_tuple("A", 1)
        pairs = _namedzip_v1(
            ("A",), (1,), typename="Pair", field_names=["letter", "number"]
        )
        generated_pair = next(pairs)
        assert generated_pair == expected_pair

    def test_namedzip_v1_iterables_fieldnames_mismatch(self):
        """Call with non-equal number of iterables and field names.

        Should raise ValueError

        """

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
    """Smoke tests for `namedzip.namedzip._namedzip_longest_v1`."""

    def test_namedzip_longest_v1_generator_smoke(self, two_iterables):
        """`_namedzip_longest_v1` called with iterables."""

        pairs = _namedzip_longest_v1(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        for pair in pairs:
            pass

    def test_namedzip_longest_v1_factory_smoke(self, two_iterables):
        """`_namedzip_longest_v1` called without iterables."""

        zip_pairs = _namedzip_longest_v1(
            typename="Pair", field_names=["letter", "number"]
        )
        pairs = zip_pairs(*two_iterables)
        for pair in pairs:
            pass


class TestNamedziplongestV1Integration:
    """Collection for `namedzip.namedzip._namedzip_longest_v1`."""

    def test_namedzip_longest_v1_generator_type(self, two_iterables):
        """Returns a generator when called with positional args."""

        pairs = _namedzip_longest_v1(
            *two_iterables, typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_longest_v1_factory_type(self):
        """Returns a function when called without positional args."""

        zip_pairs = _namedzip_longest_v1(
            typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(zip_pairs, types.FunctionType)

    def test_namedzip_longest_v1_required_keyword_args(self):
        """Requires `typename` and `field_names` keyword arguments."""

        with pytest.raises(TypeError):
            _namedzip_longest_v1()
        with pytest.raises(TypeError):
            _namedzip_longest_v1(typename="Pair")
        with pytest.raises(TypeError):
            _namedzip_longest_v1(field_names=["letter", "number"])

    def test_namedzip_longest_v1_yields_namedtuple(self):
        """Verify that `_namedzip_longest_v1` generates named tuple."""

        pair_tuple = namedtuple("Pair", ["letter", "number"])
        expected_pair = pair_tuple("A", 1)
        pairs = _namedzip_longest_v1(
            ("A",), (1,), typename="Pair", field_names=["letter", "number"]
        )
        generated_pair = next(pairs)
        assert generated_pair == expected_pair

    def test_namedzip_longest_v1_iterables_fieldnames_mismatch(self, two_iterables):
        """Call with non-equal number of iterables and field names.

        Should raise ValueError

        """

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
        """Non-equal number of field names and defaults.

        Should raise ValueError

        """

        with pytest.raises(ValueError):  # Three field names, two default values.
            _namedzip_longest_v1(
                typename="ABC", field_names=["A", "B", "C"], defaults=[1, 2]
            )
        with pytest.raises(ValueError):  # Three field names, four default values.
            _namedzip_longest_v1(
                typename="ABC", field_names=["A", "B", "C"], defaults=[1, 2, 3, 4]
            )


class TestCompareIterablesToFieldsUnit:
    """Collection; `namedzip.namedzip._compare_iterables_to_fields`."""

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
    """Collection for `namedzip.namedzip._create_zip`."""

    def test__create_zip_defaults(self, two_iterables):
        "Returns instance of `zip` when used with defaults."

        zipped = _create_zip(*two_iterables)
        assert isinstance(zipped, zip)

    def test__create_zip_type_longest_false(self, two_iterables):
        "Returns instance of `zip` when `type_longest` is False."

        zipped = _create_zip(*two_iterables, type_longest=False)
        assert isinstance(zipped, zip)

    def test__create_zip_type_longest_true(self, two_iterables):
        "Returns instance of `zip_longest` if `type_longest` is True."

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
    """Collection for `namedzip.namedzip._namedzip_generator`."""

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


class TestVerifyNamedTuple:
    """Collection for `namedzip.namedzip._verify_named_tuple`."""

    def test__verify_named_tuple_collections_namedtuple(self):
        """Named tuple should not raise exception."""

        named_tuple = namedtuple("Pair", ["letter", "number"])
        _verify_named_tuple(named_tuple)

    @pytest.mark.skipif(
        sys.version_info < (3, 5), reason="Requires Python 3.5 or higher"
    )
    def test__verify_named_tuple_typing_namedtuple(self):
        """Named tuple should not raise exception."""

        from typing import NamedTuple

        named_tuple = NamedTuple("Pair", [("letter", str), ("number", int)])
        _verify_named_tuple(named_tuple)

    @pytest.mark.parametrize(
        "invalid_object",
        [bytes(), dict(), float(), frozenset(), int(), list(), set(), str(), tuple()],
    )
    def test__verify_named_tuple_basic_data_types(self, invalid_object):
        """Basic data types should raise TypeError."""

        with pytest.raises(TypeError):
            _verify_named_tuple(invalid_object)


class TestSetDefaultsUnit:
    """Collection for `namedzip.namedzip._set_defaults`."""

    def test__set_defaults_no_defaults(self):
        """Returns None when no defaults are set."""

        named_tuple = namedtuple("Group", ["letter", "number", "symbol"])
        defaults_arg = None
        fillvalue = "X"
        defaults = _set_defaults(defaults_arg, fillvalue, named_tuple)
        assert defaults is None

    def test__set_defaults_from_delauts_arg_equal_length(self):
        """Returns tuple of default values supplied."""

        named_tuple = namedtuple("Group", ["letter", "number", "symbol"])
        defaults_arg = ["X", 99, "#"]
        fillvalue = None
        defaults = _set_defaults(defaults_arg, fillvalue, named_tuple)
        assert defaults == tuple(defaults_arg)

    def test__set_defaults_from_delauts_arg_shorter(self):
        """Inserts `fillvalue` for leading fields without defaults."""

        named_tuple = namedtuple("Group", ["letter", "number", "symbol"])
        defaults_arg = (99, "#")
        fillvalue = "A"
        defaults = _set_defaults(defaults_arg, fillvalue, named_tuple)
        assert defaults[0] == "A"

    def test__set_defaults_from_delauts_arg_longer(self):
        """Raises ValueError when too many defaults are specified."""

        named_tuple = namedtuple("Group", ["letter", "number", "symbol"])
        defaults_arg = ("X", 99, "#", "$")
        fillvalue = None
        with pytest.raises(ValueError):
            _set_defaults(defaults_arg, fillvalue, named_tuple)

    @pytest.mark.skipif(
        sys.version_info < (3, 7), reason="Requires Python 3.7 or higher"
    )
    def test__set_defaults_from_namedtuple_attribute_equal_length(self):
        """Returns defaults values specified in `named_tuple`."""

        named_tuple = namedtuple(
            "Group", ["letter", "number", "symbol"], defaults=("X", 99, "#")
        )
        defaults_arg = None
        fillvalue = None
        expected = ("X", 99, "#")
        defaults = _set_defaults(defaults_arg, fillvalue, named_tuple)
        assert defaults == expected

    @pytest.mark.skipif(
        sys.version_info < (3, 7), reason="Requires Python 3.7 or higher"
    )
    def test__set_defaults_from_namedtuple_attribute_shorter(self):
        """Returns tuple of defaults values specified in `named_tuple`.

        Padded with `fillvalue` when defaults are fewer than fields.

        """

        named_tuple = namedtuple(
            "Group", ["letter", "number", "symbol"], defaults=(99, "#")
        )
        defaults_arg = None
        fillvalue = "Z"
        expected = ("Z", 99, "#")
        defaults = _set_defaults(defaults_arg, fillvalue, named_tuple)
        assert defaults == expected

    @pytest.mark.skipif(
        sys.version_info < (3, 7), reason="Requires Python 3.7 or higher"
    )
    def test__set_defaults_arg_override(self):
        """Defaults arg overrides named tuple defaults."""

        named_tuple = namedtuple(
            "Group", ["letter", "number", "symbol"], defaults=("X", 99, "#")
        )
        defaults_arg = ["Y", 100, "$"]
        fillvalue = None
        defaults = _set_defaults(defaults_arg, fillvalue, named_tuple)
        assert defaults == tuple(defaults_arg)
