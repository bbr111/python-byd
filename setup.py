#!/usr/bin/env python3
"""Script to set up the BYD B-Box API wrapper."""
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bydhvs",
    version="0.2.0",
    description="A module for communicating with the BYD HVS Battery system",
    long_description=long_description,
    url="https://github.com/bbr111/python-bydhvs",
    download_url="https://github.com/bbr111/python-bydhvs/releases",
    author="bbr111",
    author_email="ben1@gmx.net",
    license="GPL-3.0",
    install_requires=[
        "asyncio",
        "logging"
    ],
    packages=["bydhvs"],
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
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Utilities",
    ],
)
