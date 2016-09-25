from pyoptix._driver import NativeContextWrapper, RTexception
from pyoptix.compiler import Compiler
from pyoptix.mixins.scoped import ScopedMixin


_context_stack = []


def current_context():
    return _context_stack[-1]


def _push_context(ctx):
    if not isinstance(ctx, Context):
        raise TypeError('context must be an instance of Context')
    _context_stack.append(ctx)


def _pop_context():
    return _context_stack.pop()


class Context(NativeContextWrapper, ScopedMixin):
    def __init__(self):
        NativeContextWrapper.__init__(self)
        ScopedMixin.__init__(self)
        self._compiler = None
        self._miss_programs = {}

        _push_context(self)

    def push(self):
        if current_context() == self:
            raise RuntimeError("Cannot push: Context is already at the top of the stack")
        else:
            _push_context(self)

    def pop(self):
        if current_context() == self:
            _pop_context()
        else:
            raise RuntimeError("Cannot pop: Context is not at the top of the stack")

    @property
    def compiler(self):
        if self._compiler is None:
            self.init_compiler()
        return self._compiler

    def init_compiler(self, output_path=None, include_paths=None, arch=None, use_fast_math=None):
        kwargs = {}

        if output_path:
            kwargs['output_path'] = output_path

        if include_paths:
            kwargs['include_paths'] = include_paths

        if use_fast_math:
            kwargs['use_fast_math'] = use_fast_math

        if arch:
            kwargs['arch'] = arch
        else:
            sm_major, sm_minor = self.get_device_compute_capability(0)
            kwargs['arch'] = "sm_{0}{1}".format(sm_major, sm_minor)

        self._compiler = Compiler(**kwargs)

    def compile_program(self, file_path, ptx_name=None):
        return self.compiler.compile(file_path, ptx_name)

    def launch(self, entry_point_index, width, height=None, depth=None):
        if not height:
            self._launch_1d(entry_point_index, width)
        elif not depth:
            self._launch_2d(entry_point_index, width, height)
        else:
            self._launch_3d(entry_point_index, width, height, depth)

    def set_miss_program(self, ray_type_index, program):
        self._miss_programs[ray_type_index] = program
        self._set_miss_program(ray_type_index, program)

    def get_miss_program(self, ray_type_index):
        return self._miss_programs[ray_type_index]

    def set_all_exceptions_enabled(self, is_enabled):
        self.set_exception_enabled(RTexception.RT_EXCEPTION_ALL, is_enabled)


# Create a context automatically
_context_stack.append(Context())