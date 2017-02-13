import numpy
from pyoptix.context import current_context
from pyoptix.mixins.destroyable import DestroyableObject
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.parent import ParentMixin
from pyoptix.mixins.hascontext import HasContextMixin


class Transform(GraphNodeMixin, ParentMixin, HasContextMixin, DestroyableObject):
    def __init__(self, children=None):
        from pyoptix.geometry_group import GeometryGroup
        from pyoptix.group import Group
        from pyoptix.selector import Selector

        HasContextMixin.__init__(self, current_context())
        DestroyableObject.__init__(self, self._safe_context._create_transform())
        GraphNodeMixin.__init__(self)
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

        self._safe_native.set_matrix(transpose, matrix.tolist())

    def get_matrix(self, transpose):
        return numpy.array(self._safe_native.get_matrix(transpose), dtype=numpy.float32)

    def validate(self):
        self._safe_native.validate()
