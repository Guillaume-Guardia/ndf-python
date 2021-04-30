#!/usr/bin/env python

from setuptools import setup

setup(
    name="pyndf",
    version="0.1.0",
    author="Guillaume Guardia",
    author_email="guardia.1903@apside-groupe.com",
    packages=["pyndf"],
    package_dir={"": "src"},
    package_data={"pyndf": ["data/test.xlsx"]},
    # url="http://pypi.python.org/pypi/ndf-python/",
    license="LICENSE.txt",
    description="Do NDF for Apside",
    long_description=open("README.md").read(),
    install_requires=[],
)
