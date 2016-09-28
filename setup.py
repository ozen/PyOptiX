import sys
import os
import fnmatch
from subprocess import check_call
from tempfile import NamedTemporaryFile
from setuptools import setup, Extension, find_packages, Command
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

# Modify variables below according to your system.
CUDA_ROOT = '/usr/local/cuda'
OPTIX_ROOT = '/usr/local/optix'
BOOST_LIB_DIR = None
BOOST_PYTHON_LIBNAME = "boost_python-py%s%s" % (sys.version_info.major, sys.version_info.minor)


def glob_recursive(path, pattern):
    matches = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(dirpath, filename))
    return matches


class PyOptiXCommand(Command):
    user_options = [
        ('cuda-root=', None, 'installation directory of CUDA'),
        ('optix-root=', None, 'installation directory of OptiX'),
        ('boost-lib-dir=', None, 'directory that Boost library resides'),
        ('boost-python-libname=', None, 'name of the Boost.Python library file, e.g. boost_python-py32'),
    ]

    def initialize_options(self):
        self.cuda_root = CUDA_ROOT
        self.optix_root = OPTIX_ROOT
        self.boost_lib_dir = BOOST_LIB_DIR
        self.boost_python_libname = BOOST_PYTHON_LIBNAME

    def finalize_options(self):
        if not os.path.isdir(self.cuda_root):
            raise OSError('CUDA directory does not exist: {0}. \n'
                          'Provide a valid directory with cuda-root=<path> option.'.format(self.cuda_root))

        if not os.path.isdir(self.optix_root):
            raise OSError('OptiX directory does not exist: {0} \n'
                          'Provide a valid directory with optix-root=<path> option.'.format(self.optix_root))

        if self.boost_lib_dir is not None and not os.path.isdir(self.boost_lib_dir):
            raise OSError('Boost Library directory does not exist: {0}'.format(self.boost_lib_dir))

        cuda_include = os.path.join(self.cuda_root, 'include')
        optix_include = os.path.join(self.optix_root, 'include')
        cuda_lib = os.path.join(self.cuda_root, 'lib64')
        optix_lib = os.path.join(self.optix_root, 'lib64')

        self.distribution.ext_modules[0].include_dirs.extend([cuda_include, optix_include])
        self.distribution.ext_modules[0].library_dirs.extend([cuda_lib, optix_lib])
        self.distribution.ext_modules[0].runtime_library_dirs.extend([cuda_lib, optix_lib])
        self.distribution.ext_modules[0].libraries.append(self.boost_python_libname)

        if self.boost_lib_dir is not None:
            self.distribution.ext_modules[0].library_dirs.append(self.boost_lib_dir)
            self.distribution.ext_modules[0].runtime_library_dirs.append(self.boost_lib_dir)

    def run(self):
        nvcc_path = os.path.join(self.cuda_root, 'bin', 'nvcc')
        cuda_include = os.path.join(self.cuda_root, 'include')
        optix_include = os.path.join(self.optix_root, 'include')
        cuda_lib = os.path.join(self.cuda_root, 'lib64')
        optix_lib = os.path.join(self.optix_root, 'lib64')

        try:
            config = ConfigParser()
            config.add_section('pyoptix')
            nvcc_command = "{0} -I{1} -I{2} -L{3} -L{4} -loptix -loptixu -lcudart".format(
                nvcc_path, cuda_include, optix_include, cuda_lib, optix_lib)
            config.set('pyoptix', 'nvcc_command', nvcc_command)

            tmp = NamedTemporaryFile(mode='w+', delete=False)
            config.write(tmp)
            tmp.close()
            check_call(['sudo', 'cp', tmp.name, '/etc/pyoptix.conf'])
            check_call(['sudo', 'chmod', '444', '/etc/pyoptix.conf'])
        except Exception as e:
            print("nvcc configuration could not be saved. When you use PyOptiX Compiler, "
                  "nvcc path must be in PATH and OptiX library paths must be in LD_LIBRARY_PATH")


class PyOptiXInstallCommand(install, PyOptiXCommand):
    user_options = install.user_options + PyOptiXCommand.user_options

    def initialize_options(self):
        install.initialize_options(self)
        PyOptiXCommand.initialize_options(self)

    def finalize_options(self):
        install.finalize_options(self)
        PyOptiXCommand.finalize_options(self)

    def run(self):
        install.run(self)
        PyOptiXCommand.run(self)


class PyOptiXBuildExtCommand(build_ext, PyOptiXCommand):
    user_options = build_ext.user_options + PyOptiXCommand.user_options

    def initialize_options(self):
        build_ext.initialize_options(self)
        PyOptiXCommand.initialize_options(self)

    def finalize_options(self):
        build_ext.finalize_options(self)
        PyOptiXCommand.finalize_options(self)


setup(
    name='pyoptix',
    version='1.0.0a1',
    description='Python wrapper for NVIDIA OptiX',
    author='Yigit Ozen',
    author_email='ozen@computer.org',
    license="MIT",
    url='http://github.com/ozen/pyoptix',
    packages=find_packages(),
    cmdclass={
        'install': PyOptiXInstallCommand,
        'build_ext': PyOptiXBuildExtCommand,
    },
    ext_modules=[Extension(name='pyoptix._driver',
                           sources=glob_recursive('driver', '*.cpp'),
                           include_dirs=[x[0] for x in os.walk('driver')],
                           libraries=['optix', 'optixu', 'cudart'])],
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
