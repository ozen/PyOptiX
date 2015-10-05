from pyoptix._driver import _OptixProgramWrapper
from pyoptix.objects.commons.optix_object import OptixObject
from pyoptix.objects.commons.optix_scoped_object import OptixScopedObject


class OptixProgram(_OptixProgramWrapper, OptixObject, OptixScopedObject):

    def __init__(self, native, context, file_path=None, function_name=None):
        OptixObject.__init__(self, context, native)
        OptixScopedObject.__init__(self)
        _OptixProgramWrapper.__init__(self, native)

        self.file_path = file_path
        self.function_name = function_name
