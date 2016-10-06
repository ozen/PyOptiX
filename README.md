# PyOptiX

PyOptiX lets you access Nvidia's OptiX Ray Tracing Engine from Python.

## What's Inside

PyOptiX wraps OptiX C++ API using an extension that uses Boost.Python library. Python API is similar to C++ API.
PyOptiX documentation does not include anything about OptiX, so you should already know OptiX and its C++ API.

PyOptiX implements a `Context` stack. `Acceleration`, `Buffer`, `Geometry`, `GeometryGroup`, `GeometryInstance`,
`Group`, `Material`, `Program`, `Selector`, `TextureSampler`, `Transform` objects are always
created in the active `Context`.

Scoped Objects have dict interfaces in Python. Variable Objects are automatically handled when you assign a variable to
a Scoped Object. Python to C transfer of variables are done through numpy. PyOptiX automatically handles this if either
it can query the variable in OptiX or the variable is an PyOptiX Object. If it can't, you need to pass variables
using numpy arrays.

`EntryPoint` class encapsulates entry point concept in OptiX. `EntryPoint` objects are created by passing a ray
generation program and an optional exception program; and they can be launched later with given sizes.

`Compiler` class compiles program source files to ptx files. If you pass a source file when creating a `Program` object,
`Compiler` is automatically used to compile the source.

## Installation

#### Prerequisites

* Install the necessary libraries: Python dev package, Boost.Python, setuptools.
For Ubuntu, the install command will look like this:

        sudo apt-get install -y build-essential python-dev python-setuptools python3-dev python3-setuptools libboost-python-dev

* CUDA and OptiX SDK's must be installed before installing PyOptiX.
* `nvcc` must be in PATH.
* CUDA, OptiX, and Boost.Python library paths must be in either ldconfig or `LD_LIBRARY_PATH`.


#### Using pip

    pip install pyoptix

#### From source

    git clone https://github.com/ozen/PyOptiX.git
    cd pyoptix
    python setup.py install

#### pyoptix.conf file

Setup script creates `pyoptix.conf` file next to the python binary that is used by setup script. `pyoptix.Compiler`
class uses `pyoptix.conf` to determine `nvcc` path and flags when compiling sources to ptx files in run time.
If `pyoptix.conf` creation somehow fails, you need to set `Compiler.nvcc_path` and `Compiler.flags` attributes manually
during run time before compiling any programs.

## API Reference

### pyoptix.current_context()

Returns currently active (at the top of the stack) `Context` object.

### pyoptix.Context

### pyoptix.Compiler

### pyoptix.Acceleration

### pyoptix.Geometry

### pyoptix.GeometryGroup

### pyoptix.GeometryInstance

### pyoptix.Group

### pyoptix.Material

### pyoptix.Selector

### pyoptix.Transform

### pyoptix.Buffer

### pyoptix.TextureSampler

### pyoptix.Program

### pyoptix.EntryPoint

### pyoptix.enums

#### pyoptix.enums.Format