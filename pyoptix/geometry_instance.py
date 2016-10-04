from pyoptix._driver import NativeGeometryInstanceWrapper
from pyoptix.context import current_context
from pyoptix.geometry import Geometry
from pyoptix.material import Material
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.scoped import ScopedMixin


class GeometryInstance(NativeGeometryInstanceWrapper, GraphNodeMixin, ScopedMixin):
    def __init__(self, geometry=None, materials=None):
        self._context = current_context()
        self._native = self._context._create_geometry_instance()
        NativeGeometryInstanceWrapper.__init__(self, self._native)
        GraphNodeMixin.__init__(self)
        ScopedMixin.__init__(self)

        self._geometry = None
        self._materials = []

        if geometry is not None and isinstance(geometry, Geometry):
            self.set_geometry(geometry)

        if materials is not None:
            # allow single material parameter
            if isinstance(materials, Material):
                materials = [materials]

            if not isinstance(materials, list):
                raise TypeError('materials parameter must be a list')

            self._set_material_count(len(materials))
            for idx, material in enumerate(materials):
                self.set_material(idx, material)

    def add_material(self, material):
        self._set_material_count(len(self._materials))
        self._set_material(len(self._materials), material)

    def set_material(self, idx, material):
        if not isinstance(material, Material):
            raise TypeError('Parameter material is not of type MaterialObj')

        if idx > len(self._materials):
            raise IndexError('Material index is out of range')

        if idx == len(self._materials):
            self._materials.append(material)
        else:
            self._materials[idx] = material

        self._set_material_count(len(self._materials))
        self._set_material(idx, material)

    def get_material(self, idx=0):
        if idx < len(self._materials):
            return self._materials[idx]
        else:
            raise IndexError('Material index is out of range')

    def get_materials(self):
        return self._materials

    def get_material_count(self):
        return len(self._materials)

    def set_geometry(self, geometry):
        if not isinstance(geometry, Geometry):
            raise TypeError('Parameter geometry is not of type GeometryObj')

        self._geometry = geometry
        self._set_geometry(geometry)

    def get_geometry(self):
        return self._geometry
