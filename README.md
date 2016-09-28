# PyOptiX

PyOptiX lets you access Nvidia's OptiX Ray Tracing Engine from Python.

## Installation

#### Prerequisites

* Install the necessary libraries. For Ubuntu, the install command will look like this:

        sudo apt-get install -y build-essential python-dev python-setuptools python3-dev python3-setuptools libboost-python-dev

* CUDA and OptiX SDK's must be installed before installing PyOptiX.


#### Paths to libraries

The setup script must be able to locate CUDA, OptiX, and Boost.Python library files.
If their paths are different in your system than the defaults, you can pass the paths through command line options.

1. CUDA:
    Default location is `/usr/local/cuda`. You can use symlinks or pass `--cuda-root=<path>` option to setup script.
2. OptiX:
    Default location is `/usr/local/optix`. You can use symlinks or pass `--optix-root=<path>` option to setup script.
3. Boost.Python:
    Searched in LD_LIBRARY_PATH. Default library file name is boost_python-py<version suffix>
    e.g. boost_python-py34 for Python 3.4. You can pass a different directory to find Boost.Python using
    `--boost-lib-dir=<path>` option. You can pass the library file name using `--boost-python-libname=<name>` option.


#### Using pip

    pip install pyoptix
    
Example usage of setup options:

    pip install pyoptix \
    --install-option="--cuda-root=/usr/local/cuda-7.5" \
    --install-option="--optix-root=/opt/NVIDIA-OptiX-SDK-4.0.0-linux64" \
    --install-option="--boost-lib-dir=/usr/lib/weird-path" \
    --install-option="--boost-python-libname=boost_python3"

#### From source

    git clone https://github.com/ozen/PyOptiX.git
    cd pyoptix
    python setup.py install
    
Example usage of setup options:

    python setup.py install \
    --cuda-root=/usr/local/cuda-7.5 \
    --optix-root=/opt/NVIDIA-OptiX-SDK-4.0.0-linux64 \
    --boost-lib-dir=/usr/lib/weird-path \
    --boost-python-libname=boost_python3

#### Root access to create config file

Setup script will ask for root access to create /etc/pyoptix.conf file which consists of nvcc configuration that is
used by PyOptiX compiler while compiling program sources to ptx files during runtime.

If the creation succeeds, PyOptiX compiler will work out of the box.
If it fails, in order to PyOptiX compiler work, nvcc binary path must be in PATH, and required library file paths
including CUDA and OptiX must be in LD_LIBRARY_PATH environment variables.

## API Reference

Will be added soon.
