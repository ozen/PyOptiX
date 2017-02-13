import logging
from pyoptix.context import current_context
from pyoptix.program import Program
from pyoptix.utils import is_2_string_tuple
from pyoptix.mixins.hascontext import HasContextMixin

logger = logging.getLogger(__name__)


class EntryPoint(HasContextMixin):
    __default_exception_program = None

    @classmethod
    def set_default_exception_program(cls, file_path, function_name):
        cls.__default_exception_program = (file_path, function_name)

    def __init__(self, ray_generation_program, exception_program=None, size=None):
        HasContextMixin.__init__(self, current_context())

        if is_2_string_tuple(ray_generation_program):
            self.ray_generation_program = Program(*ray_generation_program)
        elif isinstance(ray_generation_program, Program):
            self.ray_generation_program = ray_generation_program
        else:
            raise ValueError('Invalid ray generation program given')

        if is_2_string_tuple(exception_program):
            self.exception_program = Program(*exception_program)
        elif isinstance(exception_program, Program) or exception_program is None:
            self.exception_program = exception_program
        else:
            raise ValueError('Invalid exception program given')

        self.size = size

    def __call__(self):
        self.launch()

    def __getitem__(self, item):
        return self.ray_generation_program[item]

    def __setitem__(self, key, value):
        if value is not None:
            self.ray_generation_program[key] = value

    def __delitem__(self, key):
        del self.ray_generation_program[key]
        
    def __contains__(self, item):
        return item in self.ray_generation_program

    def launch(self, size=None, context=None):
        if self.size is None and size is None:
            raise ValueError("Launch size must be set before or while launching")
        elif size is None:
            size = self.size

        if context is None:
            context = self._safe_context

        context.set_entry_point_count(1)
        context.set_ray_generation_program(0, self.ray_generation_program)

        if self.exception_program is not None:
            context.set_exception_program(0, self.exception_program)
        elif self.__default_exception_program is not None:
            context.set_exception_program(0, Program.get_or_create(*self.__default_exception_program))

        # launch
        context.validate()
        context.compile()
        logger.debug("Launching {0} with {1} threads".format(self.ray_generation_program.name, size))
        context.launch(0, *size)
