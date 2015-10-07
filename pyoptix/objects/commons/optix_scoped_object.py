import numpy
from pyoptix._driver import RTobjecttype


dict_for_optix_to_numpy_one_dtype = {
    0: None,

    RTobjecttype.RT_OBJECTTYPE_FLOAT: (numpy.float32, 1),
    RTobjecttype.RT_OBJECTTYPE_FLOAT2: (numpy.float32, 2),
    RTobjecttype.RT_OBJECTTYPE_FLOAT3: (numpy.float32, 3),
    RTobjecttype.RT_OBJECTTYPE_FLOAT4: (numpy.float32, 4),

    RTobjecttype.RT_OBJECTTYPE_INT: (numpy.int32, 1),
    RTobjecttype.RT_OBJECTTYPE_INT2: (numpy.int32, 2),
    RTobjecttype.RT_OBJECTTYPE_INT3: (numpy.int32, 3),
    RTobjecttype.RT_OBJECTTYPE_INT4: (numpy.int32, 4),

    RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT: (numpy.uint32, 1),
    RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT2: (numpy.uint32, 2),
    RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT3: (numpy.uint32, 3),
    RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT4: (numpy.uint32, 4),
}


dict_for_numpy_to_optix = {
    0: None,

    numpy.float32: {
        1: RTobjecttype.RT_OBJECTTYPE_FLOAT,
        2: RTobjecttype.RT_OBJECTTYPE_FLOAT2,
        3: RTobjecttype.RT_OBJECTTYPE_FLOAT3,
        4: RTobjecttype.RT_OBJECTTYPE_FLOAT4
    },

    numpy.int32: {
        1: RTobjecttype.RT_OBJECTTYPE_INT,
        2: RTobjecttype.RT_OBJECTTYPE_INT2,
        3: RTobjecttype.RT_OBJECTTYPE_INT3,
        4: RTobjecttype.RT_OBJECTTYPE_INT4
    },

    numpy.uint32: {
        1: RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT,
        2: RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT2,
        3: RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT3,
        4: RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT4
    },
}


class OptixScopedObject(object):
    def __init__(self):
        self._variables = dict()

    def __setitem__(self, key, value):
        # Optix interface
        optix_variable = self._query_variable(key)
        if not optix_variable.is_valid():
            optix_variable = self._declare_variable(key)

        # first take type from optix
        value_type = optix_variable.type
        is_optix_given_type = False

        if value_type is not RTobjecttype.RT_OBJECTTYPE_UNKNOWN and value_type is not RTobjecttype.RT_OBJECTTYPE_USER:
            is_optix_given_type = True

        from pyoptix.objects.optix_buffer import OptixBuffer
        from pyoptix.objects.optix_texture_sampler import OptixTextureSampler
        from pyoptix.objects.optix_program import OptixProgram
        from pyoptix.objects.optix_group import OptixGroup
        from pyoptix.objects.optix_geometry_group import OptixGeometryGroup
        from pyoptix.objects.optix_selector import OptixSelector
        from pyoptix.objects.optix_transform import OptixTransform

        if isinstance(value, OptixBuffer):
            if is_optix_given_type and value_type is not RTobjecttype.RT_OBJECTTYPE_BUFFER:
                raise ValueError("Optix type is " + str(optix_variable) + " but you give buffer")
            optix_variable._set_buffer(value)

        elif isinstance(value, OptixTextureSampler):
            if is_optix_given_type and value_type is not RTobjecttype.RT_OBJECTTYPE_TEXTURE_SAMPLER:
                raise ValueError("Optix type is " + str(optix_variable) + " but you give texture")
            optix_variable._set_texture(value)

        elif isinstance(value, OptixProgram):
            if is_optix_given_type and value_type is not RTobjecttype.RT_OBJECTTYPE_PROGRAM:
                raise ValueError("Optix type is " + str(optix_variable) + " but you give program")
            optix_variable._set_program_id_with_program(value)

        elif isinstance(value, OptixGroup):
            if is_optix_given_type and value_type is not RTobjecttype.RT_OBJECTTYPE_GROUP:
                raise ValueError("Optix type is " + str(optix_variable) + " but you give group")
            optix_variable._set_group(value)

        elif isinstance(value, OptixGeometryGroup):
            if is_optix_given_type and value_type is not RTobjecttype.RT_OBJECTTYPE_GEOMETRY_GROUP:
                raise ValueError("Optix type is " + str(optix_variable) + " but you give geometry group")
            optix_variable._set_geometry_group(value)

        elif isinstance(value, OptixSelector):
            if is_optix_given_type and value_type is not RTobjecttype.RT_OBJECTTYPE_SELECTOR:
                raise ValueError("Optix type is " + str(optix_variable) + " but you give selector")
            optix_variable._set_selector(value)

        elif isinstance(value, OptixTransform):
            if is_optix_given_type and value_type is not RTobjecttype.RT_OBJECTTYPE_TRANSFORM:
                raise ValueError("Optix type is " + str(optix_variable) + " but you give transform")
            optix_variable._set_transform(value)

        elif is_optix_given_type:
            # OK we have optix type so we try to convert value into optix_type
            value_numpy_array = numpy.array(value)

            if len(value_numpy_array.shape) == 0:
                value_numpy_array = value_numpy_array.reshape((1))

            numpy_type_and_dim_from_optix = dict_for_optix_to_numpy_one_dtype[value_type]

            if numpy_type_and_dim_from_optix is None:
                return NotImplementedError("Not implemented for optix type " + str(value_type))

            if len(value_numpy_array.shape) != 1:
                return ValueError("Optix accept only one dim input for " + str(value_type))

            if value_numpy_array.shape[0] is not numpy_type_and_dim_from_optix[1]:
                return ValueError("Optix wants " + str(numpy_type_and_dim_from_optix[1]) + " dim but you give : " + str(value_numpy_array.shape[0]))

            value_numpy_array = value_numpy_array.astype(numpy_type_and_dim_from_optix[0])
            value = value_numpy_array

            optix_variable._set_variable_with_type(value, value_type)

        elif isinstance(value, numpy.ndarray):
            value_numpy_array = value
            if len(value_numpy_array.shape) == 0:
                value_numpy_array = value_numpy_array.reshape((1))
            optix_variable._set_with_numpy_array1x1_dtype(value_numpy_array)

        else:
            raise NotImplementedError("Optix can not recognize the type, you should give a numpy array.")
        """
        else:
            self._remove_variable(optix_variable)
            raise ValueError(str(type(value)) + "can not assign to OptixScopedObject")
        """

        # Python interface
        self._variables[key] = value

    def __getitem__(self, key):
        return self._variables[key]

    def __len__(self):
        return len(self._variables)

    def __delitem__(self, key):
        optix_variable = self._query_variable(key)
        if not optix_variable.is_valid():
            raise IndexError("there is no key like : " + str(key))

        self._remove_variable(optix_variable)
        del self._variables[key]

    def __contains__(self, item):
        return item in self._variables

    def __iter__(self):
        return iter(self._variables)

    def get_variables(self):
        return self._variables
