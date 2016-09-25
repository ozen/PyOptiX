import logging
import re
import os
import shlex
import fnmatch
import six
from subprocess import check_call, CalledProcessError
from pyoptix.utils import glob_recursive, find_sub_path

logger = logging.getLogger(__name__)


class CompilerMeta(type):
    def __init__(cls, name, bases, attrs):
        super(CompilerMeta, cls).__init__(name, bases, attrs)

        if not os.path.exists(attrs['output_path']):
            os.makedirs(attrs['output_path'])


class Compiler(six.with_metaclass(CompilerMeta, object)):
    nvcc_path = 'nvcc'
    optix_include_path = '/usr/local/optix/include'
    program_directories = []
    output_path = '/tmp/pyoptix/ptx'
    use_fast_math = True
    dynamic_programs = False
    _arch = 'sm_21'

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
                for compiler_include_path in cls.program_directories:
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

        output_ptx_path = os.path.join(cls.output_path, output_ptx_name)
        is_compiled = True

        if cls.is_compile_required(source_path, output_ptx_path):
            if os.path.exists(output_ptx_path):
                os.remove(output_ptx_path)

            logger.info("Compiling {0}".format(source_path))
            bash_command = cls.nvcc_path + " " + source_path
            bash_command += " -ptx"
            bash_command += " -arch=" + cls._arch
            if cls.use_fast_math:
                bash_command += " --use_fast_math"
            for include_path in cls.program_directories + [cls.optix_include_path]:
                if os.path.exists(include_path):
                    bash_command += " -I=" + include_path
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
            logger.debug("No compiling required for {0}".format(source_path))
            is_compiled = False

        return output_ptx_path, is_compiled

    @classmethod
    def compile_all_directories(cls, source_extension='.cu'):
        for program_dir in cls.program_directories:
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
            abs_path = find_sub_path(file_path, cls.program_directories)
            if os.path.exists(abs_path):
                return abs_path
            else:
                raise ValueError('File not found')
