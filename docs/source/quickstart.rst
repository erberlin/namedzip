Quickstart
==========

:func:`namedzip` and :func:`namedzip_longest` extend :func:`zip` and :func:`itertools.zip_longest`
respectively to generate named tuples.

Installation
------------
.. code-block:: shell

    $ pip install namedzip

Usage examples
--------------
.. code:: python

   >>> from namedzip import namedtuple, namedzip, namedzip_longest

:func:`namedzip` and :func:`namedzip_longest` can either be used **with iterable arguments**,
like the interfaces which they extend, to return generator objects:

.. code:: python

   >>> x_vals = [1, 2, 3]
   >>> y_vals = [9, 8]
   >>> Point = namedtuple("Point", ["x", "y"])
   >>>
   >>> for point in namedzip(Point, x_vals, y_vals):
   ...     print(point)
   ...
   Point(x=1, y=9)
   Point(x=2, y=8)
   >>>
   >>> for point in namedzip_longest(Point, x_vals, y_vals):
   ...     print(point)
   ...
   Point(x=1, y=9)
   Point(x=2, y=8)
   Point(x=3, y=None)
   >>>

Or **without iterable arguments** to return reusable function objects:

.. code:: python

   >>> zip_points = namedzip(Point)
   >>> for point in zip_points(x_vals, y_vals):
   ...     print(point)
   ...
   Point(x=1, y=9)
   Point(x=2, y=8)
   >>>
   >>> zip_points = namedzip_longest(Point)
   >>> for point in zip_points(x_vals, y_vals):
   ...     print(point)
   ...
   Point(x=1, y=9)
   Point(x=2, y=8)
   Point(x=3, y=None)
   >>>

Default values
--------------

Just like :func:`itertools.zip_longest`, :func:`namedzip_longest` takes a custom ``fillvalue``.

.. code:: python

   >>> iterables = [(1, 2), (9, 8, 7), (11, 22)]
   >>> Point3D = namedtuple("Point3D", ["x", "y", "z"])
   >>>
   >>> for point in namedzip_longest(Point3D, *iterables, fillvalue=0):
   ...     print(point)
   ...
   Point3D(x=1, y=9, z=11)
   Point3D(x=2, y=8, z=22)
   Point3D(x=0, y=7, z=0)
   >>>

However :func:`namedzip_longest` also allows for the use of individual default
values specified in the named tuple or in the function call.

.. code:: python

   >>> iterables = [(1, 2), (9, 8, 7), (11, 22)]
   >>> Point3D = namedtuple("Point3D", ["x", "y", "z"], defaults=(100, 1, 0))
   >>>
   >>> for point in namedzip_longest(Point3D, *iterables):
   ...     print(point)
   ...
   Point3D(x=1, y=9, z=11)
   Point3D(x=2, y=8, z=22)
   Point3D(x=100, y=7, z=0)
   >>>
   >>> for point in namedzip_longest(Point3D, *iterables, defaults=(77, 88, 99)):
   ...     print(point)
   ...
   Point3D(x=1, y=9, z=11)
   Point3D(x=2, y=8, z=22)
   Point3D(x=77, y=7, z=99)
   >>>

Individual default values are applied to the last n iterables, and the ``fillvalue``
will be used for leading iterables if fewer ``defaults`` are specified.

.. code:: python

   >>> for point in namedzip_longest(Point3D, *iterables, fillvalue="fill", defaults=(88,)):
   ...     print(point)
   ...
   Point3D(x=1, y=9, z=11)
   Point3D(x=2, y=8, z=22)
   Point3D(x='fill', y=7, z=88)
   >>>

Note that any default values set in a named tuple will be ignored if the ``defaults``
keyword argument is specified for :func:`namedzip_longest`. 

Named tuple classes for the ``named_tuple`` arg
-----------------------------------------------

The ``named_tuple`` argument can either be a tuple subclass from the :func:`collections.namedtuple`
factory function or a subclass of :class:`typing.NamedTuple`.

.. code:: python

   from namedzip import namedzip
   from collections import namedtuple
   from typing import NamedTuple

   Cell1 = namedtuple("Cell1", ["row", "column"])

   Cell2 = NamedTuple('Cell2', [('row', int), ('column', str)])

   class Cell3(NamedTuple):
       row: int
       column: str

   cell_zip1 = namedzip(Cell1)
   cell_zip2 = namedzip(Cell2)
   cell_zip3 = namedzip(Cell3)

:func:`collections.namedtuple` is also availabe for import from the `namedzip` package.

.. code:: python

   from namedzip import namedtuple

Development setup
-----------------
Clone repo:

.. code-block:: shell

   $ git clone https://github.com/erberlin/namedzip.git
   $ cd namedzip

Create and activate virtual environment on Windows:

.. code-block:: shell

   > python -m venv venv
   > venv\Scripts\activate

Create and activate virtual environment on OS X & Linux:

.. code-block:: shell

   $ python3 -m venv venv
   $ source venv/bin/activate

Install development packages:

.. code-block:: shell

   $ pip install -r requirements.txt

Run test suite:

.. code-block:: shell

   $ pytest -v
