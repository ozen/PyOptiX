from pyoptix.context import current_context
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.parent import ParentMixin


class Selector(GraphNodeMixin, ParentMixin):
    def __init__(self, children=None):
        from pyoptix.geometry_group import GeometryGroup
        from pyoptix.group import Group
        from pyoptix.transform import Transform

        self._context = current_context()
        self._native = self._context._create_selector()
        GraphNodeMixin.__init__(self)
        ParentMixin.__init__(self, self._native,
                             [GeometryGroup, Group, Selector, Transform], children)

    def set_visit_program(self, program):
        self._native.set_visit_program(program._native)
