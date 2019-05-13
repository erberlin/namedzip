# -*- coding: utf-8 -*-
"""This module implements `namedzip` and `namedzip_longest`, which
extend `zip` and `itertools.zip_longest` respectively to generate
named tuples.

copyright: (c) 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.

"""

from collections import namedtuple
from functools import wraps
from inspect import isclass
import warnings

sentinel = object()


def _deprecation_warning(func):
    """Deprecation warning decorator for old api signatures."""

    deprecation_message = (
        "The typename and field_names parameters will be removed in "
        "namedzip v2.0.0. Please use the named_tuple parameter instead."
    )

    @wraps(func)
    def wrapper(*args, **kwargs):
        deprecated_kwargs = bool(
            "typename" in kwargs.keys() or "field_names" in kwargs.keys()
        )
        if deprecated_kwargs:
            warnings.filterwarnings("always", message=deprecation_message)
            warnings.warn(
                category=DeprecationWarning, message=deprecation_message, stacklevel=2
            )
            if func.__name__ == "namedzip":
                return _namedzip_v1(*args, **kwargs)
            else:
                return _namedzip_longest_v1(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


@_deprecation_warning
def namedzip(named_tuple, *iterables):
    """Extends :func:`zip` to generate named tuples.

    Returns a generator if `*iterables` are supplied, otherwise returns
    a function for creating generators.

    Parameters
    ----------
    named_tuple : tuple subclass
        tuple subclass from `collections.namedtuple` factory function,
        or subclass of `typing.NamedTuple`.
    *iterables : iterable, optional
        Iterable objects to zip.

    Returns
    -------
    generator object
        If `*iterables` are supplied.
    function object
        If `*iterables` are not supplied.

    """

    _verify_named_tuple(named_tuple)

    def _namedzip_factory(*iterables):
        _compare_iterables_to_fields(len(iterables), len(named_tuple._fields))
        zipped = _create_zip(*iterables)
        return _namedzip_generator(zipped, named_tuple)

    if iterables:
        return _namedzip_factory(*iterables)
    else:
        return _namedzip_factory


@_deprecation_warning
def namedzip_longest(named_tuple, *iterables, fillvalue=None, defaults=None):
    """Extends :func:`itertools.zip_longest` to generate named tuples.

    Returns a generator if `*iterables` are supplied, otherwise returns
    a function for creating generators.

    Parameters
    ----------
    named_tuple : tuple subclass
        tuple subclass from `collections.namedtuple` factory function,
        or subclass of `typing.NamedTuple`.
    *iterables : iterable, optional
        Iterable objects to zip.
    fillvalue : optional
        Use for setting all missing values to the same default value.
        (default is None).
    defaults : iterable, optional
        Individual default values for each iterable to zip. Overrides
        `fillvalue` for last n iterables, and any defaults specified in
        `named_tuple`. Length can be less than or equal to the number of
        named tuple field names.

    Returns
    -------
    generator object
        If `*iterables` are supplied.
    function object
        If `*iterables` are not supplied.

    """

    defaults = _set_defaults(defaults, fillvalue, named_tuple)
    if defaults is not None:
        # Override fillvalue when individual defaults are set.
        fillvalue = sentinel

    def _namedzip_longest_factory(*iterables):
        _compare_iterables_to_fields(len(iterables), len(named_tuple._fields))
        zipped = _create_zip(*iterables, fillvalue=fillvalue, type_longest=True)
        return _namedzip_generator(zipped, named_tuple, defaults)

    if iterables:
        return _namedzip_longest_factory(*iterables)
    else:
        return _namedzip_longest_factory


def _namedzip_v1(*iterables, typename, field_names, **kwargs):
    """Extends :func:`zip` to generate named tuples.

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
    **kwargs :
        Any additional keyword arguments will also be passed on to the
        `collections.namedtuple` factory function.

    Returns
    -------
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


def _namedzip_longest_v1(*iterables, typename, field_names, **kwargs):
    """Extends :func:`itertools.zip_longest` to generate named tuples.

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
    fillvalue : optional
        Use for setting all missing values to the same default value.
        Passed on to `itertools.zip_longest` (default is None).
    defaults : iterable, optional
        Individual default values for each iterable to zip. Overrides
        custom `fillvalue` if specified, and length must match the
        number of `*iterables` supplied.
    **kwargs
        Any additional keyword arguments will be passed on to the
        `collections.namedtuple` factory function.

    Returns
    -------
    generator object
        If `*iterables` are supplied.
    function object
        If `*iterables` are not supplied.

    Raises
    ------
    ValueError
        If `defaults` are specified but do not match the number of
        `field_names`.

    Notes
    -----
    Does not utilize the functionality of `collections.namedtuple` for
    setting default values.

    """

    fillvalue = kwargs.pop("fillvalue", None)
    defaults = kwargs.pop("defaults", None)
    named_tuple = namedtuple(typename, field_names, **kwargs)
    if defaults and len(defaults) != len(named_tuple._fields):
        raise ValueError(
            "Unequal number of field names ({}) and default values ({}).".format(
                len(named_tuple._fields), len(defaults)
            )
        )
    elif defaults is not None:
        # Override fillvalue if individual defaults are specified.
        fillvalue = sentinel

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

    Aggregates `*iterables` using `zip` or `itertools.zip_longest`,
    depending on the value of the `type_longest` parameter.

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
    the `named_tuple` class. Also replaces sentinel values in `zipped` if
    `defaults` are specified.

    Parameters
    ----------
    zipped : iterable
        Should be generator produced by `zip` or zip_longest`.
    named_tuple : tuple subclass
        tuple subclass from `collections.namedtuple` factory function,
        or subclass of `typing.NamedTuple`.
    defaults : iterable or None, optional
        Default values for each index of tuples generated by `zipped`.
        (default is None).

    Yields
    ------
    named tuple object

    """

    for vals in zipped:
        if defaults:
            vals = (x if x is not sentinel else defaults[i] for i, x in enumerate(vals))
        yield named_tuple(*vals)


def _set_defaults(defaults, fillvalue, named_tuple):
    """Set default values to be used by `_namedzip_generator`.

    Set values form `defaults` if not None, otherwise check if default
    values are specified in the `named_tuple` class.

    Defaults are applied to the last n fields similar to how the
    `defaults` parameter of `collections.namedtuple` works. If fewer
    defaults than field names are specified, missing (leading) default
    values will be set to `fillvalue`.

    Parameters
    ----------
    defaults : iterable or None
        Specified as keyword argument to `namedzip_longest` interface.
    fillvalue :
        Specified as keyword argument to `namedzip_longest` interface.
    named_tuple : tuple subclass
        tuple subclass from `collections.namedtuple` factory function,
        or subclass of `typing.NamedTuple`.

    Returns
    -------
    tuple or None

    Raises
    ------
    ValueError
        If the number of default values is larger than the number of
        named tuple field names.

    """

    if defaults is not None:
        # Default values specified in interface kwarg take priority.
        defaults = tuple(defaults)
        if len(defaults) > len(named_tuple._fields):
            raise ValueError(
                "Received more default values ({}) than field names ({}).".format(
                    len(defaults), len(named_tuple._fields)
                )
            )
        elif len(named_tuple._fields) > len(defaults):
            padded_defaults = [fillvalue] * (len(named_tuple._fields) - len(defaults))
            padded_defaults.extend(defaults)
            defaults = tuple(padded_defaults)
    else:
        # Defaults attribute can be called `_field_defaults` or `_fields_defaults`.
        nt_defaults = getattr(named_tuple, "_fields_defaults", None) or getattr(
            named_tuple, "_field_defaults", None
        )
        if nt_defaults:  # Can be empty dict.
            defaults = tuple(
                nt_defaults.get(field, fillvalue) for field in (named_tuple._fields)
            )
    return defaults


def _verify_named_tuple(named_tuple):
    """Attempt to verify `named_tuple` object.

    Parameters
    ----------
    named_tuple : named tuple class
        tuple subclass from `collections.namedtuple` factory function,
        or subclass of `typing.NamedTuple`.

    Raises
    ------
    TypeError
        If `named_tuple` does not appear to be a named tuple class.

    """

    if not bool(
        isclass(named_tuple)
        and issubclass(named_tuple, tuple)
        and callable(named_tuple)
        and hasattr(named_tuple, "_fields")
    ):
        raise TypeError(
            "named_tuple parameter should be a tuple subclass created "
            "by the collections.namedtuple factory function, or a "
            "subclass of typing.NamedTuple."
        )
