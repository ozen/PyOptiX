import os
from pyoptix._driver import NativeProgramWrapper
from pyoptix.context import current_context
from pyoptix.mixins.scoped import ScopedMixin
from pyoptix.utils import glob_recursive, find_sub_path


class Program(NativeProgramWrapper, ScopedMixin):
    __program_cache = {}
    __program_directories = []
    __dynamic_programs = False
    __last_context = None

    def __init__(self, file_path, function_name, ptx_name=None, compiled_file_path=None):
        self._file_path = self._get_abs_program_path(file_path)
        self._function_name = function_name

        if ptx_name is None:
            ptx_name = self._get_ptx_name(self._file_path)

        self._context = current_context()

        if compiled_file_path is None:
            # Compile program
            compiled_file_path, is_compiled = self._context.compile_program(file_path, ptx_name)

        # Create program object from compiled file
        native = self._context._create_program_from_file(compiled_file_path, function_name)

        NativeProgramWrapper.__init__(self, native)
        ScopedMixin.__init__(self)

    @property
    def name(self):
        return "({0}, {1})".format(os.path.basename(self._file_path), self._function_name)

    @property
    def file_path(self):
        return self._file_path

    @property
    def function_name(self):
        return self._function_name

    @classmethod
    def enable_dynamic_programs(cls):
        cls.__dynamic_programs = True

    @classmethod
    def disable_dynamic_programs(cls):
        cls.__dynamic_programs = False

    @classmethod
    def add_program_directory(cls, directory):
        context = current_context()

        if directory not in cls.__program_directories:
            cls.__program_directories.append(directory)
            context.compiler.include_paths.append(directory)

    @classmethod
    def compile_all_directories(cls):
        context = current_context()

        for program_dir in cls.__program_directories:
            for program_path in glob_recursive(program_dir, '*.cu'):
                file_path = os.path.abspath(program_path)
                ptx_name = cls._get_ptx_name(file_path)
                context.compile_program(file_path, ptx_name)

    @classmethod
    def get_or_create(cls, file_path, function_name):
        file_path = cls._get_abs_program_path(file_path)
        ptx_name = cls._get_ptx_name(file_path)
        program_tuple = (file_path, function_name)

        context = current_context()

        if context not in cls.__program_cache:
            cls.__program_cache[context] = {}

        program_cache = cls.__program_cache[context]

        if program_tuple in program_cache:
            # program object exists
            if cls.__dynamic_programs:
                # check if program recompiles (if program file was changed)
                compiled_path, is_compiled = context.compile_program(file_path, ptx_name)
                if is_compiled:
                    # recreate program if it was changed
                    program_cache[program_tuple] = cls(file_path, function_name, ptx_name, compiled_path)
            else:
                # return cached program if dynamic programs are disabled
                return program_cache[program_tuple]
        else:
            # compile and create if program object does not exist
            program_cache[program_tuple] = cls(file_path, function_name, ptx_name)

        return program_cache[program_tuple]

    @classmethod
    def _get_ptx_name(cls, file_path):
        return '%s.ptx' % file_path.replace(os.sep, '_')

    @classmethod
    def _get_abs_program_path(cls, file_path):
        if os.path.exists(file_path):
            return file_path
        else:
            abs_path = find_sub_path(file_path, cls.__program_directories)
            if os.path.exists(abs_path):
                return abs_path
            else:
                raise ValueError('File not found')
