# PyOptiX

PyOptiX lets you access Nvidia's OptiX Ray Tracing Engine from Python.

## Installation

#### Prerequisites

* Install the necessary libraries: Python dev package, Boost.Python, setuptools.
For Ubuntu, the install command will look like this:

        sudo apt-get install -y build-essential python-dev python-setuptools python3-dev python3-setuptools libboost-python-dev

* CUDA and OptiX SDK's must be installed before installing PyOptiX.
* `nvcc` must be in PATH.
* CUDA, OptiX, and Boost.Python library paths must be in either ldconfig or `LD_LIBRARY_PATH` on Linux and `PATH` on Windows.


#### Using pip

    pip install pyoptix

#### From source

    git clone https://github.com/ozen/PyOptiX.git
    cd pyoptix
    python setup.py install

#### Root access to create config file

Setup script will ask for root access to create /etc/pyoptix.conf file which consists of nvcc configuration that is
used by PyOptiX compiler while compiling program sources to ptx files during runtime.

If the creation succeeds, PyOptiX compiler will work out of the box.
If it fails, in order to PyOptiX compiler work, nvcc binary path must be in PATH, and required library file paths
including CUDA and OptiX must be in LD_LIBRARY_PATH environment variables.

## API Reference

Will be added soon.
