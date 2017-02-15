import numpy
from pyoptix.enums import Format, convert_buffer_type, get_format_from_dtype
from pyoptix.context import current_context
from pyoptix.mixins.bindless import BindlessMixin
from pyoptix.mixins.destroyable import DestroyableObject
from pyoptix.mixins.hascontext import HasContextMixin


class Buffer(HasContextMixin, DestroyableObject, BindlessMixin):
    def __init__(self, buffer_type='io'):
        HasContextMixin.__init__(self, current_context())
        DestroyableObject.__init__(self, self._safe_context._create_buffer(convert_buffer_type(buffer_type)))
        BindlessMixin.__init__(self)

        self._numpy_dtype = None
        self._numpy_shape = None
        self._last_dim_dropped = False

    @property
    def id(self):
        return self.get_id()

    @property
    def numpy_shape(self):
        return self._numpy_shape

    @property
    def shape(self):
        return self._safe_native.get_size()

    @property
    def dtype(self):
        return numpy.dtype(self._numpy_dtype)

    @property
    def size(self):
        return self._safe_native.get_size_in_bytes()

    @property
    def element_size(self):
        return self._safe_native.get_element_size()

    @classmethod
    def empty(cls, shape, dtype=numpy.float32, buffer_type='io', drop_last_dim=False):
        instance = cls(buffer_type=buffer_type)
        instance._reset_buffer(shape, dtype, drop_last_dim)
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

    def get_id(self):
        return self._safe_native.get_id()

    def mark_dirty(self):
        self._safe_native.mark_dirty()

    def get_element_size(self):
        return self._safe_native.get_element_size()

    def get_size(self):
        return self._safe_native.get_size()

    def get_size_in_bytes(self):
        return self._safe_native.get_size_in_bytes()

    def set_format(self, format=None, dtype=None, type_size=1):
        _format = None

        if format is not None:
            if isinstance(format, Format):
                _format = format
            else:
                raise ValueError('Invalid buffer format')
        elif dtype is not None:
            try:
                dtype = numpy.dtype(dtype)
                _format = get_format_from_dtype(dtype, type_size)
            except TypeError:
                raise ValueError('Invalid dtype argument')

        self._safe_native.set_format(_format)

    def _reset_buffer(self, numpy_shape, dtype=numpy.float32, drop_last_dim=False):
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
        if self._safe_native.get_format() == Format.user:
            self._safe_native.set_element_size(item_size)

        # convert numpy dim to optix dim (inverting shape)
        temp_shape = temp_shape[::-1]
        self._safe_native.set_size(list(temp_shape))

    def _restructure_according_to_numpy_array(self, numpy_array, drop_last_dim=False):
        self._reset_buffer(numpy_shape=numpy_array.shape, dtype=numpy_array.dtype, drop_last_dim=drop_last_dim)

    def _restructure_and_copy_from_numpy_array(self, numpy_array, drop_last_dim=False):
        self._restructure_according_to_numpy_array(numpy_array, drop_last_dim)
        self.copy_from_array(numpy_array)

    def to_array(self):
        numpy_array = numpy.empty(self._numpy_shape, dtype=self.dtype)
        self.copy_to_array(numpy_array)
        return numpy_array

    def copy_to_array(self, numpy_array):
        if numpy_array.nbytes != self._safe_native.get_size_in_bytes():
            raise BufferError("Arrays size must be equal!")

        self._safe_native.copy_into_array(numpy_array)

    def copy_from_array(self, numpy_array):
        if numpy_array.nbytes != self._safe_native.get_size_in_bytes():
            raise BufferError("Arrays size must be equal!")

        self._safe_native.copy_from_array(numpy_array)

    def set_mip_level_count(self, level_count):
        self._safe_native.set_mip_level_count(level_count)

    def get_mip_level_count(self):
        return self._safe_native.get_mip_level_count()

    def get_mip_level_size(self):
        return self._safe_native.get_mip_level_size()

    def get_mip_level_size_in_bytes(self):
        return self._safe_native.get_mip_level_size_in_bytes()

    def copy_level_from_array(self, level, numpy_array):
        if numpy_array.nbytes != self._safe_native.get_mip_level_size_in_bytes(level):
            raise BufferError("Arrays size must be equal!")

        self._safe_native.copy_mip_level_from_array(level, numpy_array)

    def copy_level_from_buffer(self, level, buffer):
        if not isinstance(buffer, Buffer):
            raise TypeError('buffer is not of type Buffer')
        self.copy_level_from_array(self, level, buffer.to_array())

    def validate(self):
        self._safe_native.validate()
