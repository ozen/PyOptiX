import os
from pyoptix.objects import ProgramObj
from pyoptix.highlevel.shared import context
from pyoptix.utils import glob_recursive, find_sub_path


class Program(ProgramObj):
    __program_cache = {}
    __program_directories = []
    __dynamic_programs = False

    def __init__(self, file_path, function_name, ptx_name=None, compiled_file_path=None):
        file_path = self._get_abs_program_path(file_path)
        if ptx_name is None:
            ptx_name = self._get_ptx_name(file_path)

        internal = context.create_program(file_path=file_path,
                                          function_name=function_name,
                                          ptx_name=ptx_name,
                                          compiled_file_path=compiled_file_path)
        ProgramObj.__init__(self, native=internal.native, context=context)

    @classmethod
    def enable_dynamic_programs(cls):
        cls.__dynamic_programs = True

    @classmethod
    def disable_dynamic_programs(cls):
        cls.__dynamic_programs = False

    @classmethod
    def add_program_directory(cls, directory):
        cls.__program_directories.append(directory)
        context.compiler.include_paths.append(directory)

    @classmethod
    def compile_all_directories(cls):
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

        if program_tuple in cls.__program_cache:
            # program object exists
            if cls.dynamic_programs:
                # check if program recompiles (if program file was changed)
                compiled_path, is_compiled = context.compile_program(file_path, ptx_name)
                if is_compiled:
                    # recreate program if it was changed
                    cls.__program_cache[program_tuple] = cls(file_path, function_name, ptx_name, compiled_path)
            else:
                # return cached program if dynamic programs are disabled
                return cls.__program_cache[program_tuple]
        else:
            # compile and create if program object does not exist
            cls.__program_cache[program_tuple] = cls(file_path, function_name, ptx_name)

        return cls.__program_cache[program_tuple]

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
