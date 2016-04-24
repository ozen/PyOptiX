from pyoptix.objects import GeometryGroupObj
from pyoptix.highlevel.shared import InitChildrenMixin, context


class GeometryGroup(GeometryGroupObj, InitChildrenMixin):
    def __init__(self, children=None):
        native = context._create_geometry_group()
        GeometryGroupObj.__init__(self, native=native, context=context)
        InitChildrenMixin.__init__(self, children)
