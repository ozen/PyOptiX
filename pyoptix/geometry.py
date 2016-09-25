from pyoptix._driver import NativeGeometryWrapper
from pyoptix.context import current_context


class Geometry(NativeGeometryWrapper):
    def __init__(self, bounding_box_program, intersection_program):
        self._context = current_context()
        native = self._context._create_geometry()
        NativeGeometryWrapper.__init__(self, native)

        self._bounding_box_program = None
        self._intersection_program = None

        self.set_bounding_box_program(bounding_box_program)
        self.set_intersection_program(intersection_program)

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
