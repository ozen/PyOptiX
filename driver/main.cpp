#include "shared_includes.h"
#include "destroyable.h"
#include "variable.h"
#include "scoped.h"
#include "program.h"
#include "acceleration.h"
#include "context.h"
#include "buffer.h"
#include "texture_sampler.h"
#include "geometry.h"
#include "material.h"
#include "selector.h"
#include "transform.h"
#include "geometry_group.h"
#include "group.h"
#include "geometry_instance.h"


BOOST_PYTHON_MODULE(_driver)
{
    Py_Initialize();
    boost::numpy::initialize();

    /*
    *   CORE
    */
    boost::python::scope().attr("OPTIX_VERSION") = OPTIX_VERSION;
    NativeDestroyableWrapper::export_for_python();
    NativeVariableWrapper::export_for_python();
    NativeScopedWrapper::export_for_python();
    NativeProgramWrapper::export_for_python();
    NativeContextWrapper::export_for_python();
    NativeAccelerationWrapper::export_for_python();
    NativeBufferWrapper::export_for_python();
    NativeTextureSamplerWrapper::export_for_python();
    NativeGeometryWrapper::export_for_python();
    NativeMaterialWrapper::export_for_python();
    NativeSelectorWrapper::export_for_python();
    NativeTransformWrapper::export_for_python();
    NativeGeometryGroupWrapper::export_for_python();
    NativeGroupWrapper::export_for_python();
    NativeGeometryInstanceWrapper::export_for_python();

    /*
    *   ENUMs
    */
    boost::python::enum_<RTformat>("RTformat")
        .value("RT_FORMAT_UNKNOWN", RT_FORMAT_UNKNOWN)
        .value("RT_FORMAT_FLOAT", RT_FORMAT_FLOAT)
        .value("RT_FORMAT_FLOAT2", RT_FORMAT_FLOAT2)
        .value("RT_FORMAT_FLOAT3", RT_FORMAT_FLOAT3)
        .value("RT_FORMAT_FLOAT4", RT_FORMAT_FLOAT4)
        .value("RT_FORMAT_BYTE", RT_FORMAT_BYTE)
        .value("RT_FORMAT_BYTE2", RT_FORMAT_BYTE2)
        .value("RT_FORMAT_BYTE3", RT_FORMAT_BYTE3)
        .value("RT_FORMAT_BYTE4", RT_FORMAT_BYTE4)
        .value("RT_FORMAT_UNSIGNED_BYTE", RT_FORMAT_UNSIGNED_BYTE)
        .value("RT_FORMAT_UNSIGNED_BYTE2", RT_FORMAT_UNSIGNED_BYTE2)
        .value("RT_FORMAT_UNSIGNED_BYTE3", RT_FORMAT_UNSIGNED_BYTE3)
        .value("RT_FORMAT_UNSIGNED_BYTE4", RT_FORMAT_UNSIGNED_BYTE4)
        .value("RT_FORMAT_SHORT", RT_FORMAT_SHORT)
        .value("RT_FORMAT_SHORT2", RT_FORMAT_SHORT2)
        .value("RT_FORMAT_SHORT3", RT_FORMAT_SHORT3)
        .value("RT_FORMAT_SHORT4", RT_FORMAT_SHORT4)
        .value("RT_FORMAT_UNSIGNED_SHORT", RT_FORMAT_UNSIGNED_SHORT)
        .value("RT_FORMAT_UNSIGNED_SHORT2", RT_FORMAT_UNSIGNED_SHORT2)
        .value("RT_FORMAT_UNSIGNED_SHORT3", RT_FORMAT_UNSIGNED_SHORT3)
        .value("RT_FORMAT_UNSIGNED_SHORT4", RT_FORMAT_UNSIGNED_SHORT4)
        .value("RT_FORMAT_INT", RT_FORMAT_INT)
        .value("RT_FORMAT_INT2", RT_FORMAT_INT2)
        .value("RT_FORMAT_INT3", RT_FORMAT_INT3)
        .value("RT_FORMAT_INT4", RT_FORMAT_INT4)
        .value("RT_FORMAT_UNSIGNED_INT", RT_FORMAT_UNSIGNED_INT)
        .value("RT_FORMAT_UNSIGNED_INT2", RT_FORMAT_UNSIGNED_INT2)
        .value("RT_FORMAT_UNSIGNED_INT3", RT_FORMAT_UNSIGNED_INT3)
        .value("RT_FORMAT_UNSIGNED_INT4", RT_FORMAT_UNSIGNED_INT4)
        .value("RT_FORMAT_USER", RT_FORMAT_USER)
        .value("RT_FORMAT_BUFFER_ID", RT_FORMAT_BUFFER_ID)
        .value("RT_FORMAT_PROGRAM_ID", RT_FORMAT_PROGRAM_ID);

    boost::python::enum_<RTbuffertype>("RTbuffertype")
        .value("RT_BUFFER_INPUT", RT_BUFFER_INPUT)
        .value("RT_BUFFER_OUTPUT", RT_BUFFER_OUTPUT)
        .value("RT_BUFFER_INPUT_OUTPUT", RT_BUFFER_INPUT_OUTPUT);

    boost::python::enum_<RTbufferflag>("RTbufferflag")
        .value("RT_BUFFER_GPU_LOCAL", RT_BUFFER_GPU_LOCAL)
        .value("RT_BUFFER_COPY_ON_DIRTY", RT_BUFFER_COPY_ON_DIRTY);

    boost::python::enum_<RTwrapmode>("RTwrapmode")
        .value("RT_WRAP_REPEAT", RT_WRAP_REPEAT)
        .value("RT_WRAP_CLAMP_TO_EDGE", RT_WRAP_CLAMP_TO_EDGE)
        .value("RT_WRAP_MIRROR", RT_WRAP_MIRROR)
        .value("RT_WRAP_CLAMP_TO_BORDER", RT_WRAP_CLAMP_TO_BORDER);

    boost::python::enum_<RTfiltermode>("RTfiltermode")
        .value("RT_FILTER_NEAREST", RT_FILTER_NEAREST)
        .value("RT_FILTER_LINEAR", RT_FILTER_LINEAR)
        .value("RT_FILTER_NONE", RT_FILTER_NONE);

    boost::python::enum_<RTtexturereadmode>("RTtexturereadmode")
        .value("RT_TEXTURE_READ_ELEMENT_TYPE", RT_TEXTURE_READ_ELEMENT_TYPE)
        .value("RT_TEXTURE_READ_NORMALIZED_FLOAT", RT_TEXTURE_READ_NORMALIZED_FLOAT);

    boost::python::enum_<RTtextureindexmode>("RTtextureindexmode")
        .value("RT_TEXTURE_INDEX_NORMALIZED_COORDINATES", RT_TEXTURE_INDEX_NORMALIZED_COORDINATES)
        .value("RT_TEXTURE_INDEX_ARRAY_INDEX", RT_TEXTURE_INDEX_ARRAY_INDEX);

    boost::python::enum_<RTexception>("RTexception")
        .value("RT_EXCEPTION_PROGRAM_ID_INVALID", RT_EXCEPTION_PROGRAM_ID_INVALID)
        .value("RT_EXCEPTION_TEXTURE_ID_INVALID", RT_EXCEPTION_TEXTURE_ID_INVALID)
        .value("RT_EXCEPTION_BUFFER_ID_INVALID", RT_EXCEPTION_BUFFER_ID_INVALID)
        .value("RT_EXCEPTION_INDEX_OUT_OF_BOUNDS", RT_EXCEPTION_INDEX_OUT_OF_BOUNDS)
        .value("RT_EXCEPTION_STACK_OVERFLOW", RT_EXCEPTION_STACK_OVERFLOW)
        .value("RT_EXCEPTION_BUFFER_INDEX_OUT_OF_BOUNDS", RT_EXCEPTION_BUFFER_INDEX_OUT_OF_BOUNDS)
        .value("RT_EXCEPTION_INVALID_RAY", RT_EXCEPTION_INVALID_RAY)
        .value("RT_EXCEPTION_INTERNAL_ERROR", RT_EXCEPTION_INTERNAL_ERROR)
        .value("RT_EXCEPTION_USER", RT_EXCEPTION_USER)
        .value("RT_EXCEPTION_ALL", RT_EXCEPTION_ALL);

    boost::python::enum_<RTobjecttype>("RTobjecttype")
        .value("RT_OBJECTTYPE_UNKNOWN", RT_OBJECTTYPE_UNKNOWN)
        .value("RT_OBJECTTYPE_GROUP", RT_OBJECTTYPE_GROUP)
        .value("RT_OBJECTTYPE_GEOMETRY_GROUP", RT_OBJECTTYPE_GEOMETRY_GROUP)
        .value("RT_OBJECTTYPE_TRANSFORM", RT_OBJECTTYPE_TRANSFORM)
        .value("RT_OBJECTTYPE_SELECTOR", RT_OBJECTTYPE_SELECTOR)
        .value("RT_OBJECTTYPE_GEOMETRY_INSTANCE", RT_OBJECTTYPE_GEOMETRY_INSTANCE)
        .value("RT_OBJECTTYPE_BUFFER", RT_OBJECTTYPE_BUFFER)
        .value("RT_OBJECTTYPE_TEXTURE_SAMPLER", RT_OBJECTTYPE_TEXTURE_SAMPLER)
        .value("RT_OBJECTTYPE_OBJECT", RT_OBJECTTYPE_OBJECT)
        .value("RT_OBJECTTYPE_MATRIX_FLOAT2x2", RT_OBJECTTYPE_MATRIX_FLOAT2x2)
        .value("RT_OBJECTTYPE_MATRIX_FLOAT2x3", RT_OBJECTTYPE_MATRIX_FLOAT2x3)
        .value("RT_OBJECTTYPE_MATRIX_FLOAT2x4", RT_OBJECTTYPE_MATRIX_FLOAT2x4)
        .value("RT_OBJECTTYPE_MATRIX_FLOAT3x2", RT_OBJECTTYPE_MATRIX_FLOAT3x2)
        .value("RT_OBJECTTYPE_MATRIX_FLOAT3x3", RT_OBJECTTYPE_MATRIX_FLOAT3x3)
        .value("RT_OBJECTTYPE_MATRIX_FLOAT3x4", RT_OBJECTTYPE_MATRIX_FLOAT3x4)
        .value("RT_OBJECTTYPE_MATRIX_FLOAT4x2", RT_OBJECTTYPE_MATRIX_FLOAT4x2)
        .value("RT_OBJECTTYPE_MATRIX_FLOAT4x3", RT_OBJECTTYPE_MATRIX_FLOAT4x3)
        .value("RT_OBJECTTYPE_MATRIX_FLOAT4x4", RT_OBJECTTYPE_MATRIX_FLOAT4x4)
        .value("RT_OBJECTTYPE_FLOAT", RT_OBJECTTYPE_FLOAT)
        .value("RT_OBJECTTYPE_FLOAT2", RT_OBJECTTYPE_FLOAT2)
        .value("RT_OBJECTTYPE_FLOAT3", RT_OBJECTTYPE_FLOAT3)
        .value("RT_OBJECTTYPE_FLOAT4", RT_OBJECTTYPE_FLOAT4)
        .value("RT_OBJECTTYPE_INT", RT_OBJECTTYPE_INT)
        .value("RT_OBJECTTYPE_INT2", RT_OBJECTTYPE_INT2)
        .value("RT_OBJECTTYPE_INT3", RT_OBJECTTYPE_INT3)
        .value("RT_OBJECTTYPE_INT4", RT_OBJECTTYPE_INT4)
        .value("RT_OBJECTTYPE_UNSIGNED_INT", RT_OBJECTTYPE_UNSIGNED_INT)
        .value("RT_OBJECTTYPE_UNSIGNED_INT2", RT_OBJECTTYPE_UNSIGNED_INT2)
        .value("RT_OBJECTTYPE_UNSIGNED_INT3", RT_OBJECTTYPE_UNSIGNED_INT3)
        .value("RT_OBJECTTYPE_UNSIGNED_INT4", RT_OBJECTTYPE_UNSIGNED_INT4)
        .value("RT_OBJECTTYPE_USER", RT_OBJECTTYPE_USER)
        .value("RT_OBJECTTYPE_PROGRAM", RT_OBJECTTYPE_PROGRAM);


    /*
    *   NATIVES
    */
    boost::python::class_<optix::Acceleration>("_Acceleration", "_Acceleration docstring", boost::python::no_init);
    boost::python::class_<optix::Buffer>("_Buffer", "_Buffer docstring", boost::python::no_init);
    boost::python::class_<optix::Context>("_Context", "_Context docstring", boost::python::no_init);
    boost::python::class_<optix::Geometry>("_Geometry", "_Geometry docstring", boost::python::no_init);
    boost::python::class_<optix::GeometryGroup>("_GeometryGroup", "_GeometryGroup docstring", boost::python::no_init);
    boost::python::class_<optix::GeometryInstance>("_GeometryInstance", "_GeometryInstance docstring", boost::python::no_init);
    boost::python::class_<optix::Group>("_Group", "_Group docstring", boost::python::no_init);
    boost::python::class_<optix::Material>("_Material", "_Material docstring", boost::python::no_init);
    boost::python::class_<optix::Program>("_Program", "_Program docstring", boost::python::no_init);
    boost::python::class_<optix::Selector>("_Selector", "_Selector docstring", boost::python::no_init);
    boost::python::class_<optix::TextureSampler>("_TextureSampler", "_TextureSampler docstring", boost::python::no_init);
    boost::python::class_<optix::Transform>("_Transform", "_Transform docstring", boost::python::no_init);
    boost::python::class_<optix::Variable>("_Variable", "_Variable docstring", boost::python::no_init);
}
