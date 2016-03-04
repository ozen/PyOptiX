import sys
import os
import fnmatch
from setuptools import setup, Extension, find_packages


def glob_recursive(path, pattern):
    matches = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(dirpath, filename))
    return matches


PYTHON_VERSION_SUFFIX = "-py%s%s" % (sys.version_info.major, sys.version_info.minor)
LIBRARIES = ['optix', 'optixu', 'cudart', 'boost_numpy%s' % PYTHON_VERSION_SUFFIX,
             'boost_python%s' % PYTHON_VERSION_SUFFIX]
LIBRARY_DIRS = ['/usr/local/optix/lib64', '/usr/local/cuda/lib64', '/usr/lib']
LIBRARY_INCLUDE = ['/usr/local/optix/include', '/usr/local/cuda/include', '/usr/local/include', '/usr/include']
EXTENSION_INCLUDE = [x[0] for x in os.walk('driver')]
EXTENSION_SOURCES = glob_recursive('driver', '*.cpp')

setup(
    name='pyoptix',
    version='0.3.0',
    packages=find_packages(),
    ext_modules=[Extension('pyoptix._driver', EXTENSION_SOURCES,
                           include_dirs=LIBRARY_INCLUDE + EXTENSION_INCLUDE,
                           library_dirs=LIBRARY_DIRS,
                           libraries=LIBRARIES)],
    install_requires=['numpy'],
)
