from pyoptix._driver import _OptixAccelerationWrapper
from pyoptix.objects.commons.optix_object import OptixObject


class OptixAcceleration(_OptixAccelerationWrapper, OptixObject):

    def __init__(self, native, context, builder, traverser):
        OptixObject.__init__(self, context, native)
        _OptixAccelerationWrapper.__init__(self, native)
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
