# PyOptiX

PyOptiX lets you access Nvidia's OptiX Ray Tracing Engine from Python.


## Prerequisites

1. CUDA

    Make sure ```/usr/local/cuda``` points to your CUDA installation, either directly or through symbolic links.

2. OptiX

    Make sure ```/usr/local/optix``` points to your OptiX installation, either directly or through symbolic links.

3. Boost.Python

    Boost.Python must be installed. For Ubuntu, the install command will look like this:

        sudo apt-get install libboost-python-dev
        

## Environment Variables

nvcc binary (CUDA compiler) must be in PATH. OptiX library files must be in LD_LIBRARY_PATH.

    export PATH=/usr/local/cuda/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/lib:/usr/lib/x86_64-linux-gnu:/usr/local/optix/lib64:$LD_LIBRARY_PATH

To make these changes persistent, edit your ```/etc/environment``` file. Here is an example of /etc/environment file:

    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/cuda/bin"
    LD_LIBRARY_PATH="/usr/local/cuda/lib64:/usr/local/lib:/usr/lib/x86_64-linux-gnu:/usr/local/optix/lib64"

Changes in /etc/environment file take effect after re-log.


## Installation

    pip install pyoptix


## Interface

`pyoptix.objects` module mimics OptiX interface. Start by creating an OptiX context:

```python
from pyoptix.objects import OptixContext
context = OptixContext()
```

Then, OptiX objects are created through context

```python
main_group = context.create_group()
```

`pyoptix.highlevel` module extends objects to provide an easier interface. It creates a default context and use it. 

You can provide your own context if you wish. Whenever a call to `pyoptix.highlevel` needs a context, it uses the last set context.

```python
from pyoptix.highlevel import Group
main_group = Group()
```

### Contributors

[Yigit Ozen]  
Mert Kucuk  

[Yigit Ozen]: github.com/ozen
