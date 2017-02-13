#include "destroyable.h"


NativeDestroyableWrapper::NativeDestroyableWrapper() {
    is_destroyed = false;
    object = nullptr;
}

NativeDestroyableWrapper::~NativeDestroyableWrapper() {

}

void NativeDestroyableWrapper::set_destroyable_object(optix::DestroyableObj* object) {
    this->object = object;
}

void NativeDestroyableWrapper::validate() {
    object->validate();
}

void NativeDestroyableWrapper::mark_destroyed() {
    is_destroyed = true;
}

void NativeDestroyableWrapper::boost_python_expose() {
    boost::python::class_<NativeDestroyableWrapper >(
                "NativeDestroyableWrapper",
                "Wraps optix::Destroyable class",
                boost::python::no_init)

            .add_property("is_destroyed", &NativeDestroyableWrapper::is_destroyed)
            .def("validate", &NativeDestroyableWrapper::validate)
            .def("mark_destroyed", &NativeDestroyableWrapper::mark_destroyed);
}
