from pyoptix.objects import SelectorObj
from pyoptix.highlevel.shared import InitChildrenMixin, get_context


class Selector(SelectorObj, InitChildrenMixin):
    def __init__(self, children=None):
        context = get_context()
        native = context._create_selector()
        SelectorObj.__init__(self, native=native, context=context)
        InitChildrenMixin.__init__(self, children)
