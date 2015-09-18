from pyoptix._driver import _OptixGeometryGroupWrapper
from pyoptix.objects.commons.optix_has_child import OptixHasChild
from pyoptix.objects.commons.optix_object import OptixObject
from pyoptix.objects.optix_geometry_instance import OptixGeometryInstance
from pyoptix.objects.optix_acceleration import OptixAcceleration


class OptixGeometryGroup(_OptixGeometryGroupWrapper, OptixObject, OptixHasChild):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixGeometryGroupWrapper.__init__(self, native)

        allowed_children = [OptixGeometryInstance, OptixAcceleration]
        self._acceleration = None

        OptixHasChild.__init__(self, allowed_children)

    def set_acceleration(self, acceleration):
        self._set_acceleration(acceleration)
        self._acceleration = acceleration
