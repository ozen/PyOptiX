import numpy
from pyoptix.enums import ObjectType, get_object_type_from_dtype, get_dtype_from_object_type, \
    get_object_type_from_pyoptix_class

OBJECT_TYPE_TO_SET_FUNCTION = {
    ObjectType.buffer: 'set_buffer',
    ObjectType.texture_sampler: 'set_texture',
    ObjectType.program: 'set_program_id_with_program',
    ObjectType.group: 'set_group',
    ObjectType.geometry_group: 'set_geometry_group',
    ObjectType.selector: 'set_selector',
    ObjectType.transform: 'set_transform',
}


class Variable(object):
    def __init__(self, wrapped_variable):
        self._native = wrapped_variable
        self._value = None

    @property
    def name(self):
        return self._native.name

    @property
    def type(self):
        return self._native.type

    @property
    def annotation(self):
        return self._native.annotation

    @property
    def nbytes(self):
        return self._native.nbytes

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        optix_has_type = self.type != ObjectType.unknown and self.type != ObjectType.user
        class_object_type = get_object_type_from_pyoptix_class(value)

        if class_object_type:
            # OPTION 1: value is a known OptiX object like GeometryGroup, Buffer etc.
            # do a preliminary check on type right now so it won't fail in device-compile time
            if optix_has_type and self.type != class_object_type and self.type != ObjectType.object:
                raise TypeError("Variable type is {0}, but {1} was given".format(self.type, type(value)))

            # call the respective set function of the optix type of the variable
            getattr(self._native, OBJECT_TYPE_TO_SET_FUNCTION[class_object_type])(value._native)
            self._value = value

        elif optix_has_type:
            # OPTION 2: OptiX variable has a type but value is not a known OptiX object.
            # Try to form a numpy array from value that is compatible with the variable type.
            try:
                dtype, shape = get_dtype_from_object_type(self.type)

                if dtype is None or shape is None:
                    raise ValueError()

                value = numpy.array(value, dtype=dtype)

                if len(value.shape) == 0:
                    value = value.reshape(1)

                if value.shape != shape:
                    raise TypeError("Array shape does not match to the shape of {0}.".format(self.type))

                self._native.set_from_array(value, self.type)
                self._value = value

            except (ValueError, AttributeError):
                raise TypeError("Variable type is {0}, but {1} was given".format(self.type, type(value)))

        elif isinstance(value, numpy.ndarray) and not optix_has_type:
            # OPTION 3: OptiX variable type is unknown or it is user-type, but the value is a numpy array.
            # Use ndarray's dtype to determine variable type
            if len(value.shape) == 0:
                value = value.reshape(1)

            object_type = get_object_type_from_dtype(value.dtype, value.shape)
            self._native.set_from_array(value, object_type)
            self._value = value

        else:
            # Unknown and user-typed variables can only be assigned an ndarray
            raise TypeError("Cannot recognize the variable type or it's user-type. You can assign a numpy array.")
