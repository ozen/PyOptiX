from pyoptix.objects import TransformObj
from pyoptix.highlevel.shared import get_context, InitChildrenMixin


class Transform(TransformObj, InitChildrenMixin):
    def __init__(self, children=None):
        context = get_context()
        native = context._create_transform()
        TransformObj.__init__(self, native=native, context=context)
        InitChildrenMixin.__init__(self, children)
