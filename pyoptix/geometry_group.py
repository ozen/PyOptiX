from pyoptix._driver import NativeGeometryGroupWrapper
from pyoptix.context import current_context
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.parent import ParentMixin


class GeometryGroup(NativeGeometryGroupWrapper, GraphNodeMixin, ParentMixin):
    def __init__(self, children=None):
        from pyoptix.acceleration import Acceleration
        from pyoptix.geometry_instance import GeometryInstance

        self._context = current_context()
        self._native = self._context._create_geometry_group()
        NativeGeometryGroupWrapper.__init__(self, self._native)
        GraphNodeMixin.__init__(self)
        ParentMixin.__init__(self, [Acceleration, GeometryInstance], children)

        self._acceleration = None

    def set_acceleration(self, acceleration):
        acceleration.validate()
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

    """
    Override get children methods because GeometryGroup's children must be of type GeometryInstance
    """
    def get_geometry_instances(self):
        return self._children

    def get_materials(self):
        materials = set()
        for geometry_instance in self._children:
            materials = materials | set(geometry_instance.get_materials())
        return list(materials)

    def get_geometries(self):
        geometries = set()
        for geometry_instance in self._children:
            geometries.add(geometry_instance.get_geometry())
        return list(geometries)
