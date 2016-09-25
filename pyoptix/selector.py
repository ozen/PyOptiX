from pyoptix._driver import NativeSelectorWrapper
from pyoptix.context import current_context
from pyoptix.mixins.parent import ParentMixin


class Selector(NativeSelectorWrapper, ParentMixin):
    def __init__(self, children=None):
        from pyoptix.geometry_group import GeometryGroup
        from pyoptix.group import Group
        from pyoptix.transform import Transform

        self._context = current_context()
        native = self._context._create_selector()
        NativeSelectorWrapper.__init__(self, native)
        ParentMixin.__init__(self, [GeometryGroup, Group, Selector, Transform], children)
