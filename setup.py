# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="matdata2py",
    version="0.1.0",
    description="library to import Matlab data to python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sammousavi/MatData2Py",
    author="Sam Mousavi",
    author_email="s.mo.mousavi@gmail.com",
    license="GNU",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["matdata2py"],
    include_package_data=True,
    install_requires=["numpy","h5py"]
    
    )