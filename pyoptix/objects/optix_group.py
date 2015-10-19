from pyoptix._driver import _OptixGroupWrapper
from pyoptix.objects.commons.optix_has_child import OptixHasChild
from pyoptix.objects.commons.optix_object import OptixObject


class OptixGroup(_OptixGroupWrapper, OptixObject, OptixHasChild):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixGroupWrapper.__init__(self, native)

        from pyoptix.objects.optix_geometry_group import OptixGeometryGroup
        from pyoptix.objects.optix_selector import OptixSelector
        from pyoptix.objects.optix_transform import OptixTransform
        from pyoptix.objects.optix_acceleration import OptixAcceleration
        allowed_children = [OptixGeometryGroup, OptixGroup, OptixSelector, OptixTransform, OptixAcceleration]

        self._acceleration = None

        OptixHasChild.__init__(self, allowed_children)

    def set_acceleration(self, acceleration):
        self._set_acceleration(acceleration)
        self._acceleration = acceleration

    def get_acceleration(self):
        return self._acceleration
