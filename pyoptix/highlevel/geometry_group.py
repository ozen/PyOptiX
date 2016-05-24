from pyoptix.objects import GeometryGroupObj
from pyoptix.highlevel.shared import InitChildrenMixin, get_context


class GeometryGroup(GeometryGroupObj, InitChildrenMixin):
    def __init__(self, children=None):
        context = get_context()
        native = context._create_geometry_group()
        GeometryGroupObj.__init__(self, native=native, context=context)
        InitChildrenMixin.__init__(self, children)
