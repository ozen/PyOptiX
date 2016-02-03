from pyoptix._driver import _OptixVariableWrapper, RTobjecttype
from pyoptix.objects.commons.types import get_object_type_from_dtype, get_dtype_from_object_type, \
    get_object_type_from_pyoptix_class
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

    def __init__(self, wrapped_variable):
        _OptixVariableWrapper.__init__(self, wrapped_variable._native)
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        optix_has_type = False
        if self.type != RTobjecttype.RT_OBJECTTYPE_UNKNOWN and self.type != RTobjecttype.RT_OBJECTTYPE_USER:
            optix_has_type = True

        class_object_type = get_object_type_from_pyoptix_class(value)

        if class_object_type:
            # OPTION 1: value is a known OptiX object like GeometryGroup, Buffer etc.
            # do a preliminary check on type right now so it won't fail in device-compile time
            if optix_has_type and self.type != class_object_type and self.type != RTobjecttype.RT_OBJECTTYPE_OBJECT:
                raise TypeError("Variable type is {0}, but {1} was given".format(self.type, type(value)))

            # call the respective set function of the optix type of the variable
            getattr(self, OBJECT_TYPE_TO_SET_FUNCTION[class_object_type])(value)
            self._value = value

        elif optix_has_type:
            # OPTION 2: OptiX variable has a type but value is not a known OptiX object.
            # Try to form a numpy array from value that is compatible with the variable type.
            try:
                dtype, dim = get_dtype_from_object_type(self.type)
                if dtype is None or dim is None:
                    raise ValueError()
                value = numpy.array(value, dtype=dtype)
                if len(value.shape) != 1:
                    value = value.reshape(1)
                if value.shape[0] != dim:
                    raise TypeError("Cannot convert the value to a numpy array matching {0}.".format(self.type))
                self._set_from_numpy_with_type(value, self.type)
                self._value = value
            except (ValueError, AttributeError):
                raise TypeError("Variable type is {0}, but {1} was given".format(self.type, type(value)))

        elif isinstance(value, numpy.ndarray) and not optix_has_type:
            # OPTION 3: OptiX variable type is unknown or it is user-type, but the value is a numpy array.
            # Use ndarray's dtype to determine variable type
            if len(value.shape) == 0:
                value = value.reshape(1)
            object_type = get_object_type_from_dtype(value.dtype, value.shape[-1])
            self._set_from_numpy_with_type(value, object_type)
            self._value = value

        else:
            # Unknown and user-typed variables can only be assigned an ndarray
            raise TypeError("Cannot recognize the variable type or it's user-type. You can assign a numpy array.")
