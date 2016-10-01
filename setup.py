import sys
import os
import fnmatch
from subprocess import check_call, check_output
from tempfile import NamedTemporaryFile
from setuptools import setup, Extension, find_packages

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

BOOST_PYTHON_LIBNAMES = [
    "libboost_python-py%s%s.so" % (sys.version_info.major, sys.version_info.minor),
    "libboost_python%s.so" % sys.version_info.major,
]

ld_paths = None


def populate_ld_paths():
    global ld_paths
    ld_paths = []
    for line in check_output(['sudo', 'ldconfig', '-v']).decode('utf8').splitlines():
        if line.startswith('/'):
            ld_paths.append(line[:line.find(':')])
    ld_paths.extend(os.environ["LD_LIBRARY_PATH"].split(os.pathsep))


def glob_recursive(path, pattern):
    matches = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(dirpath, filename))
    return matches


def search_library(filenames):
    if not isinstance(filenames, list):
        filenames = [filenames]

    if ld_paths is None:
        populate_ld_paths()

    for path in ld_paths:
        for filename in filenames:
            print(os.path.join(path, filename))
            if os.path.exists(os.path.join(path, filename)):
                return os.path.abspath(os.path.join(path, filename))


def search_on_path(filenames):
    if not isinstance(filenames, list):
        filenames = [filenames]

    for path in os.environ["PATH"].split(os.pathsep):
        for filename in filenames:
            if os.path.exists(os.path.join(path, filename)):
                return os.path.abspath(os.path.join(path, filename))


def main():
    lib64 = os.path.join('lib', 'x64') if sys.platform.startswith('win') else 'lib64'

    nvcc_path = search_on_path(['nvcc', 'nvcc.exe'])
    if nvcc_path is None:
        raise OSError('nvcc is not in PATH')

    cuda_root = os.path.dirname(os.path.dirname(nvcc_path))
    cuda_include = os.path.join(cuda_root, 'include')
    cuda_libs = [
        os.path.join(cuda_root, 'lib'),
        os.path.join(cuda_root, lib64),
        os.path.join(cuda_root, 'bin'),
    ]

    if sys.platform.startswith('win'):
        optix_lib_path = search_on_path('optix.1.dll')
    else:
        optix_lib_path = search_library('liboptix.so')

    if optix_lib_path is None:
        raise OSError('OptiX Library not found. '
                      'Add its path to ldconfig or LD_LIBRARY_PATH on Linux and to PATH on Windows.')

    optix_root = os.path.dirname(os.path.dirname(optix_lib_path))
    optix_include = os.path.join(optix_root, 'include')
    optix_libs = [
        os.path.join(optix_root, 'lib'),
        os.path.join(optix_root, lib64),
        os.path.join(optix_root, 'bin'),
    ]

    if sys.platform.startswith('win'):
        boost_python_lib_file = search_on_path('boost_python.dll')
    else:
        boost_python_lib_file = search_library(BOOST_PYTHON_LIBNAMES)

    if boost_python_lib_file is None:
        raise OSError('Boost.Python library not found. '
                      'Add its path to ldconfig or LD_LIBRARY_PATH on Linux and to PATH on Windows.')

    boost_python_lib_dir, boost_python_lib_name = os.path.split(boost_python_lib_file)

    sources = glob_recursive('driver', '*.cpp')
    include_dirs = [x[0] for x in os.walk('driver')] + [cuda_include, optix_include]
    library_dirs = cuda_libs + optix_libs + [boost_python_lib_dir]
    libraries = ['optix', 'optixu', 'cudart', boost_python_lib_name]

    try:
        config = ConfigParser()
        config.add_section('pyoptix')
        nvcc_command = '{0} -I{1} -I{2} -loptix -loptixu -lcudart {3}'.format(
            nvcc_path, cuda_include, optix_include, ' '.join(['-L' + lib for lib in cuda_libs + optix_libs]))
        config.set('pyoptix', 'nvcc_command', nvcc_command)
        config.set('pyoptix', 'include_dirs', os.pathsep.join(include_dirs))
        config.set('pyoptix', 'library_dirs', os.pathsep.join(library_dirs))
        config.set('pyoptix', 'libraries', os.pathsep.join(libraries))
        tmp = NamedTemporaryFile(mode='w+', delete=False)
        config.write(tmp)
        tmp.close()
        check_call(['sudo', 'cp', tmp.name, '/etc/pyoptix.conf'])
        check_call(['sudo', 'chmod', '444', '/etc/pyoptix.conf'])
    except Exception as e:
        print("nvcc configuration could not be saved. When you use PyOptiX Compiler, "
              "nvcc path must be in PATH and OptiX library paths must be in LD_LIBRARY_PATH")

    setup(
        name='pyoptix',
        version='1.0.0a1',
        description='Python wrapper for NVIDIA OptiX',
        author='Yigit Ozen',
        author_email='ozen@computer.org',
        license="MIT",
        url='http://github.com/ozen/pyoptix',
        packages=find_packages(),
        ext_modules=[Extension(name='pyoptix._driver', sources=sources, include_dirs=include_dirs,
                               library_dirs=library_dirs, runtime_library_dirs=library_dirs, libraries=libraries,
                               language='c++')],
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

if __name__ == '__main__':
    main()