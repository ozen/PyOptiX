import numpy
from pyoptix.enums import ObjectType, Format, WrapMode, FilterMode, TextureIndexMode, TextureReadMode, BufferType

OBJECT_TYPE_TO_DTYPE = {
    ObjectType.float: (numpy.float32, 1),
    ObjectType.float2: (numpy.float32, 2),
    ObjectType.float3: (numpy.float32, 3),
    ObjectType.float4: (numpy.float32, 4),

    ObjectType.int: (numpy.int32, 1),
    ObjectType.int2: (numpy.int32, 2),
    ObjectType.int3: (numpy.int32, 3),
    ObjectType.int4: (numpy.int32, 4),

    ObjectType.unsigned_int: (numpy.uint32, 1),
    ObjectType.unsigned_int2: (numpy.uint32, 2),
    ObjectType.unsigned_int3: (numpy.uint32, 3),
    ObjectType.unsigned_int4: (numpy.uint32, 4),
}

DTYPE_TO_OBJECT_TYPE = {
    numpy.dtype(numpy.float32): {
        1: ObjectType.float,
        2: ObjectType.float2,
        3: ObjectType.float3,
        4: ObjectType.float4
    },

    numpy.dtype(numpy.int32): {
        1: ObjectType.int,
        2: ObjectType.int2,
        3: ObjectType.int3,
        4: ObjectType.int4
    },

    numpy.dtype(numpy.uint32): {
        1: ObjectType.unsigned_int,
        2: ObjectType.unsigned_int2,
        3: ObjectType.unsigned_int3,
        4: ObjectType.unsigned_int4
    },

    'default': ObjectType.user,
}

FORMAT_TO_DTYPE = {
    Format.float: (numpy.float32, 1),
    Format.float2: (numpy.float32, 2),
    Format.float3: (numpy.float32, 3),
    Format.float4: (numpy.float32, 4),

    Format.int: (numpy.int32, 1),
    Format.int2: (numpy.int32, 2),
    Format.int3: (numpy.int32, 3),
    Format.int4: (numpy.int32, 4),

    Format.unsigned_int: (numpy.uint32, 1),
    Format.unsigned_int2: (numpy.uint32, 2),
    Format.unsigned_int3: (numpy.uint32, 3),
    Format.unsigned_int4: (numpy.uint32, 4),

    Format.short: (numpy.int16, 1),
    Format.short2: (numpy.int16, 2),
    Format.short3: (numpy.int16, 3),
    Format.short4: (numpy.int16, 4),

    Format.unsigned_short: (numpy.uint16, 1),
    Format.unsigned_short2: (numpy.uint16, 2),
    Format.unsigned_short3: (numpy.uint16, 3),
    Format.unsigned_short4: (numpy.uint16, 4),

    Format.byte: (numpy.int8, 1),
    Format.byte2: (numpy.int8, 2),
    Format.byte3: (numpy.int8, 3),
    Format.byte4: (numpy.int8, 4),

    Format.unsigned_byte: (numpy.uint8, 1),
    Format.unsigned_byte2: (numpy.uint8, 2),
    Format.unsigned_byte3: (numpy.uint8, 3),
    Format.unsigned_byte4: (numpy.uint8, 4),
}

DTYPE_TO_FORMAT = {
    numpy.dtype(numpy.float32): {
        1: Format.float,
        2: Format.float2,
        3: Format.float3,
        4: Format.float4
    },

    numpy.dtype(numpy.int32): {
        1: Format.int,
        2: Format.int2,
        3: Format.int3,
        4: Format.int4
    },

    numpy.dtype(numpy.uint32): {
        1: Format.unsigned_int,
        2: Format.unsigned_int2,
        3: Format.unsigned_int3,
        4: Format.unsigned_int4
    },

    numpy.dtype(numpy.int16): {
        1: Format.short,
        2: Format.short2,
        3: Format.short3,
        4: Format.short4
    },

    numpy.dtype(numpy.uint16): {
        1: Format.unsigned_short,
        2: Format.unsigned_short2,
        3: Format.unsigned_short3,
        4: Format.unsigned_short4
    },

    numpy.dtype(numpy.int8): {
        1: Format.byte,
        2: Format.byte2,
        3: Format.byte3,
        4: Format.byte4
    },

    numpy.dtype(numpy.uint8): {
        1: Format.unsigned_byte,
        2: Format.unsigned_byte2,
        3: Format.unsigned_byte3,
        4: Format.unsigned_byte4
    },

    'default': Format.user
}


PYOPTIX_CLASS_TO_OBJECT_TYPE = {
    'Buffer': ObjectType.buffer,
    'TextureSampler': ObjectType.texture_sampler,
    'Program': ObjectType.program,
    'Group': ObjectType.group,
    'GeometryGroup': ObjectType.geometry_group,
    'GeometryInstance': ObjectType.geometry_instance,
    'Selector': ObjectType.selector,
    'Transform': ObjectType.transform,

    'default': None,
}


WRAP_STRING_TO_OPTIX_ENUM = {
    'repeat': WrapMode.repeat,
    'clamp_to_edge': WrapMode.clamp_to_edge,
    'mirror': WrapMode.mirror,
    'clamp_to_border': WrapMode.clamp_to_border,
}

FILTERING_STRING_TO_OPTIX_ENUM = {
    'nearest': FilterMode.nearest,
    'linear': FilterMode.linear,
    'none': FilterMode.none,
}

READ_STRING_TO_OPTIX_ENUM = {
    'element_type': TextureReadMode.element_type,
    'normalized_float': TextureReadMode.normalized_float,
}

INDEXING_STRING_TO_OPTIX_ENUM = {
    'normalized_coordinates': TextureIndexMode.normalized_coordinates,
    'array_index': TextureIndexMode.array_index,
}

BUFFER_STRING_TO_OPTIX_ENUM = {
    'io': BufferType.input_output,
    'i': BufferType.input,
    'o': BufferType.output,
}


def get_dtype_from_object_type(object_type):
    if object_type in OBJECT_TYPE_TO_DTYPE:
        return OBJECT_TYPE_TO_DTYPE[object_type]
    else:
        return None, None


def get_object_type_from_dtype(dtype, type_size):
    if dtype in DTYPE_TO_OBJECT_TYPE and type_size in DTYPE_TO_OBJECT_TYPE[dtype]:
        return DTYPE_TO_OBJECT_TYPE[dtype][type_size]
    else:
        return DTYPE_TO_OBJECT_TYPE['default']


def get_format_from_dtype(dtype, type_size):
    if dtype in DTYPE_TO_FORMAT and type_size in DTYPE_TO_FORMAT[dtype]:
        return DTYPE_TO_FORMAT[dtype][type_size]
    else:
        return DTYPE_TO_FORMAT['default']


def get_object_type_from_pyoptix_class(instance):
    try:
        if instance.__class__.__name__ in PYOPTIX_CLASS_TO_OBJECT_TYPE:
            return PYOPTIX_CLASS_TO_OBJECT_TYPE[instance.__class__.__name__]
        else:
            for base in instance.__class__.__bases__:
                if base.__name__ in PYOPTIX_CLASS_TO_OBJECT_TYPE:
                    return PYOPTIX_CLASS_TO_OBJECT_TYPE[base.__name__]
            return PYOPTIX_CLASS_TO_OBJECT_TYPE['default']
    except Exception:
        return None


def convert_wrap_mode(string):
    if isinstance(string, str) and string.lower() in WRAP_STRING_TO_OPTIX_ENUM:
        return WRAP_STRING_TO_OPTIX_ENUM[string]
    else:
        return string


def convert_filtering_mode(string):
    if isinstance(string, str) and string.lower() in FILTERING_STRING_TO_OPTIX_ENUM:
        return FILTERING_STRING_TO_OPTIX_ENUM[string]
    else:
        return string


def convert_read_mode(string):
    if isinstance(string, str) and string.lower() in READ_STRING_TO_OPTIX_ENUM:
        return READ_STRING_TO_OPTIX_ENUM[string]
    else:
        return string


def convert_indexing_mode(string):
    if isinstance(string, str) and string.lower() in INDEXING_STRING_TO_OPTIX_ENUM:
        return INDEXING_STRING_TO_OPTIX_ENUM[string]
    else:
        return string


def convert_buffer_type(string):
    if isinstance(string, str) and string.lower() in BUFFER_STRING_TO_OPTIX_ENUM:
        return BUFFER_STRING_TO_OPTIX_ENUM[string]
    else:
        raise string
