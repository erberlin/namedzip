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

This Python package implements ``namedzip`` and ``namedzip_longest``, which extend ``zip`` and ``itertools.zip_longest`` respectively to generate named tuples using ``collections.namedtuple``.

Installation
------------
.. code-block:: shell

    $ pip install namedzip

Usage examples
--------------
.. code:: python

   >>> from namedzip import namedzip, namedzip_longest

``namedzip`` and ``namedzip_longest`` can either be used **with iterable positional
arguments**, like the interfaces which they extend, to return generator objects:

.. code:: python

   >>> iterables = (["A", "B", "C"], [1, 2, 3])
   >>> pairs = namedzip(*iterables, typename="Pair", field_names=("letter", "number"))
   >>> for pair in pairs:
   ...     print(pair)
   ...
   Pair(letter='A', number=1)
   Pair(letter='B', number=2)
   Pair(letter='C', number=3)
   >>>
   >>> iterables = (["A", "B"], [1, 2, 3])
   >>> pairs = namedzip_longest(*iterables, typename="Pair", field_names=("letter", "number"), defaults=("X", 99))
   >>> for pair in pairs:
   ...     print(pair)
   ...
   Pair(letter='A', number=1)
   Pair(letter='B', number=2)
   Pair(letter='X', number=3)
   >>>

Or **without positional arguments** to return reusable function objects:

.. code:: python

   >>> zip_pairs = namedzip(typename="Pair", field_names=("letter", "number"))
   >>> pairs = zip_pairs(["A", "B", "C"], [1, 2, 3])
   >>> for pair in pairs:
   ...     print(pair)
   ...
   Pair(letter='A', number=1)
   Pair(letter='B', number=2)
   Pair(letter='C', number=3)
   >>>
   >>> zip_pairs = namedzip_longest(typename="Pair", field_names=("letter", "number"), defaults=("X", 99))
   >>> pairs = zip_pairs(["A", "B", "C"], [1, 2])
   >>> for pair in pairs:
   ...     print(pair)
   ...
   Pair(letter='A', number=1)
   Pair(letter='B', number=2)
   Pair(letter='C', number=99)
   >>>

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