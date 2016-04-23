#include "destroyable.h"


NativeDestroyableWrapper::NativeDestroyableWrapper() {}

NativeDestroyableWrapper::~NativeDestroyableWrapper() {}

void NativeDestroyableWrapper::set_destroyable_object(optix::DestroyableObj* object) {
    this->object = object;
}

void NativeDestroyableWrapper::destroy() {
    object->destroy();
}
void NativeDestroyableWrapper::validate() {
    object->validate();
}

void NativeDestroyableWrapper::export_for_python() {
    boost::python::class_<NativeDestroyableWrapper >(
                "NativeDestroyableWrapper",
                "NativeDestroyableWrapper docstring",
                boost::python::no_init)

            .def("destroy", &NativeDestroyableWrapper::destroy)
            .def("validate", &NativeDestroyableWrapper::validate);
}
