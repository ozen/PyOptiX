#include "acceleration.h"


NativeAccelerationWrapper::NativeAccelerationWrapper(optix::Acceleration acceleration) {
    this->acceleration = acceleration;
    this->set_destroyable_object(this->acceleration.get());
}

void NativeAccelerationWrapper::set_property(std::string name, std::string value_name) {
    this->acceleration->setProperty(name, value_name);
}

void NativeAccelerationWrapper::mark_dirty() {
    this->acceleration->markDirty();
}

bool NativeAccelerationWrapper::is_dirty() {
    return this->acceleration->isDirty();
}

optix::Acceleration NativeAccelerationWrapper::get_native() {
    return acceleration;
}

void NativeAccelerationWrapper::export_for_python() {
    boost::python::class_<NativeAccelerationWrapper, boost::python::bases<NativeDestroyableWrapper> >(
                "NativeAccelerationWrapper",
                "NativeAccelerationWrapper docstring",
                boost::python::init<optix::Acceleration>())

            .def("_set_property", &NativeAccelerationWrapper::set_property)
            .def("mark_dirty", &NativeAccelerationWrapper::mark_dirty)
            .def("is_dirty", &NativeAccelerationWrapper::is_dirty);
}
