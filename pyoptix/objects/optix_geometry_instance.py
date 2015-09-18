from pyoptix._driver import _OptixGeometryInstanceWrapper
from pyoptix.objects.commons.optix_object import OptixObject
from pyoptix.objects.commons.optix_scoped_object import OptixScopedObject


class OptixGeometryInstance(_OptixGeometryInstanceWrapper, OptixObject, OptixScopedObject):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixGeometryInstanceWrapper.__init__(self, native)
        OptixScopedObject.__init__(self)
