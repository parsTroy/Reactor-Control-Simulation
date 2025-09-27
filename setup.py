# Reactor Control Simulation - Python Package Setup
# This file allows us to install our project as a Python package

from setuptools import setup, find_packages
import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext

# Define the C++ extension module
ext_modules = [
    Pybind11Extension(
        "reactor_sim",
        ["python_bindings/bindings.cpp"],
        include_dirs=["cpp_core"],
        language="c++",
        cxx_std=17,
    ),
]

setup(
    name="reactor-control-sim",
    version="1.0.0",
    description="Nuclear Reactor Control Simulation",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: C++",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
