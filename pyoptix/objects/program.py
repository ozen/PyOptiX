import os
from pyoptix._driver import NativeProgramWrapper
from pyoptix.objects.shared.optix_object import OptixObject
from pyoptix.objects.shared.optix_scoped_object import OptixScopedObject


class ProgramObj(NativeProgramWrapper, OptixObject, OptixScopedObject):

    def __init__(self, native, context, file_path=None, function_name=None):
        OptixObject.__init__(self, context, native)
        OptixScopedObject.__init__(self)
        NativeProgramWrapper.__init__(self, native)

        self.file_path = file_path
        self.function_name = function_name

    @property
    def name(self):
        return "({0}, {1})".format(os.path.basename(self.file_path), self.function_name)
