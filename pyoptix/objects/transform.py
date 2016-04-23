import numpy
from pyoptix._driver import NativeTransformWrapper
from pyoptix.objects.shared.optix_object import OptixObject
from pyoptix.objects.shared.optix_parent import OptixParent


class TransformObj(NativeTransformWrapper, OptixObject, OptixParent):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        NativeTransformWrapper.__init__(self, native)

        from pyoptix.objects.geometry_group import GeometryGroupObj
        from pyoptix.objects.group import GroupObj
        from pyoptix.objects.selector import SelectorObj
        allowed_children = [GeometryGroupObj, GroupObj, SelectorObj, TransformObj]

        OptixParent.__init__(self, allowed_children)

        self.transpose = False

    def set(self, matrix, column_major=False):
        self.transpose = column_major

        if isinstance(matrix, numpy.ndarray) and isinstance(matrix.dtype, numpy.float32):
            self.set_matrix(self.transpose, matrix)
        else:
            self.set_matrix(self.transpose, numpy.matrix(matrix, dtype=numpy.float32))

    def get(self, column_major=None):
        transpose = column_major if column_major is not None else self.transpose
        return self.get_matrix(transpose)

    def get_child_count(self):
        return 1

    def _set_child_count(self, count):
        pass
