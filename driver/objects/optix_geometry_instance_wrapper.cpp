#include "optix_geometry_instance_wrapper.h"
#include "Python.h"
#include <boost/python.hpp>


OptixGeometryInstanceWrapper::OptixGeometryInstanceWrapper(optix::GeometryInstance geometry_instance)
{
    this->geometry_instance = geometry_instance;
    this->set_scoped_object(this->geometry_instance.get());
}

OptixGeometryInstanceWrapper::~OptixGeometryInstanceWrapper()
{
    if(this->geometry_instance.get() != 0)
        this->geometry_instance->destroy();
}

void OptixGeometryInstanceWrapper::set_geometry(OptixGeometryWrapper* geometry)
{
    return this->geometry_instance->setGeometry(geometry->get_native());
}

void OptixGeometryInstanceWrapper::set_material_count(unsigned int count)
{
    return this->geometry_instance->setMaterialCount(count);
}

unsigned int OptixGeometryInstanceWrapper::get_material_count()
{
    return this->geometry_instance->getMaterialCount();
}

void OptixGeometryInstanceWrapper::set_material(unsigned int idx, OptixMaterialWrapper* material)
{
    this->geometry_instance->setMaterial(idx, material->get_native());
}

optix::GeometryInstance OptixGeometryInstanceWrapper::get_native()
{
    return geometry_instance;
}

void OptixGeometryInstanceWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixGeometryInstanceWrapper, bp::bases<OptixScopedObjectWrapper> >(
                "_OptixGeometryInstanceWrapper",
                "_OptixGeometryInstanceWrapper docstring",
                bp::init<optix::GeometryInstance>())

            .def("set_geometry", &OptixGeometryInstanceWrapper::set_geometry)
            .def("set_material_count", &OptixGeometryInstanceWrapper::set_material_count)
            .def("get_material_count", &OptixGeometryInstanceWrapper::get_material_count)
            .def("set_material", &OptixGeometryInstanceWrapper::set_material);
}
