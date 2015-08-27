from pyoptix._driver import _OptixAccelerationWrapper
from pyoptix.objects.commons.optix_object import OptixObject


class OptixAcceleration(_OptixAccelerationWrapper, OptixObject):

    def __init__(self, native, context):

        OptixObject.__init__(self, context, native)
        _OptixAccelerationWrapper.__init__(self, native)
