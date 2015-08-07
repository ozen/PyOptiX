#include "optix_variable_wrapper.h"

#include "optix_buffer_wrapper.h"
#include "optix_texture_sampler_wrapper.h"
#include "optix_group_wrapper.h"
#include "optix_geometry_group_wrapper.h"
#include "optix_transform_wrapper.h"
#include "optix_selector_wrapper.h"


OptixVariableWrapper::OptixVariableWrapper(optix::Variable variable)
{
    this->variable = variable;
}

bool OptixVariableWrapper::is_valid()
{
    if( this->variable == 0)
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

optix::Variable OptixVariableWrapper::get_variable_native()
{
    return this->variable;
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


void OptixVariableWrapper::set_variable_with_type(const boost::numpy::ndarray& numpy_array, RTobjecttype object_type)
{
    void* ptr = numpy_array.get_data();

    switch(object_type)
    {
    case RT_OBJECTTYPE_FLOAT:                      /*!< Float Type               */
        this->variable->setFloat(((float*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_FLOAT2:                     /*!< Float2 Type               */
        this->variable->setFloat(((optix::float2*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_FLOAT3:                     /*!< Float3 Type               */
        this->variable->setFloat(((optix::float3*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_FLOAT4:                     /*!< Float4 Type               */
        this->variable->setFloat(((optix::float3*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_INT:                        /*!< Integer Type              */
        this->variable->setInt(((int*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_INT2:                       /*!< Integer2 Type             */
        this->variable->setInt(((optix::int2*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_INT3:                       /*!< Integer3 Type             */
        this->variable->setInt(((optix::int3*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_INT4:                       /*!< Integer4 Type             */
        this->variable->setInt(((optix::int4*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT:               /*!< Unsigned Integer Type     */
        this->variable->setUint(((unsigned int*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT2:              /*!< Unsigned Integer2 Type    */
        this->variable->setUint(((optix::uint2*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT3:              /*!< Unsigned Integer3 Type    */
        this->variable->setUint(((optix::uint3*)ptr)[0]);
        break;
    case RT_OBJECTTYPE_UNSIGNED_INT4:              /*!< Unsigned Integer4 Type    */
        this->variable->setUint(((optix::uint4*)ptr)[0]);
        break;
    default:
        std::cout<<"Can not assign variable"<<std::endl;
        throw "Merhaba Dunya";
    };

}


#include "optix_program_wrapper.h"
void OptixVariableWrapper::set_program_id_with_program(OptixProgramWrapper* program_wrapper)
{
    this->variable->setProgramId(program_wrapper->get_native_program());
}

#include "numpy_boost_helpers.h"
void OptixVariableWrapper::set_with_numpy_array1x1_dtype(const boost::numpy::ndarray& numpy_array1x1)
{
    long size_in_bytes = get_array_size_in_bytes(numpy_array1x1);
    this->variable->setUserData(size_in_bytes, numpy_array1x1.get_data());
}


// *********************************
// *********************************
// PYTHON SUPPORT
// *********************************
// *********************************

#include "Python.h"
#include <boost/python.hpp>
void OptixVariableWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixVariableWrapper>("_OptixVariableWrapper", "_OptixVariableWrapper docstring", bp::no_init)
            .def("is_valid", &OptixVariableWrapper::is_valid)
            .add_property("name", &OptixVariableWrapper::get_name)
            .add_property("annotation", &OptixVariableWrapper::get_annotation)
            .add_property("type", &OptixVariableWrapper::get_type)
            .add_property("nbytes", &OptixVariableWrapper::get_size_in_bytes)
            .def("_set_buffer", &OptixVariableWrapper::set_buffer)
            .def("_set_texture", &OptixVariableWrapper::set_texture)
            .def("_set_program_id_with_program", &OptixVariableWrapper::set_program_id_with_program)
            .def("_set_with_numpy_array1x1_dtype", &OptixVariableWrapper::set_with_numpy_array1x1_dtype)
            .def("_set_variable_with_type", &OptixVariableWrapper::set_variable_with_type)
            .def("_set_group", &OptixVariableWrapper::set_group)
            .def("_set_geometry_group", &OptixVariableWrapper::set_geometry_group)
            .def("_set_transform", &OptixVariableWrapper::set_transform)
            .def("_set_selector", &OptixVariableWrapper::set_selector);



}
