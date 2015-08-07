from pyoptix.driver.Core import _OptixGeometryInstanceWrapper
from pyoptix.objects.commons.optix_has_child import OptixHasChild
from pyoptix.objects.commons.optix_object import OptixObject


class OptixGeometryInstance(_OptixGeometryInstanceWrapper, OptixObject):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixGeometryInstanceWrapper.__init__(self, native)