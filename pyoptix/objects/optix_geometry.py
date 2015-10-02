from pyoptix._driver import _OptixGeometryWrapper
from pyoptix.objects.commons.optix_scoped_object import OptixScopedObject
from pyoptix.objects.commons.optix_object import OptixObject


class OptixGeometry(_OptixGeometryWrapper, OptixObject, OptixScopedObject):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixGeometryWrapper.__init__(self, native)
        OptixScopedObject.__init__(self)

        self._bounding_box_program = None
        self._intersection_program = None

    def set_bounding_box_program(self, program):
        self._bounding_box_program = program
        self._set_bounding_box_program(program)

    def get_bounding_box_program(self):
        return self._bounding_box_program

    def set_intersection_program(self, program):
        self._intersection_program = program
        self._set_intersection_program(program)

    def get_intersection_program(self):
        return self._intersection_program
