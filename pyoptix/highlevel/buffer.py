import numpy
from pyoptix.objects import BufferObj
from pyoptix.highlevel.shared import context
from pyoptix.types import convert_buffer_type


class Buffer(BufferObj):
    def __init__(self, buffer_type='io'):
        native = context._create_buffer(convert_buffer_type(buffer_type))
        BufferObj.__init__(self, native=native, context=context)

    @classmethod
    def empty(cls, shape, dtype=numpy.float32, buffer_type='io', drop_last_dim=False):
        instance = cls(buffer_type=buffer_type)
        instance.reset_buffer(shape, dtype, drop_last_dim)
        return instance

    @classmethod
    def from_array(cls, array, dtype=None, buffer_type='io', drop_last_dim=False):
        if not isinstance(array, numpy.ndarray):
            try:
                array = numpy.array(array, dtype=dtype)
            except Exception as e:
                raise TypeError('array parameter must be a numpy array or castable to numpy array')

        instance = cls(buffer_type=buffer_type)
        instance.restructure_and_copy_from_numpy_array(array, drop_last_dim)
        return instance

    @classmethod
    def zeros(cls, shape, dtype=numpy.float32, buffer_type='io', drop_last_dim=False):
        instance = cls(buffer_type=buffer_type)
        instance.restructure_and_copy_from_numpy_array(numpy.zeros(shape, dtype=dtype), drop_last_dim)
        return instance
