from distutils.core import setup, Extension

from vizera_setup_tools.includer import get_include_paths_lib_paths_and_lib_names
include_paths, library_paths, libraries = get_include_paths_lib_paths_and_lib_names('Optix', 'BoostNumpy', 'BoostPython')

from vizera_setup_tools.cpp_project import get_include_paths_and_source_files
cpp_project_include_dirs, cpp_project_source_files = get_include_paths_and_source_files('PyOptixCppProject')


include_dirs = include_paths + cpp_project_include_dirs
library_dirs = library_paths

# define the libraries to link with the boost python library
libraries = libraries


PyOptixCpp_module = Extension('PyOptixCpp',
                              define_macros=[('MAJOR_VERSION', '0'),
                                             ('MINOR_VERSION', '1')],
                              include_dirs=include_dirs,
                              libraries=libraries,
                              library_dirs=library_dirs,
                              sources=cpp_project_source_files)

# create the extension and add it to the python distribution
setup(
    name='PyOptix',
    version='0.0.1',
    author='Mert Kucuk',
    author_email='mertkucuk@gmail.com',
    ext_modules=[PyOptixCpp_module]
)
