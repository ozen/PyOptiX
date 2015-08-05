#ifndef CORE_PACKAGE_H
#define CORE_PACKAGE_H

#include "Python.h"
#include <boost/python.hpp>
#include <boost/numpy.hpp>


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

void export_core_package()
{
    namespace bp = boost::python;

    bp::object core_module(bp::handle<>(bp::borrowed(PyImport_AddModule("PyOptixCpp.Core"))));
    bp::scope().attr("Core") = core_module;
    bp::scope core_scope = core_module;

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

}



#endif
