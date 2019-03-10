# -*- coding: utf-8 -*-
"""
    Tests for the namedzip.namedzip module.

    copyright: © 2019 by Erik R Berlin.
    license: MIT, see LICENSE for more details.
"""
import types
import pytest
from collections import namedtuple
from namedzip import namedzip


@pytest.fixture()
def sample_iterables():
    """Test fixture to provide sample iterables."""
    letters = ["A", "B", "C", "D"]
    numbers = [1, 2, 3, 4]
    return letters, numbers


class TestNamedzip:
    def test_namedzip_smoke(self, sample_iterables):
        """Check that a namedzip generator can be initialized and iterated through."""
        pairs = namedzip(
            *sample_iterables, typename="Pair", field_names=["letter", "number"]
        )
        for pair in pairs:
            pass

    def test_namedzip_type(self, sample_iterables):
        """Verify that namedzip() returns a generator object."""
        pairs = namedzip(
            *sample_iterables, typename="Pair", field_names=["letter", "number"]
        )
        assert isinstance(pairs, types.GeneratorType)

    def test_namedzip_yields_namedtuple(self):
        """Verify that namedzip() generates named tuple."""
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
