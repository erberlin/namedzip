========
namedzip
========
|license| |pypi| |pyversions| |wheel| |build| |docs|

.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://lbesson.mit-license.org/
.. |pypi| image:: https://img.shields.io/pypi/v/namedzip.svg
   :target: https://pypi.org/project/namedzip/
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/namedzip.svg
.. |wheel| image:: https://img.shields.io/pypi/wheel/namedzip.svg
.. |build| image:: https://img.shields.io/circleci/project/github/erberlin/namedzip/master.svg
.. |docs| image:: https://img.shields.io/readthedocs/namedzip.svg
   :target: https://namedzip.readthedocs.io/en/latest/

This Python package implements ``namedzip`` and ``namedzip_longest``, which extend ``zip`` and ``itertools.zip_longest`` respectively to generate named tuples.

Installation
------------
.. code-block:: shell

    $ pip install namedzip

Usage examples
--------------
.. code:: python

   >>> from namedzip import namedtuple, namedzip, namedzip_longest

``namedzip`` and ``namedzip_longest`` can either be used **with iterable arguments**,
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

Just like ``itertools.zip_longest``, ``namedzip_longest`` takes a custom ``fillvalue``.

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

However ``namedzip_longest`` also allows for the use of individual default
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

How could this be useful?
-------------------------
The idea behind this package is to help improve readability in cases where
you have a need to iterate over multiple collections/streams of data, as well
as to allow for individual default values like show above.

Instead of messing with indices or unpacking long tuples, ``namedzip`` allows you
to access aggregated values by attribute names using dot notation.

.. code:: python

   sensor_data = [fahrenheit_vals, humidity_vals, wind_mph_vals, pressure_hpa_vals]

   Data = namedtuple("Data", ("temp_f", "humidity", "wind_mph", "pressure_hpa"))
   zip_data = namedzip_longest(Data, defaults=(57.2, 68.3, 17.1, 1016.93))   

   for data in zip_data(*sensor_data):
       temp_c = (data.temp_f - 32) / 1.8
       wind_knots = data.wind_mph / 1.15078
       pressure_atm = data.pressure_hpa / 1013.25
       dew_point = calculate_dew_point(temp_c, data.humidity)

   # NOTE: The formulas used above may not be accurate.

Documentation
-------------
Additional documentation is available at https://namedzip.readthedocs.io/en/latest/.

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

Meta
----

Erik R Berlin - erberlin.dev@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

https://github.com/erberlin/namedzip