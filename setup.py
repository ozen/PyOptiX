import sys
import platform
import os
import fnmatch
from setuptools import setup, Extension, find_packages
from setuptools.command.install import install


def glob_recursive(path, pattern):
    matches = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(dirpath, filename))
    return matches

DEFAULT_CUDA_PATH = '/usr/local/cuda'
DEFAULT_OPTIX_PATH = '/usr/local/optix'

dist_name = platform.linux_distribution()[0]

if dist_name.upper() in ["RHEL", "CENTOS", "FEDORA"]:
    PYTHON_VERSION_SUFFIX = str(sys.version_info.major)
elif dist_name.upper() in ["DEBIAN", "UBUNTU"]:
    PYTHON_VERSION_SUFFIX = "-py%s%s" % (sys.version_info.major, sys.version_info.minor)
else:
    # I don't know
    PYTHON_VERSION_SUFFIX = "-py%s%s" % (sys.version_info.major, sys.version_info.minor)


LIBRARIES = ['optix',
             'optixu',
             'cudart',
             'boost_python%s' % PYTHON_VERSION_SUFFIX]

LIBRARY_DIRS = [os.path.join(DEFAULT_CUDA_PATH, 'lib64'),
                os.path.join(DEFAULT_OPTIX_PATH, 'lib64')]

LIBRARY_INCLUDE = [os.path.join(DEFAULT_CUDA_PATH, 'include'),
                   os.path.join(DEFAULT_OPTIX_PATH, 'include')]

EXTENSION_INCLUDE = [x[0] for x in os.walk('driver')]
EXTENSION_SOURCES = glob_recursive('driver', '*.cpp')


class PyOptiXInstallCommand(install):
    user_options = install.user_options + [
        ('cuda=', None, 'installation directory of CUDA'),
        ('optix=', None, 'installation directory of OptiX'),
    ]

    def initialize_options(self):
        super(PyOptiXInstallCommand, self).initialize_options()
        self.cuda = DEFAULT_CUDA_PATH
        self.optix = DEFAULT_OPTIX_PATH

    def finalize_options(self):
        super(PyOptiXInstallCommand, self).finalize_options()

        if not os.path.isdir(self.cuda):
            raise OSError('CUDA directory does not exist: {0}'.format(self.cuda))

        if not os.path.isdir(self.optix):
            raise OSError('OptiX directory does not exist: {0}'.format(self.optix))

        include_dirs = self.distribution.ext_modules[0].include_dirs
        include_dirs = [item for item in include_dirs if item not in LIBRARY_INCLUDE] + [
            os.path.join(self.cuda, 'include'),
            os.path.join(self.optix, 'include')
        ]
        self.distribution.ext_modules[0].include_dirs = include_dirs

        library_dirs = self.distribution.ext_modules[0].library_dirs
        library_dirs = [item for item in library_dirs if item not in LIBRARY_DIRS] + [
            os.path.join(self.cuda, 'lib64'),
            os.path.join(self.optix, 'lib64')
        ]
        self.distribution.ext_modules[0].library_dirs = library_dirs

setup(
    name='pyoptix',
    version='0.7.1',
    description='Python wrapper for NVIDIA OptiX',
    author='Yigit Ozen',
    author_email='ozen@computer.org',
    license="MIT",
    url='http://github.com/ozen/pyoptix',
    packages=find_packages(),
    cmdclass={
        'install': PyOptiXInstallCommand
    },
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
