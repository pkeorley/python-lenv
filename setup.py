# Copyright © 2024 pkeorley
#
# This source code is licensed under the MIT license found in the LICENSE
# file in the root directory of this source tree.

from setuptools import setup, find_packages


def get_long_description() -> str:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
    return long_description


setup(
    name="python-lenv",
    author="pkeorley",
    author_email='pkeorley@gmail.com',

    url='https://github.com/pkeorley/python-lenv',
    version="0.1.0",

    license='MIT',
    license_files=['LICENSE'],

    python_requires='>=3.10',
    packages=find_packages(exclude=['.venv']),
    install_requires=["python-dotenv==1.0.1"],

    description="Quickly and efficiently load environment variables into a class",
    long_description=get_long_description(),
    long_description_content_type='text/markdown'
)
