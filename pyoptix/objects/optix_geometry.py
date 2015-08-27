from pyoptix._driver import _OptixGeometryWrapper
from pyoptix.objects.commons.optix_scoped_object import OptixScopedObject
from pyoptix.objects.commons.optix_object import OptixObject


class OptixGeometry(_OptixGeometryWrapper, OptixObject, OptixScopedObject):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixGeometryWrapper.__init__(self, native)
        OptixScopedObject.__init__(self)
