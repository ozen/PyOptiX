import six
from pyoptix._driver import NativeMaterialWrapper
from pyoptix.context import current_context
from pyoptix.mixins.scoped import ScopedMixin


class Material(NativeMaterialWrapper, ScopedMixin):
    def __init__(self, closest_hit=None, any_hit=None):
        self._context = current_context()
        native = self._context._create_material()
        NativeMaterialWrapper.__init__(self, native)
        ScopedMixin.__init__(self)

        self._closest_hit_programs = {}
        self._any_hit_programs = {}

        if closest_hit is None:
            closest_hit = {}
        if any_hit is None:
            any_hit = {}

        for key, value in six.iteritems(closest_hit):
            self.set_closest_hit_program(key, value)

        for key, value in six.iteritems(any_hit):
            self.set_any_hit_program(key, value)

    def set_closest_hit_program(self, ray_type_index, program):
        self._closest_hit_programs[ray_type_index] = program
        self._set_closest_hit_program(ray_type_index, program)

    def get_closest_hit_program(self, ray_type_index):
        return self._closest_hit_programs[ray_type_index]

    def set_any_hit_program(self, ray_type_index, program):
        self._any_hit_programs[ray_type_index] = program
        self._set_any_hit_program(ray_type_index, program)

    def get_any_hit_program(self, ray_type_index):
        return self._any_hit_programs[ray_type_index]
