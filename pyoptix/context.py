import weakref
import atexit
from pyoptix._driver import NativeContextWrapper
from pyoptix.enums import ExceptionType
from pyoptix.mixins.scoped import ScopedObject


class Context(ScopedObject):
    def __init__(self):
        self._program_cache = {}
        self._ray_gen_programs = {}
        self._exception_programs = {}
        self._miss_programs = {}
        self._destroyables = []

        self._native = NativeContextWrapper()
        ScopedObject.__init__(self, self._native)

        push_context(self)

    def __del__(self):
        self._mark_all_objects_destroyed()

    def _mark_all_objects_destroyed(self):
        for destroyable in self._destroyables:
            if destroyable() is not None:
                destroyable().mark_destroyed()

    @property
    def program_cache(self):
        return self._program_cache

    def push(self):
        if current_context() == self:
            raise RuntimeError("Cannot push: Context is already at the top of the stack")
        else:
            push_context(self)

    def pop(self):
        if current_context() == self:
            pop_context()
        else:
            raise RuntimeError("Cannot pop: Context is not at the top of the stack")

    def launch(self, entry_point_index, width, height=None, depth=None):
        if not height:
            self._native.launch_1d(entry_point_index, width)
        elif not depth:
            self._native.launch_2d(entry_point_index, width, height)
        else:
            self._native.launch_3d(entry_point_index, width, height, depth)

    def _create_accelerator(self, builder, traverser):
        obj = self._native.create_accelerator(builder, traverser)
        self._destroyables.append(weakref.ref(obj))
        return obj

    def _create_geometry(self):
        obj = self._native.create_geometry()
        self._destroyables.append(weakref.ref(obj))
        return obj

    def _create_buffer(self, buffer_type):
        obj = self._native.create_buffer(buffer_type)
        self._destroyables.append(weakref.ref(obj))
        return obj

    def _create_geometry_group(self):
        obj = self._native.create_geometry_group()
        self._destroyables.append(weakref.ref(obj))
        return obj

    def _create_geometry_instance(self):
        obj = self._native.create_geometry_instance()
        self._destroyables.append(weakref.ref(obj))
        return obj

    def _create_group(self):
        obj = self._native.create_group()
        self._destroyables.append(weakref.ref(obj))
        return obj

    def _create_material(self):
        obj = self._native.create_material()
        self._destroyables.append(weakref.ref(obj))
        return obj

    def _create_program_from_file(self, file_name, function_name):
        obj = self._native.create_program_from_file(file_name, function_name)
        self._destroyables.append(weakref.ref(obj))
        return obj

    def _create_selector(self):
        obj = self._native.create_selector()
        self._destroyables.append(weakref.ref(obj))
        return obj

    def _create_texture_sampler(self):
        obj = self._native.create_texture_sampler()
        self._destroyables.append(weakref.ref(obj))
        return obj

    def _create_transform(self):
        obj = self._native.create_transform()
        self._destroyables.append(weakref.ref(obj))
        return obj

    def get_ray_type_count(self):
        return self._native.get_ray_type_count()

    def set_ray_type_count(self, ray_type_count):
        if not isinstance(ray_type_count, int) or ray_type_count < 0:
            raise TypeError('Index offset must be a positive integer')

        self._native.set_ray_type_count(ray_type_count)

    def get_entry_point_count(self):
        return self._native.get_entry_point_count()

    def set_entry_point_count(self, entry_point_count):
        if not isinstance(entry_point_count, int) or entry_point_count < 0:
            raise TypeError('Entry point count must be a positive integer')

        self._native.set_entry_point_count(entry_point_count)

    def get_cpu_num_of_threads(self):
        return self._native.get_cpu_num_of_threads()

    def set_cpu_num_of_threads(self, cpu_num_of_threads):
        if not isinstance(cpu_num_of_threads, int) or cpu_num_of_threads < 0:
            raise TypeError('Number of threads must be a positive integer')

        self._native.set_cpu_num_of_threads(cpu_num_of_threads)

    def get_stack_size(self):
        return self._native.get_stack_size()

    def set_stack_size(self, stack_size_bytes):
        if not isinstance(stack_size_bytes, int) or stack_size_bytes < 0:
            raise TypeError('Stack size is the number of bytes that must be a positive integer')

        self._native.set_stack_size(stack_size_bytes)

    def get_available_devices_count(self):
        return self._native.get_available_devices_count()

    def get_device_name(self, device_id):
        return self._native.get_device_name(device_id)

    def get_device_compute_capability(self, device_id):
        return self._native.get_device_compute_capability(device_id)

    def get_enabled_device_count(self):
        return self._native.get_enabled_device_count()

    def get_enabled_devices(self):
        return self._native.get_enabled_devices()

    def set_devices(self, devices):
        self._native.set_devices(devices)

    def get_used_host_memory(self):
        return self._native.get_used_host_memory()

    def get_available_device_memory(self, device_id):
        return self._native.get_available_device_memory(device_id)

    def get_exception_enabled(self, exception_type):
        if not isinstance(exception_type, ExceptionType):
            return TypeError('exception_type is not of type pyoptix.enums.ExceptionType')

        return self._native.get_exception_enabled(exception_type)

    def set_exception_enabled(self, exception_type, enabled=True):
        if not isinstance(exception_type, ExceptionType):
            return TypeError('exception_type is not of type pyoptix.enums.ExceptionType')

        self._native.set_exception_enabled(exception_type, enabled)

    def get_print_enabled(self):
        return self._native.get_print_enabled()

    def set_print_enabled(self, enabled=True):
        self._native.set_print_enabled(enabled)

    def get_print_buffer_size(self):
        return self._native.get_print_buffer_size()

    def set_print_buffer_size(self, print_buffer_size):
        if not isinstance(print_buffer_size, int) or print_buffer_size < 0:
            raise TypeError('Print buffer size is the number of bytes that must be a positive integer')

        self._native.set_print_buffer_size(print_buffer_size)

    def set_ray_generation_program(self, entry_point_index, program):
        self._native.set_ray_generation_program(entry_point_index, program._native)
        self._ray_gen_programs[entry_point_index] = program

    def get_ray_generation_program(self, entry_point_index):
        return self._ray_gen_programs[entry_point_index]

    def set_exception_program(self, entry_point_index, program):
        self._native.set_exception_program(entry_point_index, program._native)
        self._ray_gen_programs[entry_point_index] = program

    def get_exception_program(self, entry_point_index):
        return self._exception_programs[entry_point_index]

    def set_miss_program(self, ray_type_index, program):
        self._native.set_miss_program(ray_type_index, program._native)
        self._miss_programs[ray_type_index] = program

    def get_miss_program(self, ray_type_index):
        return self._miss_programs[ray_type_index]

    def set_all_exceptions_enabled(self, is_enabled):
        self._native.set_exception_enabled(ExceptionType.all, is_enabled)

    def validate(self):
        self._native.validate()

    def compile(self):
        self._native.compile()


_context_stack = []


def current_context():
    return _context_stack[-1]


def push_context(ctx):
    if not isinstance(ctx, Context):
        raise TypeError('ctx must be an instance of Context')
    _context_stack.append(ctx)


def pop_context():
    return _context_stack.pop()


def _clear_context_stack():
    while len(_context_stack) > 0:
        ctx = _context_stack.pop()
        ctx._mark_all_objects_destroyed()


atexit.register(_clear_context_stack)

# Create a context automatically
Context()
