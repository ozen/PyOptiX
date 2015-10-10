from pyoptix._driver import _OptixVariableWrapper, RTobjecttype
from pyoptix.objects.commons.types import get_object_type_from_dtype, get_pyoptix_class_from_object_type, \
    get_dtype_from_object_type
import numpy


OBJECT_TYPE_TO_SET_FUNCTION = {
    RTobjecttype.RT_OBJECTTYPE_BUFFER: '_set_buffer',
    RTobjecttype.RT_OBJECTTYPE_TEXTURE_SAMPLER: '_set_texture',
    RTobjecttype.RT_OBJECTTYPE_PROGRAM: '_set_program_id_with_program',
    RTobjecttype.RT_OBJECTTYPE_GROUP: '_set_group',
    RTobjecttype.RT_OBJECTTYPE_GEOMETRY_GROUP: '_set_geometry_group',
    RTobjecttype.RT_OBJECTTYPE_SELECTOR: '_set_selector',
    RTobjecttype.RT_OBJECTTYPE_TRANSFORM: '_set_transform',
}


class OptixVariable(_OptixVariableWrapper):

    def __init__(self, native):
        _OptixVariableWrapper.__init__(self, native)
        self._native = native
        self._value = None

    @property
    def native(self):
        return self._native

    @property
    def value(self):
        return self._native

    @value.setter
    def value(self, value):
        if self.type == RTobjecttype.RT_OBJECTTYPE_UNKNOWN or self.type == RTobjecttype.RT_OBJECTTYPE_USER:
            if isinstance(value, numpy.ndarray):
                # Use ndarray's dtype to determine variable type
                object_type = get_object_type_from_dtype(value.dtype, value.shape[-1])
                self._set_from_numpy_with_type(value, object_type)
                self._value = value
            else:
                # Unknown and user-typed variables can only be assigned an ndarray
                raise TypeError("Cannot recognize the variable type or it's user-type. You can assign a numpy array.")

        else:
            if isinstance(value, get_pyoptix_class_from_object_type(self.type)):
                # value class and variable type match, use the respective set function
                getattr(self, OBJECT_TYPE_TO_SET_FUNCTION[self.type])(value)
                self._value = value
            else:
                try:
                    # try to convert the value to the variable type
                    dtype, dim = get_dtype_from_object_type(self.type)
                    if dtype is None or dim is None:
                        raise ValueError()
                    value = numpy.array(value, dtype=dtype)
                    if len(value.shape != 1) or value.shape[0] != dim:
                        raise TypeError("Cannot convert the value to a numpy array matching %s." % self.type)
                    self._set_from_numpy_with_type(value, self.type)
                    self._value = value
                except (ValueError, AttributeError):
                    raise TypeError("Variable type is %s, but %s was given" % (self.type, type(value)))
