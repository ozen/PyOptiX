__author__ = 'vizera-ubuntu'

from PyOptix.objects.commons.optix_object import OptixObject
from PyOptixCpp.Core import _OptixAccelerationWrapper

class OptixAcceleration(_OptixAccelerationWrapper, OptixObject):

    def __init__(self, native, context):

        OptixObject.__init__(self, context, native)
        _OptixAccelerationWrapper.__init__(self, native)
