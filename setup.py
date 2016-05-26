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

CUDA_PATH = '/usr/local/cuda'
OPTIX_PATH = '/usr/local/optix'

PYTHON_VERSION_SUFFIX = "-py%s%s" % (sys.version_info.major, sys.version_info.minor)    # Ubuntu
# PYTHON_VERSION_SUFFIX = str(sys.version_info.major)   # Fedora

LIBRARIES = ['optix',
             'optixu',
             'cudart',
             'boost_python%s' % PYTHON_VERSION_SUFFIX]

LIBRARY_DIRS = [os.path.join(CUDA_PATH, 'lib64'),
                os.path.join(OPTIX_PATH, 'lib64')]

LIBRARY_INCLUDE = [os.path.join(CUDA_PATH, 'include'),
                   os.path.join(OPTIX_PATH, 'include')]

EXTENSION_INCLUDE = [x[0] for x in os.walk('driver')]
EXTENSION_SOURCES = glob_recursive('driver', '*.cpp')

setup(
    name='pyoptix',
    version='0.7.0a2',
    description='Python wrapper for NVIDIA OptiX',
    author='Yigit Ozen',
    author_email='ozen@computer.org',
    url='http://github.com/ozen/pyoptix',
    packages=find_packages(),
    ext_modules=[Extension(name='pyoptix._driver',
                           sources=EXTENSION_SOURCES,
                           include_dirs=LIBRARY_INCLUDE + EXTENSION_INCLUDE,
                           library_dirs=LIBRARY_DIRS,
                           libraries=LIBRARIES)],
    install_requires=['six', 'numpy'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
