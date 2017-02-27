import sys
import os
import fnmatch
from subprocess import check_call, check_output, CalledProcessError
from tempfile import NamedTemporaryFile
from setuptools import setup, Extension

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

BOOST_PYTHON_LIBNAMES = [
    'boost_python-py%s%s' % (sys.version_info.major, sys.version_info.minor),
    'boost_python%s' % sys.version_info.major,
]

BOOST_PYTHON_FILENAMES = {'lib%s.so' % libname: libname for libname in BOOST_PYTHON_LIBNAMES}

ld_paths = None


def check_call_sudo_if_fails(cmd):
    try:
        return check_call(cmd)
    except CalledProcessError as e:
        return check_call(['sudo'] + cmd)


def check_output_sudo_if_fails(cmd):
    try:
        return check_output(cmd)
    except CalledProcessError as e:
        return check_output(['sudo'] + cmd)


def populate_ld_paths():
    global ld_paths
    ld_paths = []
    for line in check_output_sudo_if_fails(['ldconfig', '-vNX']).decode('utf8').splitlines():
        if line.startswith('/'):
            ld_paths.append(line[:line.find(':')])
    if "LD_LIBRARY_PATH" in os.environ:
        ld_paths.extend(os.environ["LD_LIBRARY_PATH"].split(os.pathsep))


def glob_recursive(path, pattern):
    matches = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(dirpath, filename))
    return matches


def search_library(filenames):
    filenames = list(filenames)

    if ld_paths is None:
        populate_ld_paths()

    for path in ld_paths:
        for filename in filenames:
            print(os.path.join(path, filename))
            if os.path.exists(os.path.join(path, filename)):
                return os.path.abspath(os.path.join(path, filename))


def search_on_path(filenames):
    filenames = list(filenames)

    for path in os.environ["PATH"].split(os.pathsep):
        for filename in filenames:
            if os.path.exists(os.path.join(path, filename)):
                return os.path.abspath(os.path.join(path, filename))


def save_pyoptix_conf(nvcc_path, compile_args, include_dirs, library_dirs, libraries):
    try:
        config = ConfigParser()
        config.add_section('pyoptix')

        config.set('pyoptix', 'nvcc_path', nvcc_path)
        config.set('pyoptix', 'compile_args', os.pathsep.join(compile_args))
        config.set('pyoptix', 'include_dirs', os.pathsep.join(include_dirs))
        config.set('pyoptix', 'library_dirs', os.pathsep.join(library_dirs))
        config.set('pyoptix', 'libraries', os.pathsep.join(libraries))

        tmp = NamedTemporaryFile(mode='w+', delete=False)
        config.write(tmp)
        tmp.close()
        config_path = os.path.join(os.path.dirname(sys.executable), 'pyoptix.conf')
        check_call_sudo_if_fails(['cp', tmp.name, config_path])
        check_call_sudo_if_fails(['cp', tmp.name, '/etc/pyoptix.conf'])
        check_call_sudo_if_fails(['chmod', '644', config_path])
        check_call_sudo_if_fails(['chmod', '644', '/etc/pyoptix.conf'])
    except Exception as e:
        print("PyOptiX configuration could not be saved. When you use pyoptix.Compiler, "
              "nvcc path must be in PATH, OptiX library paths must be in LD_LIBRARY_PATH, and pyoptix.Compiler "
              "attributes should be set manually.")


def extension_prebuild():
    nvcc_path = search_on_path(['nvcc', 'nvcc.exe'])
    if nvcc_path is None:
        raise OSError('nvcc is not in PATH')

    cuda_root = os.path.dirname(os.path.dirname(nvcc_path))
    cuda_include = os.path.join(cuda_root, 'include')
    cuda_lib_dirs = [
        os.path.join(cuda_root, 'lib64'),
        os.path.join(cuda_root, 'bin'),
    ]

    optix_lib_path = search_library(['liboptix.so'])

    if optix_lib_path is None:
        raise OSError('OptiX Library not found. Add its path to ldconfig or LD_LIBRARY_PATH.')

    optix_root = os.path.dirname(os.path.dirname(optix_lib_path))
    optix_include = os.path.join(optix_root, 'include')
    optix_lib_dirs = [
        os.path.join(optix_root, 'lib64'),
        os.path.join(optix_root, 'bin'),
    ]

    boost_python_lib_file = search_library(BOOST_PYTHON_FILENAMES)

    if boost_python_lib_file is None:
        raise OSError('Boost.Python library not found. Add its path to ldconfig or LD_LIBRARY_PATH.')

    boost_python_lib_dir, boost_python_lib_name = os.path.split(boost_python_lib_file)

    sources = glob_recursive('driver', '*.cpp')
    include_dirs = [x[0] for x in os.walk('driver')] + [cuda_include, optix_include]
    library_dirs = cuda_lib_dirs + optix_lib_dirs + [boost_python_lib_dir]
    libraries = ['optix', 'optixu', 'cudart', BOOST_PYTHON_FILENAMES[boost_python_lib_name]]

    compile_args = [
        '-I%s' % cuda_include, '-I%s' % optix_include, '-I%s' % optix_include, '-loptix', '-loptixu',
        '-lcudart',
    ] + ['-L%s' % lib for lib in cuda_lib_dirs + optix_lib_dirs]

    save_pyoptix_conf(nvcc_path, compile_args, include_dirs, library_dirs, libraries)

    return sources, include_dirs, library_dirs, libraries


def main():
    building_extension = False

    for arg in sys.argv:
        if arg in ['build', 'build_ext', 'install', 'install_lib']:
            building_extension = True

    if building_extension:
        sources, include_dirs, library_dirs, libraries = extension_prebuild()
    else:
        sources = include_dirs = library_dirs = libraries = []

    setup(
        name='pyoptix',
        version='0.10.1',
        description='Python wrapper for NVIDIA OptiX',
        author='Yigit Ozen',
        author_email='ozen@computer.org',
        license="MIT",
        url='http://github.com/ozen/pyoptix',
        packages=['pyoptix', 'pyoptix.mixins'],
        ext_modules=[Extension(name='pyoptix._driver', sources=sources, include_dirs=include_dirs,
                               library_dirs=library_dirs, runtime_library_dirs=library_dirs, libraries=libraries,
                               language='c++', extra_compile_args=['-std=c++11'])],
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
            'Programming Language :: Python :: 3.6',
        ],
    )


if __name__ == '__main__':
    main()
