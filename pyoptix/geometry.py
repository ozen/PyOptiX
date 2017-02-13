from pyoptix.context import current_context
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.scoped import ScopedObject
from pyoptix.mixins.hascontext import HasContextMixin


class Geometry(GraphNodeMixin, ScopedObject, HasContextMixin):
    def __init__(self, bounding_box_program, intersection_program):
        HasContextMixin.__init__(self, current_context())
        ScopedObject.__init__(self, self._safe_context._create_geometry())
        GraphNodeMixin.__init__(self)

        self._bounding_box_program = None
        self._intersection_program = None

        self.set_bounding_box_program(bounding_box_program)
        self.set_intersection_program(intersection_program)

    def mark_dirty(self):
        self._native.mark_dirty()

    def is_dirty(self):
        return self._native.is_dirty()

    def set_primitive_count(self, num_primitives):
        if not isinstance(num_primitives, int) or num_primitives < 0:
            raise TypeError('Primitive count must be an unsigned integer')

        self._native.set_primitive_count(num_primitives)

    def get_primitive_count(self):
        return self._native.get_primitive_count()

    def set_primitive_index_offset(self, index_offset):
        if not isinstance(index_offset, int) or index_offset < 0:
            raise TypeError('Index offset must be an unsigned integer')

        self._native.set_primitive_index_offset(index_offset)

    def get_primitive_index_offset(self):
        return self._native.get_primitive_index_offset()

    def set_bounding_box_program(self, program):
        self._bounding_box_program = program
        self._native.set_bounding_box_program(program._native)

    def get_bounding_box_program(self):
        return self._bounding_box_program

    def set_intersection_program(self, program):
        self._intersection_program = program
        self._native.set_intersection_program(program._native)

    def get_intersection_program(self):
        return self._intersection_program

    def validate(self):
        self._native.validate()
