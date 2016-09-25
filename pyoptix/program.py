import os
from pyoptix._driver import NativeProgramWrapper
from pyoptix.compiler import Compiler
from pyoptix.context import current_context
from pyoptix.mixins.scoped import ScopedMixin


class Program(NativeProgramWrapper, ScopedMixin):
    def __init__(self, file_path, function_name, ptx_name=None, compiled_file_path=None):
        self._context = current_context()

        self._file_path = Compiler.get_abs_program_path(file_path)
        self._function_name = function_name

        if ptx_name is None:
            ptx_name = Compiler.get_ptx_name(self._file_path)

        if compiled_file_path is None:
            # Compile program
            compiled_file_path, is_compiled = Compiler.compile(file_path, ptx_name)

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
    def get_or_create(cls, file_path, function_name):
        file_path = Compiler.get_abs_program_path(file_path)
        ptx_name = Compiler.get_ptx_name(file_path)
        program_tuple = (file_path, function_name)

        context = current_context()

        if program_tuple in context.program_cache:
            # program object exists
            if Compiler.dynamic_programs:
                # check if program recompiles (if program file was changed)
                compiled_path, is_compiled = Compiler.compile(file_path, ptx_name)
                if is_compiled:
                    # recreate program since it was changed
                    context.program_cache[program_tuple] = cls(file_path, function_name, ptx_name, compiled_path)
        else:
            # compile and create if program object does not exist
            context.program_cache[program_tuple] = cls(file_path, function_name, ptx_name)

        return context.program_cache[program_tuple]
