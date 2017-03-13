#!/usr/bin/env python

from setuptools import setup

setup(
    name="iotcommute",
    version="0.1.0",
    description="The official Python client for IOT COMMUNICATE webscoket connection",
    author="Aniket patel",
    author_email="patelaniket165@gmail.com",
    url="",
    packages=["iotcommute"],
    download_url="https://github.com/kodani/iotcommute",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: IOT developers and automation",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: iot device :: device communication ::iot messaging tool",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries"
    ],
    install_requires=["requests", "websocket-client"]
)
