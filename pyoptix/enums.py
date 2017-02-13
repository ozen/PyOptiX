import numpy
from pyoptix._driver import RTobjecttype, RTformat, RTfiltermode, RTwrapmode, RTtexturereadmode, \
    RTtextureindexmode, RTbuffertype, RTbufferflag, RTexception


class Format:
    unknown = RTformat.RT_FORMAT_UNKNOWN
    float = RTformat.RT_FORMAT_FLOAT
    float2 = RTformat.RT_FORMAT_FLOAT2
    float3 = RTformat.RT_FORMAT_FLOAT3
    float4 = RTformat.RT_FORMAT_FLOAT4
    byte = RTformat.RT_FORMAT_BYTE
    byte2 = RTformat.RT_FORMAT_BYTE2
    byte3 = RTformat.RT_FORMAT_BYTE3
    byte4 = RTformat.RT_FORMAT_BYTE4
    unsigned_byte = RTformat.RT_FORMAT_UNSIGNED_BYTE
    unsigned_byte2 = RTformat.RT_FORMAT_UNSIGNED_BYTE2
    unsigned_byte3 = RTformat.RT_FORMAT_UNSIGNED_BYTE3
    unsigned_byte4 = RTformat.RT_FORMAT_UNSIGNED_BYTE4
    short = RTformat.RT_FORMAT_SHORT
    short2 = RTformat.RT_FORMAT_SHORT2
    short3 = RTformat.RT_FORMAT_SHORT3
    short4 = RTformat.RT_FORMAT_SHORT4
    unsigned_short = RTformat.RT_FORMAT_UNSIGNED_SHORT
    unsigned_short2 = RTformat.RT_FORMAT_UNSIGNED_SHORT2
    unsigned_short3 = RTformat.RT_FORMAT_UNSIGNED_SHORT3
    unsigned_short4 = RTformat.RT_FORMAT_UNSIGNED_SHORT4
    int = RTformat.RT_FORMAT_INT
    int2 = RTformat.RT_FORMAT_INT2
    int3 = RTformat.RT_FORMAT_INT3
    int4 = RTformat.RT_FORMAT_INT4
    unsigned_int = RTformat.RT_FORMAT_UNSIGNED_INT
    unsigned_int2 = RTformat.RT_FORMAT_UNSIGNED_INT2
    unsigned_int3 = RTformat.RT_FORMAT_UNSIGNED_INT3
    unsigned_int4 = RTformat.RT_FORMAT_UNSIGNED_INT4
    user = RTformat.RT_FORMAT_USER
    buffer_id = RTformat.RT_FORMAT_BUFFER_ID
    program_id = RTformat.RT_FORMAT_PROGRAM_ID


class BufferType:
    input = RTbuffertype.RT_BUFFER_INPUT
    output = RTbuffertype.RT_BUFFER_OUTPUT
    input_output = RTbuffertype.RT_BUFFER_INPUT_OUTPUT


class BufferFlag:
    gpu_local = RTbufferflag.RT_BUFFER_GPU_LOCAL
    copy_on_dirty = RTbufferflag.RT_BUFFER_COPY_ON_DIRTY


class WrapMode:
    repeat = RTwrapmode.RT_WRAP_REPEAT
    clamp_to_edge = RTwrapmode.RT_WRAP_CLAMP_TO_EDGE
    mirror = RTwrapmode.RT_WRAP_MIRROR
    clamp_to_border = RTwrapmode.RT_WRAP_CLAMP_TO_BORDER


class FilterMode:
    nearest = RTfiltermode.RT_FILTER_NEAREST
    linear = RTfiltermode.RT_FILTER_LINEAR
    none = RTfiltermode.RT_FILTER_NONE


class TextureReadMode:
    element_type = RTtexturereadmode.RT_TEXTURE_READ_ELEMENT_TYPE
    normalized_float = RTtexturereadmode.RT_TEXTURE_READ_NORMALIZED_FLOAT


class TextureIndexMode:
    normalized_coordinates = RTtextureindexmode.RT_TEXTURE_INDEX_NORMALIZED_COORDINATES
    array_index = RTtextureindexmode.RT_TEXTURE_INDEX_ARRAY_INDEX


class ExceptionType:
    program_id_invalid = RTexception.RT_EXCEPTION_PROGRAM_ID_INVALID
    texture_id_invalid = RTexception.RT_EXCEPTION_TEXTURE_ID_INVALID
    buffer_id_invalid = RTexception.RT_EXCEPTION_BUFFER_ID_INVALID
    index_out_of_bounds = RTexception.RT_EXCEPTION_INDEX_OUT_OF_BOUNDS
    stack_overflow = RTexception.RT_EXCEPTION_STACK_OVERFLOW
    buffer_index_out_of_bounds = RTexception.RT_EXCEPTION_BUFFER_INDEX_OUT_OF_BOUNDS
    invalid_ray = RTexception.RT_EXCEPTION_INVALID_RAY
    internal_error = RTexception.RT_EXCEPTION_INTERNAL_ERROR
    user = RTexception.RT_EXCEPTION_USER
    all = RTexception.RT_EXCEPTION_ALL


class ObjectType:
    unknown = RTobjecttype.RT_OBJECTTYPE_UNKNOWN
    group = RTobjecttype.RT_OBJECTTYPE_GROUP
    geometry_group = RTobjecttype.RT_OBJECTTYPE_GEOMETRY_GROUP
    transform = RTobjecttype.RT_OBJECTTYPE_TRANSFORM
    selector = RTobjecttype.RT_OBJECTTYPE_SELECTOR
    geometry_instance = RTobjecttype.RT_OBJECTTYPE_GEOMETRY_INSTANCE
    buffer = RTobjecttype.RT_OBJECTTYPE_BUFFER
    texture_sampler = RTobjecttype.RT_OBJECTTYPE_TEXTURE_SAMPLER
    object = RTobjecttype.RT_OBJECTTYPE_OBJECT
    matrix2x2 = RTobjecttype.RT_OBJECTTYPE_MATRIX_FLOAT2x2
    matrix2x3 = RTobjecttype.RT_OBJECTTYPE_MATRIX_FLOAT2x3
    matrix2x4 = RTobjecttype.RT_OBJECTTYPE_MATRIX_FLOAT2x4
    matrix3x2 = RTobjecttype.RT_OBJECTTYPE_MATRIX_FLOAT3x2
    matrix3x3 = RTobjecttype.RT_OBJECTTYPE_MATRIX_FLOAT3x3
    matrix3x4 = RTobjecttype.RT_OBJECTTYPE_MATRIX_FLOAT3x4
    matrix4x2 = RTobjecttype.RT_OBJECTTYPE_MATRIX_FLOAT4x2
    matrix4x3 = RTobjecttype.RT_OBJECTTYPE_MATRIX_FLOAT4x3
    matrix4x4 = RTobjecttype.RT_OBJECTTYPE_MATRIX_FLOAT4x4
    float = RTobjecttype.RT_OBJECTTYPE_FLOAT
    float2 = RTobjecttype.RT_OBJECTTYPE_FLOAT2
    float3 = RTobjecttype.RT_OBJECTTYPE_FLOAT3
    float4 = RTobjecttype.RT_OBJECTTYPE_FLOAT4
    int = RTobjecttype.RT_OBJECTTYPE_INT
    int2 = RTobjecttype.RT_OBJECTTYPE_INT2
    int3 = RTobjecttype.RT_OBJECTTYPE_INT3
    int4 = RTobjecttype.RT_OBJECTTYPE_INT4
    unsigned_int = RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT
    unsigned_int2 = RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT2
    unsigned_int3 = RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT3
    unsigned_int4 = RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT4
    user = RTobjecttype.RT_OBJECTTYPE_USER
    program = RTobjecttype.RT_OBJECTTYPE_PROGRAM

OBJECT_TYPE_TO_DTYPE_SHAPE = {
    ObjectType.float: (numpy.float32, (1, )),
    ObjectType.float2: (numpy.float32, (2, )),
    ObjectType.float3: (numpy.float32, (3, )),
    ObjectType.float4: (numpy.float32, (4, )),

    ObjectType.int: (numpy.int32, (1, )),
    ObjectType.int2: (numpy.int32, (2, )),
    ObjectType.int3: (numpy.int32, (3, )),
    ObjectType.int4: (numpy.int32, (4, )),

    ObjectType.unsigned_int: (numpy.uint32, (1, )),
    ObjectType.unsigned_int2: (numpy.uint32, (2, )),
    ObjectType.unsigned_int3: (numpy.uint32, (3, )),
    ObjectType.unsigned_int4: (numpy.uint32, (4, )),

    ObjectType.matrix2x2: (numpy.float32, (2, 2)),
    ObjectType.matrix2x3: (numpy.float32, (2, 3)),
    ObjectType.matrix2x4: (numpy.float32, (2, 4)),
    ObjectType.matrix3x2: (numpy.float32, (3, 2)),
    ObjectType.matrix3x3: (numpy.float32, (3, 3)),
    ObjectType.matrix3x4: (numpy.float32, (3, 4)),
    ObjectType.matrix4x2: (numpy.float32, (4, 2)),
    ObjectType.matrix4x3: (numpy.float32, (4, 3)),
    ObjectType.matrix4x4: (numpy.float32, (4, 4)),
}

DTYPE_SHAPE_TO_OBJECT_TYPE = {
    numpy.dtype(numpy.float32): {
        (1, ): ObjectType.float,
        (2, ): ObjectType.float2,
        (3, ): ObjectType.float3,
        (4, ): ObjectType.float4,

        (2, 2): ObjectType.matrix2x2,
        (2, 3): ObjectType.matrix2x3,
        (2, 4): ObjectType.matrix2x4,
        (3, 2): ObjectType.matrix3x2,
        (3, 3): ObjectType.matrix3x3,
        (3, 4): ObjectType.matrix3x4,
        (4, 2): ObjectType.matrix4x2,
        (4, 3): ObjectType.matrix4x3,
        (4, 4): ObjectType.matrix4x4,
    },

    numpy.dtype(numpy.int32): {
        (1, ): ObjectType.int,
        (2, ): ObjectType.int2,
        (3, ): ObjectType.int3,
        (4, ): ObjectType.int4,
    },

    numpy.dtype(numpy.uint32): {
        (1, ): ObjectType.unsigned_int,
        (2, ): ObjectType.unsigned_int2,
        (3, ): ObjectType.unsigned_int3,
        (4, ): ObjectType.unsigned_int4,
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
    if object_type in OBJECT_TYPE_TO_DTYPE_SHAPE:
        return OBJECT_TYPE_TO_DTYPE_SHAPE[object_type]
    else:
        return None, None


def get_object_type_from_dtype(dtype, shape):
    if dtype in DTYPE_SHAPE_TO_OBJECT_TYPE and shape in DTYPE_SHAPE_TO_OBJECT_TYPE[dtype]:
        return DTYPE_SHAPE_TO_OBJECT_TYPE[dtype][shape]
    else:
        return DTYPE_SHAPE_TO_OBJECT_TYPE['default']


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
