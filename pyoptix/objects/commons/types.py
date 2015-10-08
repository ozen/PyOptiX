from pyoptix._driver import RTobjecttype, RTformat
import numpy


OBJECT_TYPE_TO_DTYPE = {
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


DTYPE_TO_OBJECT_TYPE = {
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


FORMAT_TO_DTYPE = {
    RTformat.RT_FORMAT_FLOAT: (numpy.float32, 1),
    RTformat.RT_FORMAT_FLOAT2: (numpy.float32, 2),
    RTformat.RT_FORMAT_FLOAT3: (numpy.float32, 3),
    RTformat.RT_FORMAT_FLOAT4: (numpy.float32, 4),

    RTformat.RT_FORMAT_INT: (numpy.int32, 1),
    RTformat.RT_FORMAT_INT2: (numpy.int32, 2),
    RTformat.RT_FORMAT_INT3: (numpy.int32, 3),
    RTformat.RT_FORMAT_INT4: (numpy.int32, 4),

    RTformat.RT_FORMAT_UNSIGNED_INT: (numpy.uint32, 1),
    RTformat.RT_FORMAT_UNSIGNED_INT2: (numpy.uint32, 2),
    RTformat.RT_FORMAT_UNSIGNED_INT3: (numpy.uint32, 3),
    RTformat.RT_FORMAT_UNSIGNED_INT4: (numpy.uint32, 4),

    RTformat.RT_FORMAT_SHORT: (numpy.int16, 1),
    RTformat.RT_FORMAT_SHORT2: (numpy.int16, 2),
    RTformat.RT_FORMAT_SHORT3: (numpy.int16, 3),
    RTformat.RT_FORMAT_SHORT4: (numpy.int16, 4),

    RTformat.RT_FORMAT_UNSIGNED_SHORT: (numpy.uint16, 1),
    RTformat.RT_FORMAT_UNSIGNED_SHORT2: (numpy.uint16, 2),
    RTformat.RT_FORMAT_UNSIGNED_SHORT3: (numpy.uint16, 3),
    RTformat.RT_FORMAT_UNSIGNED_SHORT4: (numpy.uint16, 4),

    RTformat.RT_FORMAT_BYTE: (numpy.int8, 1),
    RTformat.RT_FORMAT_BYTE2: (numpy.int8, 2),
    RTformat.RT_FORMAT_BYTE3: (numpy.int8, 3),
    RTformat.RT_FORMAT_BYTE4: (numpy.int8, 4),

    RTformat.RT_FORMAT_UNSIGNED_BYTE: (numpy.uint8, 1),
    RTformat.RT_FORMAT_UNSIGNED_BYTE2: (numpy.uint8, 2),
    RTformat.RT_FORMAT_UNSIGNED_BYTE3: (numpy.uint8, 3),
    RTformat.RT_FORMAT_UNSIGNED_BYTE4: (numpy.uint8, 4),
}


DTYPE_TO_FORMAT = {
    numpy.dtype(numpy.float32): {
        1: RTformat.RT_FORMAT_FLOAT,
        2: RTformat.RT_FORMAT_FLOAT2,
        3: RTformat.RT_FORMAT_FLOAT3,
        4: RTformat.RT_FORMAT_FLOAT4
    },

    numpy.dtype(numpy.int32): {
        1: RTformat.RT_FORMAT_INT,
        2: RTformat.RT_FORMAT_INT2,
        3: RTformat.RT_FORMAT_INT3,
        4: RTformat.RT_FORMAT_INT4
    },

    numpy.dtype(numpy.uint32): {
        1: RTformat.RT_FORMAT_UNSIGNED_INT,
        2: RTformat.RT_FORMAT_UNSIGNED_INT2,
        3: RTformat.RT_FORMAT_UNSIGNED_INT3,
        4: RTformat.RT_FORMAT_UNSIGNED_INT4
    },

    numpy.dtype(numpy.int16): {
        1: RTformat.RT_FORMAT_SHORT,
        2: RTformat.RT_FORMAT_SHORT2,
        3: RTformat.RT_FORMAT_SHORT3,
        4: RTformat.RT_FORMAT_SHORT4
    },

    numpy.dtype(numpy.uint16): {
        1: RTformat.RT_FORMAT_UNSIGNED_SHORT,
        2: RTformat.RT_FORMAT_UNSIGNED_SHORT2,
        3: RTformat.RT_FORMAT_UNSIGNED_SHORT3,
        4: RTformat.RT_FORMAT_UNSIGNED_SHORT4
    },

    numpy.dtype(numpy.int8): {
        1: RTformat.RT_FORMAT_BYTE,
        2: RTformat.RT_FORMAT_BYTE2,
        3: RTformat.RT_FORMAT_BYTE3,
        4: RTformat.RT_FORMAT_BYTE4
    },

    numpy.dtype(numpy.uint8): {
        1: RTformat.RT_FORMAT_UNSIGNED_BYTE,
        2: RTformat.RT_FORMAT_UNSIGNED_BYTE2,
        3: RTformat.RT_FORMAT_UNSIGNED_BYTE3,
        4: RTformat.RT_FORMAT_UNSIGNED_BYTE4
    },

    'default': RTformat.RT_FORMAT_USER
}


def get_format_from_dtype(dtype, type_size):
    if dtype in DTYPE_TO_FORMAT and type_size in DTYPE_TO_FORMAT[dtype]:
        return DTYPE_TO_FORMAT[dtype][type_size]
    else:
        return DTYPE_TO_FORMAT['default']
