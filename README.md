# PyOptiX

PyOptiX lets you access Nvidia's OptiX Ray Tracing Engine from Python.

## Installation

1. Download and Install CUDA

    Make sure ```/usr/local/cuda``` points to your CUDA installation, either directly or using symbolic links.

2. Download and Install OptiX

    Make sure ```/usr/local/optix``` points to your OptiX installation, either directly or using symbolic links.

3. Install NumPy to your system

        sudo apt-get install python3-pip
        sudo pip3 install numpy

4. Install Boost.Python

    You can use apt. The package name should be something like:

        sudo apt-get install libboost-python1.55-dev

5. Build and Install Boost.NumPy

    You need to download and build Boost.NumPy yourself.
    Check https://bitbucket.org/imcom/boost.numpy where you can find README file explaining the build process.


## Before Using PyOptiX

nvcc binary (CUDA compiler) must be in PATH. OptiX library files must be in LD_LIBRARY_PATH.

    export PATH=/usr/local/cuda/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/lib:/usr/lib/x86_64-linux-gnu:/usr/local/optix/lib64:$LD_LIBRARY_PATH

To make these changes persistent, edit your ```/etc/environment``` file. Here is an example of /etc/environment file:

    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/cuda/bin"
    LD_LIBRARY_PATH="/usr/local/cuda/lib64:/usr/local/lib:/usr/lib/x86_64-linux-gnu:/usr/local/optix/lib64"

Changes in /etc/environment file take effect when the system is rebooted.
