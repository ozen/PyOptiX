from pyoptix.objects import GroupObj
from pyoptix.highlevel.shared import InitChildrenMixin, get_context


class Group(GroupObj, InitChildrenMixin):
    def __init__(self, children=None):
        context = get_context()
        native = context._create_group()
        GroupObj.__init__(self, native=native, context=context)
        InitChildrenMixin.__init__(self, children)
