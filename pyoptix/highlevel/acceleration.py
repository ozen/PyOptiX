import six
from pyoptix.objects import AccelerationObj
from pyoptix.highlevel.shared import get_context


class Acceleration(AccelerationObj):
    def __init__(self, builder, traverser, **kwargs):
        context = get_context()
        native = context._create_accelerator(builder, traverser)
        AccelerationObj.__init__(self, native=native, context=context, builder=builder, traverser=traverser)
        for key, value in six.iteritems(kwargs):
            self.set_property(key, value)
