from pyoptix.objects import SelectorObj
from pyoptix.highlevel.shared import InitChildrenMixin, context


class Selector(SelectorObj, InitChildrenMixin):
    def __init__(self, children=None):
        native = context._create_selector()
        SelectorObj.__init__(self, native=native, context=context)
        InitChildrenMixin.__init__(children)
