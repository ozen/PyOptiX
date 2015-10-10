#include "optix_acceleration_wrapper.h"
#include <iostream>
#include "Python.h"
#include "boost/python.hpp"


OptixAccelerationWrapper::OptixAccelerationWrapper(optix::Acceleration acceleration)
{
    this->acceleration = acceleration;
    this->set_destroyable_object(this->acceleration.get());
}

OptixAccelerationWrapper::~OptixAccelerationWrapper()
{
    if(acceleration.get() != 0)
        this->acceleration->destroy();
}

void OptixAccelerationWrapper::set_property(std::string name, std::string value_name)
{
    this->acceleration->setProperty(name, value_name);
}

void OptixAccelerationWrapper::mark_dirty()
{
    this->acceleration->markDirty();
}


bool OptixAccelerationWrapper::is_dirty()
{
    return this->acceleration->isDirty();
}

optix::Acceleration OptixAccelerationWrapper::get_native()
{
    return acceleration;
}

void OptixAccelerationWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixAccelerationWrapper, bp::bases<OptixDestroyableObject> >(
                "_OptixAccelerationWrapper",
                "_OptixAcceleration docstring",
                bp::init<optix::Acceleration>())

            .def("_set_property", &OptixAccelerationWrapper::set_property)
            .def("mark_dirty", &OptixAccelerationWrapper::mark_dirty)
            .def("is_dirty", &OptixAccelerationWrapper::is_dirty);

}
