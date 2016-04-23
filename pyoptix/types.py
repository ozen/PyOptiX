from pyoptix._driver import RTobjecttype, RTformat, RTfiltermode, RTwrapmode, RTtexturereadmode, RTtextureindexmode
import numpy


OBJECT_TYPE_TO_DTYPE = {
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
    numpy.dtype(numpy.float32): {
        1: RTobjecttype.RT_OBJECTTYPE_FLOAT,
        2: RTobjecttype.RT_OBJECTTYPE_FLOAT2,
        3: RTobjecttype.RT_OBJECTTYPE_FLOAT3,
        4: RTobjecttype.RT_OBJECTTYPE_FLOAT4
    },

    numpy.dtype(numpy.int32): {
        1: RTobjecttype.RT_OBJECTTYPE_INT,
        2: RTobjecttype.RT_OBJECTTYPE_INT2,
        3: RTobjecttype.RT_OBJECTTYPE_INT3,
        4: RTobjecttype.RT_OBJECTTYPE_INT4
    },

    numpy.dtype(numpy.uint32): {
        1: RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT,
        2: RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT2,
        3: RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT3,
        4: RTobjecttype.RT_OBJECTTYPE_UNSIGNED_INT4
    },

    'default': RTobjecttype.RT_OBJECTTYPE_USER,
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


OBJECT_TYPE_TO_PYOPTIX_CLASS = {
    RTobjecttype.RT_OBJECTTYPE_BUFFER: 'OptixBuffer',
    RTobjecttype.RT_OBJECTTYPE_TEXTURE_SAMPLER: 'OptixTextureSampler',
    RTobjecttype.RT_OBJECTTYPE_PROGRAM: 'OptixProgram',
    RTobjecttype.RT_OBJECTTYPE_GROUP: 'OptixGroup',
    RTobjecttype.RT_OBJECTTYPE_GEOMETRY_GROUP: 'OptixGeometryGroup',
    RTobjecttype.RT_OBJECTTYPE_SELECTOR: 'OptixSelector',
    RTobjecttype.RT_OBJECTTYPE_TRANSFORM: 'OptixTransform',

    'default': None,
}

PYOPTIX_CLASS_TO_OBJECT_TYPE = {
    'OptixBuffer': RTobjecttype.RT_OBJECTTYPE_BUFFER,
    'OptixTextureSampler': RTobjecttype.RT_OBJECTTYPE_TEXTURE_SAMPLER,
    'OptixProgram': RTobjecttype.RT_OBJECTTYPE_PROGRAM,
    'OptixGroup': RTobjecttype.RT_OBJECTTYPE_GROUP,
    'OptixGeometryGroup': RTobjecttype.RT_OBJECTTYPE_GEOMETRY_GROUP,
    'OptixSelector': RTobjecttype.RT_OBJECTTYPE_SELECTOR,
    'OptixTransform': RTobjecttype.RT_OBJECTTYPE_TRANSFORM,

    'default': None,
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


def get_pyoptix_class_by_name(class_name):
    from pyoptix.objects.buffer import BufferObj
    from pyoptix.objects.texture_sampler import TextureSamplerObj
    from pyoptix.objects.program import ProgramObj
    from pyoptix.objects.group import GroupObj
    from pyoptix.objects.geometry_group import GeometryGroupObj
    from pyoptix.objects.selector import SelectorObj
    from pyoptix.objects.transform import TransformObj
    try:
        return locals()[class_name]
    except KeyError:
        return None


def get_pyoptix_class_from_object_type(object_type):
    if object_type in OBJECT_TYPE_TO_PYOPTIX_CLASS:
        class_name = OBJECT_TYPE_TO_PYOPTIX_CLASS[object_type]
    else:
        class_name = OBJECT_TYPE_TO_PYOPTIX_CLASS['default']
    return get_pyoptix_class_by_name(class_name)


def get_object_type_from_pyoptix_class(instance):
    try:
        name = instance.__class__.__name__
        if name in PYOPTIX_CLASS_TO_OBJECT_TYPE:
            return PYOPTIX_CLASS_TO_OBJECT_TYPE[name]
        else:
            return PYOPTIX_CLASS_TO_OBJECT_TYPE['default']
    except Exception:
        return None

WRAP_STRING_TO_OPTIX_ENUM = {
    'repeat': RTwrapmode.RT_WRAP_REPEAT,
    'clamp': RTwrapmode.RT_WRAP_CLAMP_TO_EDGE,
    'mirror': RTwrapmode.RT_WRAP_MIRROR,
    'clamp_to_border': RTwrapmode.RT_WRAP_CLAMP_TO_BORDER,
}

FILTERING_STRING_TO_OPTIX_ENUM = {
    'nearest': RTfiltermode.RT_FILTER_NEAREST,
    'linear': RTfiltermode.RT_FILTER_LINEAR,
    'none': RTfiltermode.RT_FILTER_NONE,
}

READ_STRING_TO_OPTIX_ENUM = {
    'element': RTtexturereadmode.RT_TEXTURE_READ_ELEMENT_TYPE,
    'normalized_float': RTtexturereadmode.RT_TEXTURE_READ_NORMALIZED_FLOAT,
}

INDEXING_STRING_TO_OPTIX_ENUM = {
    'normalized': RTtextureindexmode.RT_TEXTURE_INDEX_NORMALIZED_COORDINATES,
    'index': RTtextureindexmode.RT_TEXTURE_INDEX_ARRAY_INDEX,
}


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
