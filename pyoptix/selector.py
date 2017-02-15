from pyoptix.context import current_context
from pyoptix.mixins.destroyable import DestroyableObject
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.parent import ParentMixin
from pyoptix.mixins.hascontext import HasContextMixin


class Selector(GraphNodeMixin, ParentMixin, HasContextMixin, DestroyableObject):
    def __init__(self, children=None):
        from pyoptix.geometry_group import GeometryGroup
        from pyoptix.group import Group
        from pyoptix.transform import Transform

        HasContextMixin.__init__(self, current_context())
        DestroyableObject.__init__(self, self._safe_context._create_selector())
        GraphNodeMixin.__init__(self)
        ParentMixin.__init__(self, [GeometryGroup, Group, Selector, Transform], children)

        self._visit_program = None

    def set_visit_program(self, program):
        self._safe_native.set_visit_program(program._safe_native)
        self._visit_program = program

    def get_visit_program(self):
        return self._visit_program

    def validate(self):
        self._safe_native.validate()
