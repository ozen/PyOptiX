import numpy
from pyoptix._driver import NativeTransformWrapper
from pyoptix.context import current_context
from pyoptix.mixins.parent import ParentMixin


class Transform(NativeTransformWrapper, ParentMixin):
    def __init__(self, children=None):
        from pyoptix.geometry_group import GeometryGroup
        from pyoptix.group import Group
        from pyoptix.selector import Selector

        self._context = current_context()
        native = self._context._create_transform()
        NativeTransformWrapper.__init__(self, native)
        ParentMixin.__init__(self, [GeometryGroup, Group, Selector, Transform], children)

        self._transpose = False

    def set(self, matrix, column_major=False):
        self._transpose = column_major

        if isinstance(matrix, numpy.ndarray) and isinstance(matrix.dtype, numpy.float32):
            self.set_matrix(self._transpose, matrix)
        else:
            self.set_matrix(self._transpose, numpy.matrix(matrix, dtype=numpy.float32))

    def get(self, column_major=None):
        transpose = column_major if column_major is not None else self._transpose
        return self.get_matrix(transpose)

    def get_child_count(self):
        return 1

    def _set_child_count(self, count):
        pass

    def set_matrix(self, transpose, matrix):
        matrix = numpy.array(matrix, dtype=numpy.float32)

        if matrix.shape != (4, 4):
            raise ValueError('Transformation matrix must be 4 by 4')

        self._set_matrix(transpose, matrix.tolist())

    def get_matrix(self, transpose):
        return numpy.array(self._get_matrix(transpose), dtype=numpy.float32)
