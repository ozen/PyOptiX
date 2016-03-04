#include "Python.h"
#include <boost/python.hpp>
#include <boost/numpy.hpp>

#include "shared_includes.h"
#include "optix_destroyable_object_wrapper.h"
#include "optix_variable_wrapper.h"
#include "optix_scoped_object_wrapper.h"
#include "optix_program_wrapper.h"
#include "optix_acceleration_wrapper.h"
#include "optix_context_wrapper.h"
#include "optix_buffer_wrapper.h"
#include "optix_texture_sampler_wrapper.h"
#include "optix_geometry_wrapper.h"
#include "optix_material_wrapper.h"
#include "optix_selector_wrapper.h"
#include "optix_transform_wrapper.h"
#include "optix_geometry_group_wrapper.h"
#include "optix_group_wrapper.h"
#include "optix_geometry_instance_wrapper.h"


BOOST_PYTHON_MODULE(_driver)
{
    Py_Initialize();
    boost::numpy::initialize();
    namespace bp = boost::python;

    /*
    *   CORE
    */
    bp::scope().attr("OPTIX_VERSION") = OPTIX_VERSION;
    OptixDestroyableObject::export_for_python();
    OptixVariableWrapper::export_for_python();
    OptixScopedObjectWrapper::export_for_python();
    OptixProgramWrapper::export_for_python();
    OptixContextWrapper::export_for_python();
    OptixAccelerationWrapper::export_for_python();
    OptixBufferWrapper::export_for_python();
    OptixTextureSamplerWrapper::export_for_python();
    OptixGeometryWrapper::export_for_python();
    OptixMaterialWrapper::export_for_python();
    OptixSelectorWrapper::export_for_python();
    OptixTransformWrapper::export_for_python();
    OptixGeometryGroupWrapper::export_for_python();
    OptixGroupWrapper::export_for_python();
    OptixGeometryInstanceWrapper::export_for_python();

    /*
    *   ENUMs
    */
    //BUFFER
    bp::enum_<RTformat>("RTformat")
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

    bp::enum_<RTbuffertype>("RTbuffertype")
        .value("RT_BUFFER_INPUT", RT_BUFFER_INPUT)
        .value("RT_BUFFER_OUTPUT", RT_BUFFER_OUTPUT)
        .value("RT_BUFFER_INPUT_OUTPUT", RT_BUFFER_INPUT_OUTPUT);

    bp::enum_<RTbufferflag>("RTbufferflag")
        .value("RT_BUFFER_GPU_LOCAL", RT_BUFFER_GPU_LOCAL)
        .value("RT_BUFFER_COPY_ON_DIRTY", RT_BUFFER_COPY_ON_DIRTY);

    //TEXTURE
    bp::enum_<RTwrapmode>("RTwrapmode")
        .value("RT_WRAP_REPEAT", RT_WRAP_REPEAT)
        .value("RT_WRAP_CLAMP_TO_EDGE", RT_WRAP_CLAMP_TO_EDGE)
        .value("RT_WRAP_MIRROR", RT_WRAP_MIRROR)
        .value("RT_WRAP_CLAMP_TO_BORDER", RT_WRAP_CLAMP_TO_BORDER);

    bp::enum_<RTfiltermode>("RTfiltermode")
        .value("RT_FILTER_NEAREST", RT_FILTER_NEAREST)
        .value("RT_FILTER_LINEAR", RT_FILTER_LINEAR)
        .value("RT_FILTER_NONE", RT_FILTER_NONE);

    bp::enum_<RTtexturereadmode>("RTtexturereadmode")
        .value("RT_TEXTURE_READ_ELEMENT_TYPE", RT_TEXTURE_READ_ELEMENT_TYPE)
        .value("RT_TEXTURE_READ_NORMALIZED_FLOAT", RT_TEXTURE_READ_NORMALIZED_FLOAT);

    bp::enum_<RTtextureindexmode>("RTtextureindexmode")
        .value("RT_TEXTURE_INDEX_NORMALIZED_COORDINATES", RT_TEXTURE_INDEX_NORMALIZED_COORDINATES)
        .value("RT_TEXTURE_INDEX_ARRAY_INDEX", RT_TEXTURE_INDEX_ARRAY_INDEX);

    bp::enum_<RTexception>("RTexception")
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

    bp::enum_<RTobjecttype>("RTobjecttype")
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
    using namespace optix;
    bp::class_<Acceleration>("_Acceleration", "_Acceleration docstring", bp::no_init);
    bp::class_<Buffer>("_Buffer", "_Buffer docstring", bp::no_init);
    bp::class_<Context>("_Context", "_Context docstring", bp::no_init);
    bp::class_<Geometry>("_Geometry", "_Geometry docstring", bp::no_init);
    bp::class_<GeometryGroup>("_GeometryGroup", "_GeometryGroup docstring", bp::no_init);
    bp::class_<GeometryInstance>("_GeometryInstance", "_GeometryInstance docstring", bp::no_init);
    bp::class_<Group>("_Group", "_Group docstring", bp::no_init);
    bp::class_<Material>("_Material", "_Material docstring", bp::no_init);
    bp::class_<Program>("_Program", "_Program docstring", bp::no_init);
    bp::class_<Selector>("_Selector", "_Selector docstring", bp::no_init);
    bp::class_<TextureSampler>("_TextureSampler", "_TextureSampler docstring", bp::no_init);
    bp::class_<Transform>("_Transform", "_Transform docstring", bp::no_init);
    bp::class_<Variable>("_Variable", "_Variable docstring", bp::no_init);
}
