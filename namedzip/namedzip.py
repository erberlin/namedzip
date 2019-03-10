# -*- coding: utf-8 -*-
"""
This module implements namedzip(), which extends zip() to generate named tuples instead
of regular tuples.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.
"""
from collections import namedtuple


def namedzip(*iterables, typename, field_names, **kwargs):
    """Extends zip() to generate named tuples.

    Works like the built-in `zip` function, but requires two additional keyword
    arguments used for the `namedtuple` factory function.

    See https://docs.python.org/3/library/functions.html#zip
    and https://docs.python.org/3/library/collections.html#collections.namedtuple
    for documentation on `zip` and `collections.namedtuple`.

    Parameters
    ----------
    iterables : iterable
        Tuple of iterable objects passed as positional arguments.
        Passed on to `zip` function.
    typename : string
        Name for generated named tuple objects.
        Passed on to `namedtuple` factory function.
    field_names : iterable
        Field names for generated named tuple objects.
        Passed on to `namedtuple` factory function.
    **kwargs : type
        Any additional keyword arguments will also be passed on to the `namedtuple`
        factory function. See link above for `collections.namedtuple` documentation.

    Yields
    ------
    named tuple object
        Holds values from each supplied iterable aggregated by `zip`.

    Raises
    ------
    ValueError
        If the number of iterables does not match the number of field names.

    Examples
    --------
    >>> from namedzip import namedzip
    >>> arr1 = ["A", "B", "C"]
    >>> arr2 = [1, 2, 3]
    >>> pairs = namedzip(arr1, arr2, typename="Pair", field_names=["letter", "number"])
    >>> for pair in pairs:
    ...     print(pair)
    ...     print(pair.letter * pair.number)
    ...
    Pair(letter='A', number=1)
    A
    Pair(letter='B', number=2)
    BB
    Pair(letter='C', number=3)
    CCC

    """
    named_tuple = namedtuple(typename, field_names, **kwargs)
    if len(iterables) != len(named_tuple._fields):
        raise ValueError(
            "Number of iterable objects ({}) and field names ({}) do not match.".format(
                len(iterables), len(named_tuple._fields)
            )
        )
    zipped = zip(*iterables)

    def generator():
        for vals in zipped:
            yield named_tuple(*vals)

    return generator()


def namedzip_longest(
    *iterables, typename, field_names, fillvalue=None, defaults=None, **kwargs
):
    """Extends itertools.zip_longest() to generate named tuples."""
    from itertools import zip_longest

    named_tuple = namedtuple(typename, field_names, **kwargs)
    if len(iterables) != len(named_tuple._fields):
        raise ValueError(
            "Number of iterable objects ({}) and field names ({}) do not match.".format(
                len(iterables), len(named_tuple._fields)
            )
        )
    if defaults and len(defaults) != len(named_tuple._fields):
        raise ValueError(
            "Number of field names ({}) and default values ({}) do not match.".format(
                len(named_tuple._fields), len(defaults)
            )
        )
    if defaults:
        # Override fillvalue if individual defaults are specified.
        fillvalue = None
    zipped = zip_longest(*iterables, fillvalue=fillvalue)

    def generator():
        for vals in zipped:
            if defaults:
                vals = (x if x is not None else defaults[i] for i, x in enumerate(vals))
            yield named_tuple(*vals)

    return generator()
