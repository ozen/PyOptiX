import six
from pyoptix._driver import NativeAccelerationWrapper
from pyoptix.context import current_context


class Acceleration(NativeAccelerationWrapper):
    def __init__(self, builder, traverser, **kwargs):
        self._context = current_context()
        native = self._context._create_accelerator(builder, traverser)
        NativeAccelerationWrapper.__init__(self, native)

        for key, value in six.iteritems(kwargs):
            self.set_property(key, value)
