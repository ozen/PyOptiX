import six
from pyoptix.context import current_context
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.scoped import ScopedMixin


class Material(GraphNodeMixin, ScopedMixin):
    def __init__(self, closest_hit=None, any_hit=None):
        self._context = current_context()
        self._native = self._context._create_material()
        GraphNodeMixin.__init__(self)
        ScopedMixin.__init__(self, self._native)

        self._closest_hit_programs = {}
        self._any_hit_programs = {}

        if closest_hit is None:
            closest_hit = {}
        if any_hit is None:
            any_hit = {}

        for index, program in six.iteritems(closest_hit):
            self.set_closest_hit_program(index, program._native)

        for index, program in six.iteritems(any_hit):
            self.set_any_hit_program(index, program._native)

    def set_closest_hit_program(self, ray_type_index, program):
        self._closest_hit_programs[ray_type_index] = program
        self._native.set_closest_hit_program(ray_type_index, program._native)

    def get_closest_hit_program(self, ray_type_index):
        return self._closest_hit_programs[ray_type_index]

    def set_any_hit_program(self, ray_type_index, program):
        self._any_hit_programs[ray_type_index] = program
        self._native.set_any_hit_program(ray_type_index, program._native)

    def get_any_hit_program(self, ray_type_index):
        return self._any_hit_programs[ray_type_index]
