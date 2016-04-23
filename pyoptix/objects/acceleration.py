from pyoptix._driver import NativeAccelerationWrapper
from pyoptix.objects.shared.optix_object import OptixObject


class AccelerationObj(NativeAccelerationWrapper, OptixObject):
    def __init__(self, native, context, builder, traverser):
        OptixObject.__init__(self, context, native)
        NativeAccelerationWrapper.__init__(self, native)
        self.builder = builder
        self.traverser = traverser
        self.properties = {}

    def set_property(self, name, value):
        self.properties[name] = value
        self._set_property(name, value)

    def get_property(self, name):
        return self.properties[name]

    def clone(self):
        clone = self._context.create_acceleration(self.builder, self.traverser)
        for key, value in self.properties.items():
            clone.set_property(key, value)
        return clone
