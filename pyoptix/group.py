from pyoptix._driver import NativeGroupWrapper
from pyoptix.context import current_context
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.parent import ParentMixin


class Group(NativeGroupWrapper, GraphNodeMixin, ParentMixin):
    def __init__(self, children=None):
        from pyoptix.acceleration import Acceleration
        from pyoptix.geometry_group import GeometryGroup
        from pyoptix.selector import Selector
        from pyoptix.transform import Transform

        self._context = current_context()
        self._native = self._context._create_group()
        NativeGroupWrapper.__init__(self, self._native)
        GraphNodeMixin.__init__(self)
        ParentMixin.__init__(self,
                             [GeometryGroup, Group, Selector, Transform, Acceleration],
                             children)

        self._acceleration = None

    def set_acceleration(self, acceleration):
        self._set_acceleration(acceleration)
        self._acceleration = acceleration

    def get_acceleration(self):
        return self._acceleration

    """
    Use Context scope when a variable is assigned to GeometryGroup
    """
    def __getitem__(self, item):
        return self._context[item]

    def __setitem__(self, key, value):
        if value is not None:
            self._context[key] = value

    def __delitem__(self, key):
        del self._context[key]

    def __contains__(self, item):
        return item in self._context
