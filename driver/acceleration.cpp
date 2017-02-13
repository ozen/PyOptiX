#include "acceleration.h"


NativeAccelerationWrapper::NativeAccelerationWrapper(optix::Acceleration acceleration) {
    this->acceleration = acceleration;
    this->set_destroyable_object(this->acceleration.get());
}

NativeAccelerationWrapper::~NativeAccelerationWrapper() {
    if (!is_destroyed) {
        this->acceleration->destroy();
        is_destroyed = true;
    }
}

void NativeAccelerationWrapper::set_property(const std::string& name, const std::string& value) {
    this->acceleration->setProperty(name, value);
}

std::string NativeAccelerationWrapper::get_property(const std::string& name) {
    return this->acceleration->getProperty(name);
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

void NativeAccelerationWrapper::boost_python_expose() {
    boost::python::class_<NativeAccelerationWrapper, boost::python::bases<NativeDestroyableWrapper> >(
                "NativeAccelerationWrapper",
                "Wraps optix::Acceleration class",
                boost::python::no_init)

            .def("set_property", &NativeAccelerationWrapper::set_property)
            .def("get_property", &NativeAccelerationWrapper::get_property)
            .def("mark_dirty", &NativeAccelerationWrapper::mark_dirty)
            .def("is_dirty", &NativeAccelerationWrapper::is_dirty);
}
