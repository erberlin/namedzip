import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.rst").read_text()

setup(
    name="namedzip",
    version="1.0.0",
    description="Extends zip() and itertools.zip_longest() to generate named tuples.",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/erberlin/namedzip",
    author="Erik R Berlin",
    author_email="erberlin.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["namedzip"],
    include_package_data=False,
)
