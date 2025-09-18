#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

from threefive.version import version


setuptools.setup(
    name="threefive",
    version=version,
    author="Adrian ",
    author_email="spam@iodisco.com",
    description="threefive is The #1 SCTE-35 Decoder and Encoder on the Planet",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/superkabuki/threefive",
    install_requires=[
        "pyaes",
    ],
    scripts=["bin/threefive","bin/threefive3",],
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: Sleepycat License",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: BSD :: OpenBSD",
        "Operating System :: POSIX :: BSD :: NetBSD",
        "Operating System :: POSIX :: Linux",
        "Topic :: Multimedia :: Video",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.8",
)
