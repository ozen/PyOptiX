# PyOptiX

PyOptiX lets you access Nvidia's OptiX Ray Tracing Engine from Python.

## Prerequisites

* CUDA (on /usr/local/cuda [1])
* OptiX (on /usr/local/optix [1])
* numpy
* Boost.Python
* Boost.NumPy

[1] Symbolic links can be used if you have installed it to somewhere else.


### Before Running

nvcc binary (CUDA compiler) must be in PATH. Use the following command to add it:

```
export PATH=/usr/local/cuda/bin:$PATH
```

OptiX library files must be in LD_LIBRARY_PATH. Use the following command (or a variation for your setup) to add it:

```
export LD_LIBRARY_PATH=/usr/local/lib:/usr/lib/x86_64-linux-gnu:/usr/local/optix/lib64:$LD_LIBRARY_PATH
```