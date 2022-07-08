# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# The version string is stored in only one place
#   so get it from msgen.py.
from msgen_cli import msgen

with open('README.rst') as readme:
    long_description = ''.join(readme).strip()

setup(
    name='msgen',
    version=msgen.VERSION,
    author='Microsoft Corporation, Microsoft Genomics Team',
    author_email='msgensupp@microsoft.com',
    description='Microsoft Genomics Command-line Client',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    platforms='any',
    url='https://github.com/microsoft/msgen',
    license='MIT',
    packages=['msgen_cli'],
    py_modules=['msgen_cli.msgen'],
    entry_points={
        'console_scripts': 'msgen=msgen_cli.msgen:main',
    },
    install_requires=[
        'azure-storage-blob==12.12.0',
        'requests>=2.11.1',
    ],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],

    keywords='azure genomics',
)
