import numpy
from pyoptix._driver import NativeBufferWrapper, RTformat
from pyoptix.context import current_context
from pyoptix.types import convert_buffer_type, get_format_from_dtype


class Buffer(NativeBufferWrapper):
    def __init__(self, buffer_type='io'):
        self._context = current_context()
        native = self._context._create_buffer(convert_buffer_type(buffer_type))
        NativeBufferWrapper.__init__(self, native)

        self._numpy_dtype = None
        self._numpy_shape = None
        self._last_dim_dropped = False

    @property
    def shape(self):
        return self._numpy_shape

    @property
    def dtype(self):
        return numpy.dtype(self._numpy_dtype)

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
        instance._restructure_and_copy_from_numpy_array(array, drop_last_dim)
        return instance

    def set_format(self, format=None, dtype=None, type_size=1):
        _format = None

        if format is not None:
            if isinstance(format, RTformat):
                _format = format
            else:
                raise ValueError('Invalid buffer format')
        elif dtype is not None:
            try:
                dtype = numpy.dtype(dtype)
                _format = get_format_from_dtype(dtype, type_size)
            except TypeError:
                raise ValueError('Invalid dtype argument')

        self._set_format(_format)

    def reset_buffer(self, numpy_shape, dtype=numpy.float32, drop_last_dim=False):
        self._numpy_dtype = numpy.dtype(dtype)
        self._numpy_shape = numpy_shape

        item_size = self._numpy_dtype.itemsize
        temp_shape = numpy_shape
        type_size = 1

        if drop_last_dim:
            item_size = numpy_shape[-1] * self._numpy_dtype.itemsize
            temp_shape = numpy_shape[0:-1]
            type_size = numpy_shape[-1]
            self._last_dim_dropped = True

        self.set_format(dtype=dtype, type_size=type_size)
        if self.get_format() == RTformat.RT_FORMAT_USER:
            self._set_element_size(item_size)

        # convert numpy dim to optix dim (inverting shape)
        temp_shape = temp_shape[::-1]
        self._set_size(list(temp_shape))

    def _restructure_according_to_numpy_array(self, numpy_array, drop_last_dim=False):
        self.reset_buffer(numpy_shape=numpy_array.shape, dtype=numpy_array.dtype, drop_last_dim=drop_last_dim)

    def _restructure_and_copy_from_numpy_array(self, numpy_array, drop_last_dim=False):
        self._restructure_according_to_numpy_array(numpy_array, drop_last_dim)
        self.copy_from_array(numpy_array)

    def to_array(self):
        numpy_array = numpy.empty(self._numpy_shape, dtype=self.dtype)
        self.copy_to_array(numpy_array)
        return numpy_array

    def copy_to_array(self, numpy_array):
        if numpy_array.nbytes != self._get_size_in_bytes():
            raise BufferError("Arrays size must be equal!")

        self._copy_into_array(numpy_array)

    def copy_from_array(self, numpy_array):
        if numpy_array.nbytes != self._get_size_in_bytes():
            raise BufferError("Arrays size must be equal!")

        self._copy_from_array(numpy_array)

    def copy_level_from_array(self, level, numpy_array):
        if numpy_array.nbytes != self._get_mip_level_size_in_bytes(level):
            raise BufferError("Arrays size must be equal!")

        self._copy_mip_level_from_array(level, numpy_array)

    def copy_level_from_buffer(self, level, buffer):
        if not isinstance(buffer, Buffer):
            raise TypeError('buffer is not of type Buffer')
        self.copy_level_from_array(self, level, buffer.to_array())
