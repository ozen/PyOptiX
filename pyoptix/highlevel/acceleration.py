from pyoptix.objects import AccelerationObj
from pyoptix.highlevel.shared import context


class Acceleration(AccelerationObj):
    def __init__(self, builder, traverser, **kwargs):
        native = context._create_accelerator(builder, traverser)
        AccelerationObj.__init__(self, native=native, context=context, builder=builder, traverser=traverser)
        self.properties = kwargs
