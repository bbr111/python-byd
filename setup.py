#!/usr/bin/env python3
"""Script to set up the BYD B-Box API wrapper."""
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="python-byd",
    version="0.0.1",
    description="Python Wrapper for interacting with the BYD B-Box API.",
    long_description=long_description,
    url="https://github.com/bbr111/python-byd",
    download_url="https://github.com/bbr111/python-byd/releases",
    author="Benjamin Bräuer",
    author_email="",
    license="GNU General Public License v3.0",
    install_requires=[
    ],
    packages=["byd"],
    python_requires=">=3.9",
    zip_safe=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
)
