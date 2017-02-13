import os
from pyoptix.compiler import Compiler
from pyoptix.context import current_context
from pyoptix.mixins.scoped import ScopedMixin


class Program(ScopedMixin):
    dynamic_programs = False

    def __init__(self, file_path, function_name, output_ptx_name=None):
        self._context = current_context()
        self._function_name = function_name

        file_path = Compiler.get_abs_program_path(file_path)

        if Compiler.is_ptx(file_path):
            self._ptx_path = file_path
        else:
            # if not ptx, compile to ptx
            self._ptx_path, _ = Compiler.compile(file_path, output_ptx_name)

        # Create program object from compiled file
        self._native = self._context._create_program_from_file(self._ptx_path, self._function_name)
        ScopedMixin.__init__(self, self._native)

        self._context.program_cache[(file_path, function_name)] = self

    @property
    def id(self):
        return self.get_id()

    @property
    def name(self):
        return "({0}, {1})".format(os.path.basename(self._ptx_path), self._function_name)

    @property
    def file_path(self):
        return self._ptx_path

    @property
    def function_name(self):
        return self._function_name

    def get_id(self):
        return self._native.get_id()

    @classmethod
    def get_or_create(cls, file_path, function_name):
        file_path = Compiler.get_abs_program_path(file_path)
        cache_key = (file_path, function_name)
        context = current_context()

        if cache_key not in context.program_cache:
            # create new if it does not exist in cache
            context.program_cache[cache_key] = cls(file_path, function_name)
        elif not Compiler.is_ptx(file_path) and Program.dynamic_programs:
            # check if the source file was changed. it is compiled if it was changed
            ptx_path, is_compiled = Compiler.compile(file_path)

            # recreate program object if it was changed
            if is_compiled:
                context.program_cache[cache_key] = cls(ptx_path, function_name)

        return context.program_cache[cache_key]
