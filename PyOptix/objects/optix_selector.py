__author__ = 'vizera-ubuntu'

from PyOptixCpp.Core import _OptixSelectorWrapper

from PyOptix.objects.commons.optix_has_child import OptixHasChild
from PyOptix.objects.commons.optix_object import OptixObject

class OptixSelector(_OptixSelectorWrapper, OptixObject, OptixHasChild):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixSelectorWrapper.__init__(self, native)

        from PyOptix.objects.optix_geometry_group import OptixGeometryGroup
        from PyOptix.objects.optix_group import OptixGroup
        from PyOptix.objects.optix_selector import OptixSelector
        from PyOptix.objects.optix_transform import OptixTransform

        allowed_children = [OptixGeometryGroup, OptixGroup, OptixSelector, OptixTransform]
        OptixHasChild.__init__(self, allowed_children)