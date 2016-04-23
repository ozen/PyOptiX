from pyoptix.objects import MaterialObj, GeometryInstanceObj
from pyoptix.highlevel.shared import context


class GeometryInstance(GeometryInstanceObj):
    def __init__(self, geometry=None, materials=None):
        native = context._create_geometry_instance()
        GeometryInstanceObj.__init__(self, native=native, context=context)

        if geometry is not None:
            self.set_geometry(geometry)

        if materials is not None:
            # allow single material parameter
            if isinstance(materials, MaterialObj):
                materials = [materials]

            if not isinstance(materials, list):
                raise TypeError('materials parameter must be a list')

            self.set_material_count(len(materials))
            for idx, material in enumerate(materials):
                self.set_material(idx, material)
