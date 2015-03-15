#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'


# Built-in Modules
# Standard Modules
# Custom Modules

"""
Will automatically ensure that all build prerequisites are available
via ez_setup.

Usage:
    python setup.py install
"""
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup
setup(
    name="Skin Detector",
    version="1.0a Prototype",
    url='',
    author='Will Brennan',
    author_email='william.brennan@skytales.com',
    license='GPL',
    install_requires=["numpy"],
)
