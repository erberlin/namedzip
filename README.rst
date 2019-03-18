========
namedzip
========
|license|

.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://lbesson.mit-license.org/

This package implements ``namedzip`` and ``namedzip_longest``, which extend ``zip`` and ``itertools.zip_longest`` respectively to generate named tuples using ``collections.namedtuple``.

Installation
------------
.. code-block:: shell

    $ git clone https://github.com/erberlin/namedzip.git
    $ cd namedzip
    $ pip install .

Usage examples
--------------
.. code:: python

   >>> from namedzip import namedzip, namedzip_longest

``namedzip`` and ``namedzip_longest`` can either be used **with iterable positional
arguments**, like the functions which they extend, to return generator objects:

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

Development setup
-----------------
Clone repo and create virtual environment:

.. code-block:: shell

   $ git clone https://github.com/erberlin/namedzip.git
   $ cd namedzip
   $ python -m venv venv

Activate virtual environment on Windows:

.. code-block:: shell

   > venv\Scripts\activate

Activate virtual environment on OS X & Linux:

.. code-block:: shell

   $ source venv/bin/activate

Install required packages:

.. code-block:: shell

   $ pip install requirements.txt

Run test suite:

.. code-block:: shell

   $ pytest -v

Meta
----

Erik R Berlin – erberlin.dev@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

https://github.com/erberlin/namedzip