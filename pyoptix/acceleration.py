import six
from pyoptix.context import current_context
from pyoptix.mixins.destroyable import DestroyableObject
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.hascontext import HasContextMixin


class Acceleration(GraphNodeMixin, HasContextMixin, DestroyableObject):
    def __init__(self, builder="NoAccel", traverser="NoAccel", **kwargs):
        HasContextMixin.__init__(self, current_context())
        DestroyableObject.__init__(self, self._safe_context._create_accelerator(builder, traverser))
        GraphNodeMixin.__init__(self)

        for key, value in six.iteritems(kwargs):
            self._safe_native.set_property(key, value)

    def set_property(self, key, value):
        self._safe_native.set_property(key, value)

    def get_property(self, key):
        return self._safe_native.get_property(key)

    def mark_dirty(self):
        self._safe_native.mark_dirty()

    def is_dirty(self):
        return self._safe_native.is_dirty()

    def validate(self):
        self._safe_native.validate()
