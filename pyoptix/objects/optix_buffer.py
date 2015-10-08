import numpy
from pyoptix._driver import _OptixBufferWrapper
from pyoptix._driver import RTformat
from pyoptix.objects.commons.optix_object import OptixObject
from pyoptix.objects.commons.types import get_format_from_dtype


class OptixBuffer(_OptixBufferWrapper, OptixObject):
    _dtype_numpy = None
    _shape_numpy = None
    _last_dim_dropped = None

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixBufferWrapper.__init__(self, native)
        self._last_dim_dropped = False

    @property
    def id(self):
        return self.get_id()

    @property
    def shape_of_optix_buffer(self):
        return tuple(self._get_shape())

    @property
    def itemsize_of_optix_buffer(self):
        return self._get_element_size()

    @property
    def shape(self):
        return self._shape_numpy

    @property
    def dtype(self):
        return numpy.dtype(self._dtype_numpy)

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
        self._dtype_numpy = numpy.dtype(dtype)
        self._shape_numpy = numpy_shape

        item_size = self._dtype_numpy.itemsize
        temp_shape = numpy_shape
        type_size = 1

        if drop_last_dim:
            item_size = numpy_shape[-1] * self._dtype_numpy.itemsize
            temp_shape = numpy_shape[0:-1]
            type_size = numpy_shape[-1]
            self._last_dim_dropped = True

        self.set_format(dtype=dtype, type_size=type_size)
        if self.get_format() == RTformat.RT_FORMAT_USER:
            self._set_element_size(item_size)

        # convert numpy dim to optix dim (inverting shape)
        temp_shape = temp_shape[::-1]
        self._set_shape(list(temp_shape))

    # NUMPY SUPPORT
    def restructure_according_to_numpy_array(self, numpy_array, drop_last_dim=False):
        self.reset_buffer(numpy_shape=numpy_array.shape, dtype=numpy_array.dtype, drop_last_dim=drop_last_dim)

    def restructure_and_copy_from_numpy_array(self, numpy_array, drop_last_dim=False):
        self.restructure_according_to_numpy_array(numpy_array, drop_last_dim)
        self.copy_data_from_numpy_array(numpy_array)

    def get_as_numpy_array(self):
        numpy_array = numpy.empty(self._shape_numpy, dtype=self.dtype)
        self.copy_data_into_numpy_array(numpy_array)
        return numpy_array

    def copy_data_from_numpy_array(self, numpy_array):
        if numpy_array.nbytes != self.nbytes:
            raise BufferError("Arrays size must be equal!")

        self._copy_from_numpy_array(numpy_array)

    def copy_data_into_numpy_array(self, numpy_array):
        if numpy_array.nbytes != self.nbytes:
            raise BufferError("Arrays size must be equal!")

        self._copy_into_numpy_array(numpy_array)

