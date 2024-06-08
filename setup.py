# Copyright © 2024 pkeorley
#
# This source code is licensed under the MIT license found in the LICENSE
# file in the root directory of this source tree.

from lenv import (
    __version__,
    __author__,
    __description__
)

from setuptools import setup, find_packages


def get_long_description() -> str:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
    return long_description


setup(
    name="lenv",
    author=__author__,
    author_email='pkeorley@gmail.com',

    url='https://github.com/pkeorley/lenv',
    version=__version__,

    license='MIT',
    licence_files=['LICENSE'],

    python_requires='>=3.10',
    packages=find_packages(exclude=['.venv']),
    install_requires=["python-dotenv==1.0.1"],

    description=__description__,
    long_description=get_long_description(),
    long_description_content_type='text/markdown'
)
