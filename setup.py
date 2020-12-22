#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2020 TheCoder777
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pathlib
import sys
from setuptools import setup

ROOT = pathlib.Path(__file__).parent

# readme
with open(ROOT / "README.md") as file:
    README = file.read()

# dependencies
with open(ROOT / "requirements.txt") as file:
    REQUIREMENTS = file.read().splitlines()

# system version < 3.6
if sys.version_info < (3, 6):
    raise SystemExit("Report Booklet Writer requires Python version 3.6+, consider upgrading.")

setup(
    name="rbwriter",
    scripts=["scripts/rbwriter"],
    author="Paul S.",
    author_email="thecoder777.github@gmail.com",
    url="https://github.com/TheCoder777/Report-Booklet-Writer",
    license="MIT",
    description="The Python web frontend to generate your pixel perfect report booklet",
    long_description=README,
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://github.com/TheCoder777/Report-Booklet-Writer",
        "Issues": "https://github.com/TheCoder777/Report-Booklet-Writer/issues"
    },
    # major.minor alpha/beta
    version="0.1a2",
    packages=["rbwriter"],
    include_package_data=True,
    install_requirements=REQUIREMENTS,
    python_requires=">=3.6.0",
    keywords=["front-end",
              "frontend",
              "frontend-web",
              "web-application",
              "frontend-app",
              "report-booklet",
              "booklet",
              "writer"],
    platforms=["unix", "linux", "osx"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Utilities",
    ]
)