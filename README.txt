# PyOptiX

PyOptiX lets you access Nvidia's OptiX Ray Tracing Engine from Python.

## Prerequisites

* CUDA (on /usr/local/cuda [1])
* OptiX (on /usr/local/optix [1])
* numpy
* Boost.Python
* Boost.NumPy

[1] Symbolic links can be used.


## Running

nvcc binary (CUDA compiler) must be in PATH. Use the following command to add its path:

'''
    export PATH=$PATH:/usr/local/cuda/bin
'''

OptiX library files must be in LD_LIBRARY_PATH. Use the following command (or a variation for your setup) to add its path:

'''
    export LD_LIBRARY_PATH=/usr/local/optix/lib64:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
'''