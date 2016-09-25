#include "destroyable.h"


NativeDestroyableWrapper::NativeDestroyableWrapper() {
    isDestroyed = false;
}

NativeDestroyableWrapper::~NativeDestroyableWrapper() {
    if (!isDestroyed) {
        object->destroy();
    }
}

void NativeDestroyableWrapper::set_destroyable_object(optix::DestroyableObj* object) {
    this->object = object;
}

void NativeDestroyableWrapper::destroy() {
    if (!isDestroyed) {
        object->destroy();
        isDestroyed = true;
    }
}

void NativeDestroyableWrapper::validate() {
    object->validate();
}

void NativeDestroyableWrapper::set_destroyed() {
    isDestroyed = true;
}

void NativeDestroyableWrapper::export_for_python() {
    boost::python::class_<NativeDestroyableWrapper >(
                "NativeDestroyableWrapper",
                "NativeDestroyableWrapper docstring",
                boost::python::no_init)

            .def("_destroy", &NativeDestroyableWrapper::destroy)
            .def("validate", &NativeDestroyableWrapper::validate)
            .def("_set_destroyed", &NativeDestroyableWrapper::set_destroyed);
}
