from pyoptix.driver.Core import _OptixGroupWrapper
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

        OptixHasChild.__init__(self, allowed_children)