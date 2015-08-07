from pyoptix.driver.Core import _OptixSelectorWrapper
from pyoptix.objects.commons.optix_has_child import OptixHasChild
from pyoptix.objects.commons.optix_object import OptixObject


class OptixSelector(_OptixSelectorWrapper, OptixObject, OptixHasChild):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixSelectorWrapper.__init__(self, native)

        from pyoptix.objects.optix_geometry_group import OptixGeometryGroup
        from pyoptix.objects.optix_group import OptixGroup
        from pyoptix.objects.optix_selector import OptixSelector
        from pyoptix.objects.optix_transform import OptixTransform

        allowed_children = [OptixGeometryGroup, OptixGroup, OptixSelector, OptixTransform]
        OptixHasChild.__init__(self, allowed_children)