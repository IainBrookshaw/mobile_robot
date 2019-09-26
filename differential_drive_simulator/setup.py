#! /usr/bin/env python3
"""
Differential Drive Robot: Setup & Install
Iain Brookshaw
21 September 2019
"""

import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="differential_drive_simulator",
    version="0.0.1",
    author="Iain Brookshaw",
    author_email="iain.j.brookshaw@gmail.com",
    description="Simulation of Differential Drive robot odometry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    scripts=["ddrive.py"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: Linux"
    ],
    install_requires=[
        'numpy>=1.17.2',
        'matplotlib>=3.1.1'
    ],
    python_requires='>=3.6'
)
