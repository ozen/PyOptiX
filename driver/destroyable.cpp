#include "destroyable.h"


NativeDestroyableWrapper::NativeDestroyableWrapper() {
    is_destroyed = false;
}

void NativeDestroyableWrapper::set_destroyable_object(optix::DestroyableObj* object) {
    this->object = object;
}

void NativeDestroyableWrapper::validate() {
    object->validate();
}

void NativeDestroyableWrapper::set_destroyed() {
    is_destroyed = true;
}

void NativeDestroyableWrapper::boost_python_expose() {
    boost::python::class_<NativeDestroyableWrapper >(
                "NativeDestroyableWrapper",
                "Wraps optix::Destroyable class",
                boost::python::no_init)

            .def("validate", &NativeDestroyableWrapper::validate)
            .def("set_destroyed", &NativeDestroyableWrapper::set_destroyed);
}
