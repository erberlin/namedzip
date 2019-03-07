from collections import namedtuple


def namedzip(*iterables, typename, field_names, **kwargs):
    """Extends zip() to generate named tuples."""
    named_tuple = namedtuple(typename, field_names, **kwargs)
    if len(iterables) != len(named_tuple._fields):
        raise ValueError(
            "Number of iterable objects ({}) and field names ({}) do not match.".format(
                len(iterables), len(named_tuple._fields)
            )
        )
    for zipped in zip(*iterables):
        yield named_tuple(*zipped)
