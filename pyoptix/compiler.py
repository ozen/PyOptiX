import logging
import re
import os
import sys
import shlex
import fnmatch
from stat import S_IRUSR, S_IWUSR, S_IRGRP, S_IWGRP, S_IROTH, S_IWOTH, S_IXUSR, S_IXGRP, S_IXOTH
from subprocess import check_call, CalledProcessError
from pyoptix.utils import glob_recursive, find_sub_path

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

logger = logging.getLogger(__name__)


class Compiler:
    nvcc_path = 'nvcc'
    extra_compile_args = []
    output_path = '/tmp/pyoptix/ptx'
    use_fast_math = True
    _compile_args = []
    _program_directories = []

    @classmethod
    def add_program_directory(cls, directory):
        if directory not in cls._program_directories:
            cls._program_directories.append(directory)

    @classmethod
    def remove_program_directory(cls, directory):
        if directory in cls._program_directories:
            cls._program_directories.remove(directory)

    @classmethod
    def is_compile_required(cls, source_path, ptx_path):
        if os.path.isfile(ptx_path):
            ptx_mtime = os.path.getmtime(ptx_path)
            source_mtime = os.path.getmtime(source_path)

            if source_mtime > ptx_mtime:
                return True
            elif cls._has_modified_includes(source_path, ptx_mtime):
                return True
            else:
                return False

        else:
            return True

    @classmethod
    def _has_modified_includes(cls, file_path, modified_after, depth=4):
        if depth == 0:
            return False

        include_pattern = '#include\s*"(.*)"'

        with open(file_path) as f:
            content = f.read()
            for included_path in re.findall(include_pattern, content):
                for compiler_include_path in cls._program_directories:
                    included_file_path = os.path.join(compiler_include_path, included_path)
                    if not os.path.exists(included_file_path):
                        continue

                    included_file_mtime = os.path.getmtime(included_file_path)

                    if included_file_mtime > modified_after:
                        return True
                    elif cls._has_modified_includes(included_file_path, modified_after, depth=depth - 1):
                        return True

        return False

    @classmethod
    def compile(cls, source_path, output_ptx_name=None):
        if output_ptx_name is None:
            output_ptx_name = cls.get_ptx_name(source_path)

        if not os.path.isdir(cls.output_path):
            raise RuntimeError('Compiler.output_path is not a directory.')

        output_ptx_path = os.path.join(cls.output_path, output_ptx_name)
        is_compiled = True

        if cls.is_compile_required(source_path, output_ptx_path):
            if os.path.exists(output_ptx_path):
                os.remove(output_ptx_path)

            logger.info("Compiling {0}".format(source_path))
            bash_command = cls.nvcc_path + " "
            bash_command += " ".join(cls._compile_args)
            bash_command += " ".join(cls.extra_compile_args)
            bash_command += " -ptx"
            if cls.use_fast_math:
                bash_command += " --use_fast_math"
            for include_path in cls._program_directories:
                if os.path.exists(include_path):
                    bash_command += " -I=" + include_path
            bash_command += " " + source_path
            bash_command += " -o=" + output_ptx_path
            logger.debug("Executing: {0}".format(bash_command))
            try:
                check_call(shlex.split(bash_command))
            except CalledProcessError as e:
                logger.error(e)

            if not os.path.exists(output_ptx_path):
                logger.error("Could not compile {0}".format(source_path))
                raise RuntimeError("Could not compile {0}".format(source_path))
            else:
                os.chmod(output_ptx_path, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH)

        else:
            logger.debug("No compiling required for {0}".format(source_path))
            is_compiled = False

        return output_ptx_path, is_compiled

    @classmethod
    def compile_all_directories(cls, source_extension='.cu'):
        for program_dir in cls._program_directories:
            for program_path in glob_recursive(program_dir, '*' + source_extension):
                Compiler.compile(os.path.abspath(program_path))

    @classmethod
    def clean(cls):
        if os.path.exists(cls.output_path):
            for dirpath, dirnames, filenames in os.walk(cls.output_path):
                for filename in fnmatch.filter(filenames, '*.ptx'):
                    os.remove(os.path.join(dirpath, filename))

    @staticmethod
    def is_ptx(file_path):
        return os.path.splitext(file_path)[1].lower() == '.ptx'

    @staticmethod
    def get_ptx_name(file_path):
        return '%s.ptx' % file_path.replace(os.sep, '_')

    @classmethod
    def get_abs_program_path(cls, file_path):
        if os.path.exists(file_path):
            return file_path
        else:
            abs_path = find_sub_path(file_path, cls._program_directories)
            if os.path.exists(abs_path):
                return abs_path
            else:
                raise ValueError('File not found')


try:
    config_path = os.path.join(os.path.dirname(sys.executable), 'pyoptix.conf')

    if not os.path.exists(config_path):
        config_path = '/etc/pyoptix.conf'

    config = ConfigParser()
    config.read(config_path)
    nvcc_path = config.get('pyoptix', 'nvcc_path')
    compile_args = config.get('pyoptix', 'compile_args')

    if nvcc_path is not None:
        Compiler.nvcc_path = nvcc_path
    if compile_args is not None:
        Compiler._compile_args = [arg for arg in compile_args.split(os.pathsep)]

except Exception as e:
    logger.warning("Could not load pyoptix.conf")

if not os.path.exists(Compiler.output_path):
    os.makedirs(Compiler.output_path)
    os.chmod(Compiler.output_path, S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IWGRP | S_IXGRP | S_IROTH | S_IWOTH | S_IXOTH)
