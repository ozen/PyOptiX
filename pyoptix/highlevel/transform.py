from pyoptix.objects import TransformObj
from pyoptix.highlevel.shared import context, InitChildrenMixin


class Transform(TransformObj, InitChildrenMixin):
    def __init__(self, children=None):
        native = context._create_transform()
        TransformObj.__init__(self, native=native, context=context)
        InitChildrenMixin.__init__(self, children)
