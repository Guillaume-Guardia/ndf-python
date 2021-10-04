#!/usr/bin/env python

import sys
import glob
import os
from setuptools import find_packages, setup
import py2exe

with open("requirements.txt") as f:
    required = f.read().splitlines()

sys.path.append(__file__)


def find_data_files(source, target, patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.
    source is the root of the source data tree.
    Use '' or '.' for current directory.
    target is the root of the target data tree.
    Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
    files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source, pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target, os.path.relpath(filename, source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path, []).append(filename)
    return sorted(ret.items())


setup(
    name="pyndf",
    version="1.2",
    author="Guillaume Guardia",
    author_email="guardia.1903@apside-groupe.com",
    packages=find_packages(where="src"),
    package_dir={"pyndf": "src/pyndf"},
    package_data={"pyndf": ["conf/*", "data/*", "data/icons/*"]},
    license="LICENSE.txt",
    description="Do NDF for Apside",
    long_description=open("README.md").read(),
    install_requires=required,
    data_files=find_data_files(
        "src/pyndf", "", ["conf/*", "data/*", "data/icons/*", "data/translations/*", "db/*.db", "../../README.md"]
    ),
    console=["src/pyndf/main.py"],
    options={
        "py2exe": {
            "includes": [
                "PyQt6.sip",
                "PyQt6.QtCore",
                "PyQt6.QtGui",
                "PyQt6.QtWidgets",
                "sqlalchemy.sql.default_comparator",
                "sqlalchemy.ext.baked",
                "reportlab.rl_settings",
                "sqlalchemy.dialects.sqlite",
            ],
            "excludes": ["py"],
        }
    },
)
