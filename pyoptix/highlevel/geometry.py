from pyoptix.objects import GeometryObj
from pyoptix.highlevel.shared import context


class Geometry(GeometryObj):
    def __init__(self, bounding_box_program, intersection_program):
        native = context._create_geometry()
        GeometryObj.__init__(self, native=native, context=context)
        self.set_bounding_box_program(bounding_box_program)
        self.set_intersection_program(intersection_program)
