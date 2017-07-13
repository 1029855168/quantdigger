# -*- coding: utf-8 -*-
from codecs import open

from setuptools import setup, find_packages

with open("README.rst", "r", "utf-8") as f:
    readme = f.read()

setup(
    name="QuantDigger",
    version="0.5.0",
    description="量化交易Python回测系统,python 3.5版",
    long_description=readme,
    author="QuantFans",
    author_email="dingjie.wang@foxmail.com",
    license="MIT",
    url="https://github.com/qink1986/quantdigger",
    packages=find_packages(exclude=['tests', 'demo', "requirements", "images", "setupscripts"]),
    include_package_data=True,
    install_requires=[
        "requests>=2.18.1",
        "beautifulsoup4>=4.6.0",
        "lxml>=3.5.0",
        "tushare>=0.8.2",
        "logbook>=0.12.5",
        "ta-lib>=0.4.8",
        "progressbar2>=3.6.2",
        "matplotlib>=1.5.1",
        "pandas>=0.20.2",
        "python-dateutil>=2.6.1",
        "numpy>=1.10.4",
        "pymongo>=3.1.1",
        "pyzmq>=4.1.5",
        #"cython>=0.23.4",
    ],
    classifiers=[
        #'Environment :: Finance',
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        "Programming Language :: Python :: 3.5",
    ],
    zip_safe=False,
)
