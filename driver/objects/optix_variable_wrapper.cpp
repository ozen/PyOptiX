#include "optix_variable_wrapper.h"
#include "optix_buffer_wrapper.h"
#include "optix_texture_sampler_wrapper.h"
#include "optix_group_wrapper.h"
#include "optix_geometry_group_wrapper.h"
#include "optix_transform_wrapper.h"
#include "optix_selector_wrapper.h"
#include "optix_program_wrapper.h"
#include "numpy_boost_helpers.h"
#include "Python.h"
#include <boost/python.hpp>


OptixVariableWrapper::OptixVariableWrapper(optix::Variable variable)
{
    this->variable = variable;
}

OptixVariableWrapper::~OptixVariableWrapper()
{

}

bool OptixVariableWrapper::is_valid()
{
    if (this->variable == 0)
        return false;
    return true;
}

std::string OptixVariableWrapper::get_name()
{
    return this->variable->getName();
}

std::string OptixVariableWrapper::get_annotation()
{
    return this->variable->getAnnotation();
}

RTobjecttype OptixVariableWrapper::get_type()
{
    return this->variable->getType();
}

unsigned long OptixVariableWrapper::get_size_in_bytes()
{
    return this->variable->getSize();
}

void OptixVariableWrapper::set_buffer(OptixBufferWrapper* buffer_wrapper)
{
    this->variable->setBuffer(buffer_wrapper->get_native_buffer());
}

void OptixVariableWrapper::set_texture(OptixTextureSamplerWrapper* texture_wrapper)
{
    this->variable->setTextureSampler(texture_wrapper->get_native());
}

void OptixVariableWrapper::set_group(OptixGroupWrapper* group_wrapper)
{
    this->variable->set(group_wrapper->get_native());
}

void OptixVariableWrapper::set_geometry_group(OptixGeometryGroupWrapper* geometry_group_wrapper)
{
    this->variable->set(geometry_group_wrapper->get_native());
}

void OptixVariableWrapper::set_transform(OptixTransformWrapper* transform_wrapper)
{
    this->variable->set(transform_wrapper->get_native());
}

void OptixVariableWrapper::set_selector(OptixSelectorWrapper* selector_wrapper)
{
    this->variable->set(selector_wrapper->get_native());
}

void OptixVariableWrapper::set_program_id_with_program(OptixProgramWrapper* program_wrapper)
{
    this->variable->setProgramId(program_wrapper->get_native_program());
}

void OptixVariableWrapper::set_from_numpy_with_type(const boost::numpy::ndarray& numpy_array, RTobjecttype object_type)
{
    long size_in_bytes = get_array_size_in_bytes(numpy_array);
    void* ptr = numpy_array.get_data();

    switch(object_type)
    {
    case RT_OBJECTTYPE_FLOAT:
        this->variable->setFloat(((float*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_FLOAT2:
        this->variable->setFloat(((optix::float2*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_FLOAT3:
        this->variable->setFloat(((optix::float3*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_FLOAT4:
        this->variable->setFloat(((optix::float3*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_INT:
        this->variable->setInt(((int*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_INT2:
        this->variable->setInt(((optix::int2*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_INT3:
        this->variable->setInt(((optix::int3*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_INT4:
        this->variable->setInt(((optix::int4*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT:
        this->variable->setUint(((unsigned int*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT2:
        this->variable->setUint(((optix::uint2*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT3:
        this->variable->setUint(((optix::uint3*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT4:
        this->variable->setUint(((optix::uint4*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_USER:
        this->variable->setUserData(size_in_bytes, ptr);
        break;
    default:
        throw "Cannot assign variable";
    };
}

void OptixVariableWrapper::set_from_numpy(const boost::numpy::ndarray& numpy_array)
{
    long size_in_bytes = get_array_size_in_bytes(numpy_array);
    this->variable->setUserData(size_in_bytes, numpy_array.get_data());
}

optix::Variable OptixVariableWrapper::get_native()
{
    return variable;
}

void OptixVariableWrapper::export_for_python()
{
    boost::python::class_<OptixVariableWrapper>(
                "_OptixVariableWrapper",
                "_OptixVariableWrapper docstring",
                 boost::python::init<optix::Variable>())

            .add_property("name", &OptixVariableWrapper::get_name)
            .add_property("annotation", &OptixVariableWrapper::get_annotation)
            .add_property("type", &OptixVariableWrapper::get_type)
            .add_property("nbytes", &OptixVariableWrapper::get_size_in_bytes)
            .add_property("_native", &OptixVariableWrapper::get_native)
            .def("is_valid", &OptixVariableWrapper::is_valid)
            .def("_set_buffer", &OptixVariableWrapper::set_buffer)
            .def("_set_texture", &OptixVariableWrapper::set_texture)
            .def("_set_program_id_with_program", &OptixVariableWrapper::set_program_id_with_program)
            .def("_set_group", &OptixVariableWrapper::set_group)
            .def("_set_geometry_group", &OptixVariableWrapper::set_geometry_group)
            .def("_set_transform", &OptixVariableWrapper::set_transform)
            .def("_set_selector", &OptixVariableWrapper::set_selector)
            .def("_set_from_numpy", &OptixVariableWrapper::set_from_numpy)
            .def("_set_from_numpy_with_type", &OptixVariableWrapper::set_from_numpy_with_type);

}
