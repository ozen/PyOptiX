import six
from pyoptix.context import current_context
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.scoped import ScopedObject
from pyoptix.mixins.hascontext import HasContextMixin


class Material(GraphNodeMixin, ScopedObject, HasContextMixin):
    def __init__(self, closest_hit=None, any_hit=None):
        HasContextMixin.__init__(self, current_context())
        ScopedObject.__init__(self, self._safe_context._create_material())
        GraphNodeMixin.__init__(self)

        self._closest_hit_programs = {}
        self._any_hit_programs = {}

        if closest_hit is None:
            closest_hit = {}
        if any_hit is None:
            any_hit = {}

        for index, program in six.iteritems(closest_hit):
            self.set_closest_hit_program(index, program)

        for index, program in six.iteritems(any_hit):
            self.set_any_hit_program(index, program)

    def set_closest_hit_program(self, ray_type_index, program):
        self._closest_hit_programs[ray_type_index] = program
        self._safe_native.set_closest_hit_program(ray_type_index, program._safe_native)

    def get_closest_hit_program(self, ray_type_index):
        return self._closest_hit_programs[ray_type_index]

    def set_any_hit_program(self, ray_type_index, program):
        self._any_hit_programs[ray_type_index] = program
        self._safe_native.set_any_hit_program(ray_type_index, program._safe_native)

    def get_any_hit_program(self, ray_type_index):
        return self._any_hit_programs[ray_type_index]

    def validate(self):
        self._safe_native.validate()
