# PyOptiX

PyOptiX lets you access Nvidia's OptiX Ray Tracing Engine from Python.

## Important Note

We have made our best efforts to make setup.py compatible with most Linux distributions, but you may need to pull the source 
and modify it if it doesn't work for you, for example by not being able to determine Boost.Python library file name correctly.


## Prerequisites

1. CUDA

    Default directory is `/usr/local/cuda`. If it's different in your system, 
    either use symlinks or pass `--cuda=<path>` option to setup.

2. OptiX

    Default directory is `/usr/local/optix`. If it's different in your system, 
    either use symlinks or pass `--optix=<path>` option to setup.

3. Boost.Python

    Boost.Python must be installed. For Ubuntu, the install command will look like this:

        sudo apt-get install libboost-python-dev
        

## Environment Variables

nvcc binary (CUDA compiler) must be in `PATH`. CUDA and OptiX library files must be in `LD_LIBRARY_PATH`.

    export PATH=/usr/local/cuda/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/optix/lib64:$LD_LIBRARY_PATH

To make these changes persistent, edit your `/etc/environment` file. 
Changes in /etc/environment file take effect after re-log. Here is an example of /etc/environment file:

    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/cuda/bin"
    LD_LIBRARY_PATH="/usr/local/cuda/lib64:/usr/local/lib:/usr/lib/x86_64-linux-gnu:/usr/local/optix/lib64"


## Installation

#### Using pip

    pip install pyoptix
    
Use the following format to override default CUDA and OptiX paths:

    pip install pyoptix --install-option="--cuda=/usr/local/cuda-7.5" --install-option="--optix=/opt/NVIDIA-OptiX-SDK-4.0.0-linux64"

#### From Source

    git clone https://github.com/ozen/PyOptiX.git
    cd pyoptix
    python setup.py install
    
Use the following format to override default CUDA and OptiX paths:

    python setup.py install --cuda=/usr/local/cuda-7.5 --optix=/opt/NVIDIA-OptiX-SDK-4.0.0-linux64

## API Reference

Will be added soon.