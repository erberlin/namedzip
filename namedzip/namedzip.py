# -*- coding: utf-8 -*-
"""Implements the functionality of the namedzip package.

This module exposes `namedzip` and `namedzip_longest`, which extend
the `zip` and `itertools.zip_longest` to generate named tuples instead
of regular tuples.

References
----------
See documentation for
`zip <https://docs.python.org/3/library/functions.html#zip>`_,
`itertools.zip_longest <https://docs.python.org/3/library/itertools.html#itertools.zip_longest>`_,
and
`collections.namedtuple <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.

"""

from collections import namedtuple


def namedzip(*iterables, typename, field_names, **kwargs):
    """Extends built-in zip to generate named tuples.

    Returns a generator if `*iterables` are supplied, otherwise returns
    a function for creating generators.

    Parameters
    ----------
    *iterables : iterable, optional
        Iterable objects passed as positional arguments.
    typename : string
        Type name for generated named tuple objects. Passed on to
        `collections.namedtuple` factory function.
    field_names : iterable
        Field names for generated named tuple objects.Passed on to
        `collections.namedtuple` factory function.
    **kwargs : type
        Any additional keyword arguments will also be passed on to the
        `collections.namedtuple` factory function.

    Returns
    ------
    generator object
        If `*iterables` are supplied.
    function object
        If `*iterables` are not supplied.

    """

    named_tuple = namedtuple(typename, field_names, **kwargs)

    def _namedzip_factory(*iterables):
        _compare_iterables_to_fields(len(iterables), len(named_tuple._fields))
        zipped = _create_zip(*iterables)
        return _namedzip_generator(zipped, named_tuple)

    if iterables:
        return _namedzip_factory(*iterables)
    else:
        return _namedzip_factory


def namedzip_longest(*iterables, typename, field_names, **kwargs):
    """Extends itertools.zip_longest to generate named tuples.

    Returns a generator if `*iterables` are supplied, otherwise returns
    a function for creating generators.

    Parameters
    ----------
    *iterables : iterable, optional
        Iterable objects passed as positional arguments.
    typename : string
        Type name for generated named tuple objects. Passed on to
        `collections.namedtuple` factory function.
    field_names : iterable
        Field names for generated named tuple objects. Passed on to
        `collections.namedtuple` factory function.
    fillvalue : type, optional
        Use for setting all missing values to the same default value.
        (default is None).
    defaults : iterable, optional
        Individual default values for each iterable to zip. Overrides
        custom `fillvalue` if specified, and length must match the
        number of `*iterables` supplied.
    **kwargs
        Any additional keyword arguments will be passed on to the
        `collections.namedtuple` factory function.

    Returns
    ------
    generator object
        If `*iterables` are supplied.
    function object
        If `*iterables` are not supplied.

    Raises
    ------
    ValueError
        If `defaults` are specified but do not match the number of
        `field_names`.

    """

    fillvalue = kwargs.pop("fillvalue", None)
    defaults = kwargs.pop("defaults", None)
    if defaults:
        # Override fillvalue if individual defaults are specified.
        fillvalue = None
    named_tuple = namedtuple(typename, field_names, **kwargs)
    if defaults and len(defaults) != len(named_tuple._fields):
        raise ValueError(
            "Unequal number of field names ({}) and default values ({}).".format(
                len(named_tuple._fields), len(defaults)
            )
        )

    def _namedzip_longest_factory(*iterables):
        _compare_iterables_to_fields(len(iterables), len(named_tuple._fields))
        zipped = _create_zip(*iterables, fillvalue=fillvalue, type_longest=True)
        return _namedzip_generator(zipped, named_tuple, defaults)

    if iterables:
        return _namedzip_longest_factory(*iterables)
    else:
        return _namedzip_longest_factory


def _compare_iterables_to_fields(iterable_count, field_count):
    """Compare number of iterable object and field names.

    Parameters
    ----------
    iterable_count : int
        Number of iterable objects.
    field_count : int
        Number of named tuple field names.

    Raises
    ------
    ValueError
        If `iterable_count` is not equal to `field_count`.

    """

    if iterable_count != field_count:
        raise ValueError(
            "Unequal number of iterable objects ({}) and field names ({}).".format(
                iterable_count, field_count
            )
        )


def _create_zip(*iterables, fillvalue=None, type_longest=False):
    """Zips supplied iterables and returns a generator.

    Aggregates `*iterables` using `zip` or `zip_longest`, depending on
    the value of the `type_longest` parameter.

    Parameters
    ----------
    *iterables : iterable
        Iterable objects passed as positional arguments. Passed on to
        `zip` or `zip_longest` depending on the `type_longest` flag.
    fillvalue : optional
        Set all missing values to this default value. Only specified
        when called by `namedzip_longest`. (default is None).
    type_longest : bool, optional
        Specifies whether to use `zip_longest` over `zip`. Used by
        `namedzip_longest`. (default is False).

    Returns
    ------
    generator object

    """

    if type_longest:
        from itertools import zip_longest

        zipped = zip_longest(*iterables, fillvalue=fillvalue)
    else:
        zipped = zip(*iterables)
    return zipped


def _namedzip_generator(zipped, named_tuple, defaults=None):
    """Generates named tuple objects.

    Generates named tuple objects from tuples in `zipped`, based on
    the `named_tuple` class. Also replaces None values in `zipped` if
    `defaults` are specified.

    Parameters
    ----------
    zipped : iterable
        Should be generator produced by `zip` or zip_longest`.
    named_tuple : type
        Named tuple class produced by `namedtuple` factory function.
    defaults : iterable or None, optional
        Default values for each index of tuples generated by `zipped`.
        (default is None).

    Yields
    ------
    named tuple object

    """

    for vals in zipped:
        if defaults:
            vals = (x if x is not None else defaults[i] for i, x in enumerate(vals))
        yield named_tuple(*vals)
