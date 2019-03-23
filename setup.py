from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name="namedzip",
    version="1.0.5",
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
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["namedzip"],
    python_requires=">=3.4",
)
