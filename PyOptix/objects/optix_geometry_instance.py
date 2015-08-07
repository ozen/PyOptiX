from PyOptixCpp.Core import _OptixGeometryInstanceWrapper
from PyOptix.objects.commons.optix_has_child import OptixHasChild
from PyOptix.objects.commons.optix_object import OptixObject


class OptixGeometryInstance(_OptixGeometryInstanceWrapper, OptixObject):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixGeometryInstanceWrapper.__init__(self, native)