__author__ = 'vizera-ubuntu'

from PyOptixCpp.Core import _OptixProgramWrapper

from PyOptix.objects.commons.optix_object import OptixObject
from PyOptix.objects.commons.optix_scoped_object import OptixScopedObject

class OptixProgram(_OptixProgramWrapper, OptixObject, OptixScopedObject):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        OptixScopedObject.__init__(self)
        _OptixProgramWrapper.__init__(self, native)
