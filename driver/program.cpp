#include "program.h"


NativeProgramWrapper::NativeProgramWrapper(optix::Program program) {
    this->program = program;
    this->set_scoped_object(this->program.get());
}

NativeProgramWrapper::~NativeProgramWrapper() {
    if (!is_destroyed) {
        this->program->destroy();
        is_destroyed = true;
    }
}

int NativeProgramWrapper::get_id() {
    return this->program->getId();
}

optix::Program NativeProgramWrapper::get_native() {
    return this->program;
}

void NativeProgramWrapper::export_for_python() {
    boost::python::class_<NativeProgramWrapper, boost::python::bases<NativeScopedWrapper> >(
                "NativeProgramWrapper",
                "NativeProgramWrapper docstring",
                boost::python::init<optix::Program>())

            .def("get_id", &NativeProgramWrapper::get_id);
}
