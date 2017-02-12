# PyOptiX

PyOptiX lets you access Nvidia's OptiX Ray Tracing Engine from Python.

PyOptiX wraps OptiX C++ API using an extension that uses Boost.Python library. Python API is similar to C++ API.
PyOptiX documentation does not include anything about OptiX, so you should already know OptiX and its C++ API.


### Supported Platforms

Only Linux is supported. PyOptiX can work on other platforms but you may need to modify setup.py and set
`Compiler.nvcc_path` and `Compiler.flags` parameters manually during run time.


## Concepts

Since PyOptiX wraps OptiX C++ API, the API is almost the same. PyOptiX adds couple of new concepts.
Let's talk about them.

### Context Stack

PyOptiX implements a Context Stack. `Acceleration`, `Buffer`, `Geometry`, `GeometryGroup`, `GeometryInstance`,
`Group`, `Material`, `Program`, `Selector`, `TextureSampler`, `Transform` objects are always
created in the active `Context` during their instantiation.

A `Context` is created during initialization automatically.
Whenever a new Context object is instantiated, it is pushed to the stack automatically.
`pyoptix.current_context()` method returns the currently active context (which is on top of the stack).
`Context.pop()` instance method pops the context from the stack, so the next context in the stack becomes active.
You can keep the popped context in a variable, then push it to the stack again using `Context.push()` instance method,
making it active. The same Context may occur multiple times in the stack.

### PTX Generation

Programs supplied to the OptiX API must be written in PTX. PyOptiX `Program` objects are instantiated with
a file path and a function name. If the file is a PTX file, PyOptiX does nothing more than calling OptiX functions.
If the file is a source file, `pyoptix.Compiler` class is used to compile the source to PTX,
then the Program object is created.

`pyoptix.Compiler` needs to know some attributes of the system to work correctly. These attributes are collected
during PyOptiX installation and saved to (1) etc/pyoptix.conf/pyoptix.conf file and (2) pyoptix.conf file in the
same directory with Python executable that was used to execute the setup script. If this process somehow fails, you
need to set Compiler flags manually.

`Compiler.nvcc_path` must be a valid path to nvcc binary.
`Compiler.flags` is a list of optional flags passed to nvcc during PTX compilation.
`Compiler.arch` will be the value of -arch flag of nvcc. Read nvcc documentation for more information.
`Compiler.add_program_directory(directory)` method adds the directory to the list of directories in which the file paths
given to Program objects will be searched.
`Compiler.remove_program_directory(directory)` removes the directory from the list it previously added to.

If the source file given to `pyoptix.Compiler` was compiled to PTX before, Compiler checks if the source file or
the files included in `#include "<file>"` format changed; recompiles if it detects a change, uses the old PTX otherwise.

### Program Cache

`Program(file_path, function_name)` always creates a new Program object in OptiX.
PyOptiX also implements a cache for programs.
`Program.get_or_create(file_path, function_name)` static method returns the cached program if the active Context,
file path and function name all match, otherwise creates and returns it.

If `Program.dynamic_programs` class variable is set to True, the source file is recompiled if it was changed, even
if its program was cached, and the program will be recreated using the new PTX.
If `Program.dynamic_programs` is set to False, the cached program is returned without change check.

### Variable Assignments

OptiX program objects communicate with the host program through variables. API objects to which
program variables can be attached are called Scoped objects in PyOptiX. Scoped objects define a dictionary interface
for variable assignment, actual variable declaration and value assignments are handled automatically.

If the value that is being assigned is an API object, the operation is straightforward. For other types of values,
PyOptiX transfers the value to the C++ backend using NumPy arrays. Since NumPy is ubiquitous in Python circles,
PyOptiX doesn't abstract away the usage of NumPy arrays. If the variable is being attached to the program object whose
device code has the variable's declaration, PyOptiX deduces the type of the variable and casts the value
to NumPy array with proper dtype.
If it isn't, PyOptiX cannot deduce the type, therefore the user must cast the value to NumPy array with proper dtype.
The conversion between NumPy arrays and OptiX vector types are as follows:

| Array dtype | Array Shape | OptiX C++ Type |
|---|---|---|
| float32 | (1, ) | float |
| float32 | (2, ) | float2 |
| float32 | (3, ) | float3 |
| float32 | (4, ) | float4 |
| int32 | (1, ) | int |
| int32 | (2, ) | int2 |
| int32 | (3, ) | int3 |
| int32 | (4, ) | int4 |
| uint32 | (1, ) | unsigned_int |
| uint32 | (2, ) | unsigned_int2 |
| uint32 | (3, ) | unsigned_int3 |
| uint32 | (4, ) | unsigned_int4 |
| float32 | (2, 2) | matrix2x2 |
| float32 | (2, 3) | matrix2x3 |
| float32 | (2, 4) | matrix2x4 |
| float32 | (3, 2) | matrix3x2 |
| float32 | (3, 3) | matrix3x3 |
| float32 | (3, 4) | matrix3x4 |
| float32 | (4, 2) | matrix4x2 |
| float32 | (4, 3) | matrix4x3 |
| float32 | (4, 4) | matrix4x4 |


### Buffers using NumPy Arrays

Data is transferred to Buffers using NumPy arrays. Since NumPy is ubiquitous in Python circles,
PyOptiX doesn't abstract away the usage of NumPy arrays.

Buffer objects can be created using `Buffer.from_array(numpy_array, buffer_type_ drop_last_dim)` static method.
A buffer object without copying data can be created using `Buffer.empty(shape, dtype, buffer_type, drop_last_dim)`
static method.
dtype must be a NumPy dtype.
buffer_type is either one of 'i', 'o', or 'io', corresponding to
INPUT, OUTPUT, and INPUT_OUTPUT formats.
drop_last_dim is a boolean that indicates that the array holds or will hold a vector type whose length is the
size of the last dimension of the array. For example, for 2D float4 buffer, the NumPy array's shape will be
(height, width, 4) and dtype is float32. All possible conversions between NumPy arrays and buffers can be found
in the following table.

| Array dtype | Array Shape | drop_last_dim | Buffer Format | Buffer Shape |
|---|---|---|---|---|
| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | float | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 1) | True | float | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 2) | True | float2 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 3) | True | float3 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 4) | True | float4 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| int32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | int | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| int32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 1) | True | int | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| int32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 2) | True | int2 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| int32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 3) | True | int3 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| int32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 4) | True | int4 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | float | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| uint32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | unsigned_int | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| uint32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 1) | True | unsigned_int | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| uint32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 2) | True | unsigned_int2 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| uint32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 3) | True | unsigned_int3 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| uint32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 4) | True | unsigned_int4 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | float | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| int16 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | short | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| int16 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 1) | True | short | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| int16 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 2) | True | short2 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| int16 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 3) | True | short3 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| int16 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 4) | True | short4 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | float | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| uint16 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | unsigned_short | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| uint16 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 1) | True | unsigned_short | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| uint16 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 2) | True | unsigned_short2 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| uint16 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 3) | True | unsigned_short3 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| uint16 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 4) | True | unsigned_short4 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | float | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| int8 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | byte | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| int8 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 1) | True | byte | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| int8 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 2) | True | byte2 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| int8 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 3) | True | byte3 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| int8 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 4) | True | byte4 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | float | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| uint8 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | unsigned_byte | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| uint8 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 1) | True | unsigned_byte | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| uint8 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 2) | True | unsigned_byte2 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| uint8 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 3) | True | unsigned_byte3 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)
| uint8 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, 4) | True | unsigned_byte4 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)| float32 | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>) | False | float | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n</sub>)
| custom | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>, x) | True | user | (d<sub>0</sub>, d<sub>1</sub>, ..., d<sub>n-1</sub>)


The content of Buffer object can be converted to/from Numpy array using `Buffer.copy_from_array(numpy_array)` and
`Buffer.to_array()` instance methods.

### Variables or Buffers of Structs

If you have a variable or buffer of C structs in device code, you can still use NumPy arrays in Python host code.
Canonical way to do it is to define a Python class corresponding to the C struct. In the class, define a custom
`dtype` and `__array__` method. The dtype must match with the memory layout of the C struct.
The `__array__` method must create a NumPy array with the custom dtype, fill the values according to the contents
of the class instance, and return the array. NumPy will use `__array__` method to cast an object to NumPy array.
When assigning the object to the variable, wrap it with numpy.array function.
When creating a Buffer from an array of objects, make it a NumPy array and
set drop_last_dim to True since the objects themselves will be NumPy arrays with custom dtypes.

### Entry Points

`EntryPoint` class encapsulates entry point concept in OptiX. `EntryPoint` objects are created by passing a ray
generation program and an optional exception program; and they can be launched later with given sizes. You don't need
to set entry point counts or keep track of them to launch them. Just keep EntryPoints in variables and launch them
using `EntryPoint.launch()` instance method.


## Installation

#### Prerequisites

* Install the necessary libraries: Python dev package, Boost.Python, setuptools.
For Ubuntu, the install command will look like this:

        sudo apt-get install -y build-essential python-dev python-setuptools python3-dev python3-setuptools libboost-python-dev

* `CUDA` and `OptiX` SDK's must be installed before installing PyOptiX.
* `nvcc` must be in `PATH`.
* `CUDA`, `OptiX`, and `Boost.Python` library paths must be in either `ldconfig` or `LD_LIBRARY_PATH`.


#### Using pip

    pip install pyoptix


#### From source

    git clone https://github.com/ozen/PyOptiX.git
    cd pyoptix
    python setup.py install


#### pyoptix.conf file

pyoptix.conf file is explained in Concepts > PTX Generation section. pyoptix.Compiler cannot work out of the box
if pyoptix.conf file creation fails during installation.

Please note that pip creates wheel distribution of the package and caches it during installation.
Subsequent pip install commands for the same version of the package will use the cached wheel,
therefore setup.py script won't be executed and pyoptix.conf file won't be created.
When you want to prevent this you can use --no-binary flag:

    pip install pyoptix --no-binary pyoptix


## API Reference

Work In Progress


## Using the Docker Image

1. Copy OptiX SDK files into ./optix directory. This is needed to build a docker image with OptiX. Example command:

        cp -R /usr/local/NVIDIA-OptiX-SDK-4.0.2-linux64/ PyOptiX/optix/

2. Build a docker image using the Dockerfile provided in the source directory:

        cd PyOptiX
        docker build -t pyoptix .

3. Run an example in a docker container using the image. Use [nvidia-docker] to be able to use the GPU in the container.
Following command will also make the container able to access host machine's X11 server, so you will be able to see the result window.

        nvidia-docker run -it --rm \
            --volume="/home/$USER:/home/$USER" \
            --volume=/etc/group:/etc/group:ro \
            --volume=/etc/passwd:/etc/passwd:ro \
            --volume=/etc/shadow:/etc/shadow:ro \
            --volume=/etc/sudoers:/etc/sudoers:ro \
            --volume=/etc/sudoers.d:/etc/sudoers.d:ro \
            --volume=/tmp/.X11-unix:/tmp/.X11-unix:rw \
            --user=$(id -u) \
            --env="DISPLAY" \
            --workdir="/home/$USER" \
            pyoptix python3 /usr/src/PyOptiX/examples/hello/hello.py


[nvidia-docker]: https://github.com/NVIDIA/nvidia-docker
