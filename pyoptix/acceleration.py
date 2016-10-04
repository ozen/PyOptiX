import six
from pyoptix._driver import NativeAccelerationWrapper
from pyoptix.context import current_context
from pyoptix.mixins.graphnode import GraphNodeMixin


class Acceleration(NativeAccelerationWrapper, GraphNodeMixin):
    def __init__(self, builder, traverser, **kwargs):
        self._context = current_context()
        self._native = self._context._create_accelerator(builder, traverser)
        NativeAccelerationWrapper.__init__(self, self._native)
        GraphNodeMixin.__init__(self)

        for key, value in six.iteritems(kwargs):
            self.set_property(key, value)
