from pyoptix._driver import NativeGeometryInstanceWrapper
from pyoptix.objects.material import MaterialObj
from pyoptix.objects.geometry import GeometryObj
from pyoptix.objects.shared.optix_object import OptixObject
from pyoptix.objects.shared.optix_scoped_object import OptixScopedObject


class GeometryInstanceObj(NativeGeometryInstanceWrapper, OptixObject, OptixScopedObject):
    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        NativeGeometryInstanceWrapper.__init__(self, native)
        OptixScopedObject.__init__(self)

        self._geometry = None
        self._materials = []

    def add_material(self, material):
        self._set_material_count(len(self._materials))
        self._set_material(len(self._materials), material)

    def set_material(self, idx, material):
        if not isinstance(material, MaterialObj):
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
        if not isinstance(geometry, GeometryObj):
            raise TypeError('Parameter geometry is not of type GeometryObj')

        self._geometry = geometry
        self._set_geometry(geometry)

    def get_geometry(self):
        return self._geometry
