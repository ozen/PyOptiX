from pyoptix._driver import NativeGeometryGroupWrapper
from pyoptix.objects.shared.optix_parent import OptixParent
from pyoptix.objects.shared.optix_object import OptixObject
from pyoptix.objects.geometry_instance import GeometryInstanceObj
from pyoptix.objects.acceleration import AccelerationObj


class GeometryGroupObj(NativeGeometryGroupWrapper, OptixObject, OptixParent):
    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        NativeGeometryGroupWrapper.__init__(self, native)
        allowed_children = [GeometryInstanceObj, AccelerationObj]
        OptixParent.__init__(self, allowed_children)
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
        return self.context[item]

    def __setitem__(self, key, value):
        if value is not None:
            self.context[key] = value

    def __delitem__(self, key):
        del self.context[key]

    def __contains__(self, item):
        return item in self.context

    """
    Override get children methods because GeometryGroupObj's children must be GeometryInstanceObjs
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
