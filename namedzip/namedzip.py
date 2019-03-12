# -*- coding: utf-8 -*-
"""
This module implements namedzip() and namedzip_longest(), which extend zip() and
itertools.zip_longest() to generate named tuples instead of regular tuples.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.
"""
from collections import namedtuple


def namedzip(*iterables, typename, field_names, **kwargs):
    """Extends zip() to generate named tuples.

    Returns a `namedzip` generator if `*iterables` are supplied, otherwise
    returns a function for creating `namedzip` generators from iterables.

    See https://docs.python.org/3/library/functions.html#zip for documentation on `zip`
    and https://docs.python.org/3/library/collections.html#collections.namedtuple for
    documentation on `collections.namedtuple`.

    Parameters
    ----------
    *iterables : iterable, optional
        Iterable objects passed as positional arguments.
    typename : string
        Type name for generated named tuple objects.
        Passed on to `namedtuple` factory function.
    field_names : iterable
        Field names for generated named tuple objects.
        Passed on to `namedtuple` factory function.
    **kwargs : type
        Any additional keyword arguments will also be passed on to the `namedtuple`
        factory function. See link above for `collections.namedtuple` documentation.

    Returns
    ------
    generator object
        If `*iterables` are supplied.
    function object
        If `*iterables` are not supplied.

    """
    named_tuple = namedtuple(typename, field_names, **kwargs)

    def _namedzip_factory(*iterables):
        return _create_namedzip(*iterables, named_tuple=named_tuple)

    if iterables:
        return _namedzip_factory(*iterables)
    else:
        return _namedzip_factory


def namedzip_longest(*iterables, typename, field_names, **kwargs):
    """Extends itertools.zip_longest() to generate named tuples.

    Returns a `namedzip_longest` generator if `*iterables` are supplied, otherwise
    returns a function for creating `namedzip_longest` generators from iterables.

    See https://docs.python.org/3/library/itertools.html#itertools.zip_longest
    and https://docs.python.org/3/library/collections.html#collections.namedtuple
    for documentation on `itertools.zip_longest` and `collections.namedtuple`.

    Parameters
    ----------
    *iterables : iterable, optional
        Iterable objects passed as positional arguments.
    typename : string
        Name for generated named tuple objects.
        Passed on to `namedtuple` factory function.
    field_names : iterable
        Field names for generated named tuple objects.
        Passed on to `namedtuple` factory function.
    fillvalue : type, optional
        Use for setting all missing values to the same default value. (default is None).
    defaults : iterable, optional
        Individual default values for each iterable to zip. Overrides custom `fillvalue`
        if specified, and length must match the number of `*iterables` supplied.
    **kwargs : type
        Any additional keyword arguments will be passed on to the `namedtuple` factory
        function. See link above for `collections.namedtuple` documentation.

    Returns
    ------
    generator object
        If `*iterables` are supplied.
    function object
        If `*iterables` are not supplied.

    Raises
    ------
    ValueError
        If `defaults` are specified but do not match the number of `field_names`.

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
        return _create_namedzip(
            *iterables,
            named_tuple=named_tuple,
            fillvalue=fillvalue,
            defaults=defaults,
            type_longest=True
        )

    if iterables:
        return _namedzip_longest_factory(*iterables)
    else:
        return _namedzip_longest_factory


def _create_namedzip(
    *iterables, named_tuple, fillvalue=None, defaults=None, type_longest=False
):
    """Zips supplied iterables and returns a generator.

    Aggregates `*iterables` using `zip` or `zip_longest`, and returns a generator which
    yields named tuples instead of regular tuples.

    Parameters
    ----------
    *iterables : iterable
        Iterable objects passed as positional arguments. Passed on to `zip` or
        `zip_longest` depending on the `type_longest` flag.
    named_tuple : type
        Named tuple class produced by the `namedtuple` factory function.
    fillvalue : type, optional
        Used for setting all missing values to the same default value. Only specified
        when called by `namedzip_longest`, i.e. when `type_longest` is True.
        (default is None).
    defaults : iterable, optional
        Individual default values for each iterable to zip. Only specified when called
        by `namedzip_longest`, i.e. when `type_longest` is True. (default is None).
    type_longest : bool, optional
        Specifies whether to use `zip_longest` over `zip`. (default is False).
        Used by `namedzip_longest`.

    Returns
    ------
    generator object

    Raises
    ------
    ValueError
        If the number of `*iterables` supplied does not match the number of field names
        in `named_tuple`.

    """
    if len(iterables) != len(named_tuple._fields):
        raise ValueError(
            "Unequal number of iterable objects ({}) and field names ({}).".format(
                len(iterables), len(named_tuple._fields)
            )
        )
    if type_longest:
        from itertools import zip_longest

        zipped = zip_longest(*iterables, fillvalue=fillvalue)
    else:
        zipped = zip(*iterables)
    return _namedzip_generator(zipped, named_tuple, defaults)


def _namedzip_generator(zipped, named_tuple, defaults):
    """Generates named tuple objects.

    Generates named tuple objects from iterables in `zipped`, based on the `named_tuple`
    class. Also replaces None values in `zipped` if `defaults` are specified.

    Parameters
    ----------
    zipped : iterable
        Should be generator produced by `zip` or zip_longest`.
    named_tuple : type
        Named tuple class produced by the `namedtuple` factory function.
    defaults : iterable or None
        Individual default values for each position of tuples generated by `zipped`.

    Yields
    ------
    named tuple object.

    """
    for vals in zipped:
        if defaults:
            vals = (x if x is not None else defaults[i] for i, x in enumerate(vals))
        yield named_tuple(*vals)
