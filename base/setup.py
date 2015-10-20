import os
from setuptools import setup, find_packages

dirname = os.path.dirname(os.path.abspath(__file__))

setup(
    name="Yatu",
    version="0.1",
    install_requires=open("%s/requirements.txt" % dirname).read().split("\n"),
    data_files=[],
    packages=find_packages(),
)
