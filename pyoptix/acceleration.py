import six
from pyoptix.context import current_context
from pyoptix.mixins.graphnode import GraphNodeMixin


class Acceleration(GraphNodeMixin):
    def __init__(self, builder="NoAccel", traverser="NoAccel", **kwargs):
        self._context = current_context()
        self._native = self._context._create_accelerator(builder, traverser)
        GraphNodeMixin.__init__(self)

        for key, value in six.iteritems(kwargs):
            self._native.set_property(key, value)

    def set_property(self, key, value):
        self._native.set_property(key, value)

    def get_property(self, key):
        return self._native.get_property(key)

    def mark_dirty(self):
        self._native.mark_dirty()

    def is_dirty(self):
        return self._native.is_dirty()
