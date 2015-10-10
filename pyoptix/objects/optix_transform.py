from pyoptix._driver import _OptixTransformWrapper
from pyoptix.objects.commons.optix_object import OptixObject
from pyoptix.objects.commons.optix_has_child import OptixHasChild


class OptixTransform(_OptixTransformWrapper, OptixObject, OptixHasChild):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixTransformWrapper.__init__(self, native)

        from pyoptix.objects.optix_geometry_group import OptixGeometryGroup
        from pyoptix.objects.optix_group import OptixGroup
        from pyoptix.objects.optix_selector import OptixSelector

        allowed_children = [OptixGeometryGroup, OptixGroup, OptixSelector, OptixTransform]
        OptixHasChild.__init__(self, allowed_children)
