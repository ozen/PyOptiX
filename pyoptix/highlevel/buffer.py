import numpy
from pyoptix.objects import BufferObj
from pyoptix.highlevel.shared import context


class Buffer(BufferObj):
    def __init__(self, internal):
        BufferObj.__init__(self, native=internal.native, context=context)

    @classmethod
    def empty(cls, shape, dtype=numpy.float32, buffer_type='io', drop_last_dim=False):
        internal = context.create_empty_buffer(buffer_type=buffer_type,
                                               numpy_shape=shape,
                                               dtype=dtype,
                                               drop_last_dim=drop_last_dim)
        return cls(internal)

    @classmethod
    def from_array(cls, array, buffer_type='io', drop_last_dim=False):
        internal = context.create_buffer_from_numpy_array(buffer_type=buffer_type,
                                                          numpy_array=array,
                                                          drop_last_dim=drop_last_dim)
        return cls(internal)

    @classmethod
    def zeros(cls, shape, dtype=numpy.float32, buffer_type='io', drop_last_dim=False):
        internal = context.create_zeros_buffer(buffer_type=buffer_type,
                                               numpy_shape=shape,
                                               dtype=dtype,
                                               drop_last_dim=drop_last_dim)
        return cls(internal)
