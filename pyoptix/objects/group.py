from pyoptix._driver import NativeGroupWrapper
from pyoptix.objects.shared.optix_parent import OptixParent
from pyoptix.objects.shared.optix_object import OptixObject


class GroupObj(NativeGroupWrapper, OptixObject, OptixParent):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        NativeGroupWrapper.__init__(self, native)

        from pyoptix.objects.geometry_group import GeometryGroupObj
        from pyoptix.objects.selector import SelectorObj
        from pyoptix.objects.transform import TransformObj
        from pyoptix.objects.acceleration import AccelerationObj
        allowed_children = [GeometryGroupObj, GroupObj, SelectorObj, TransformObj, AccelerationObj]
        OptixParent.__init__(self, allowed_children)

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
        return self.context[item]

    def __setitem__(self, key, value):
        if value is not None:
            self.context[key] = value

    def __delitem__(self, key):
        del self.context[key]

    def __contains__(self, item):
        return item in self.context
