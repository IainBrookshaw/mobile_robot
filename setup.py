#! /usr/bin/env python3
"""
Mobile Robot: Setup & Install
Iain Brookshaw
21 September 2019
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mobilerobot",
    version="0.1.4",
    author="Iain Brookshaw",
    author_email="iain.j.brookshaw@gmail.com",
    description="useful tools for mobile robots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    scripts=[
        "demos/ddrive.py",
        "demos/a_star_demo.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux"
    ],
    install_requires=[
        'typing>=3.7.4.1',
        'scipy>=1.3.1',
        'numpy>=1.17.2',
        'matplotlib>=3.1.1'
    ],
    python_requires='>=3.6'
)
