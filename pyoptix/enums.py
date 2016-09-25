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


class Exception:
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
