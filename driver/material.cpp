#include "material.h"


NativeMaterialWrapper::NativeMaterialWrapper(optix::Material material) {
    this->material = material;
    this->set_scoped_object(this->material.get());
}

NativeMaterialWrapper::~NativeMaterialWrapper() {
    if (!is_destroyed) {
        this->material->destroy();
        is_destroyed = true;
    }
}

void NativeMaterialWrapper::set_closest_hit_program(unsigned int ray_type_index, NativeProgramWrapper* program) {
    this->material->setClosestHitProgram(ray_type_index, program->get_native());
}

void NativeMaterialWrapper::set_any_hit_program(unsigned int ray_type_index, NativeProgramWrapper* program) {
    this->material->setAnyHitProgram(ray_type_index, program->get_native());
}

optix::Material NativeMaterialWrapper::get_native() {
    return this->material;
}

void NativeMaterialWrapper::boost_python_expose() {
    boost::python::class_<NativeMaterialWrapper, boost::python::bases<NativeScopedWrapper> >(
                "NativeMaterialWrapper",
                "Wraps optix::Material class",
                boost::python::no_init)

            .def("set_closest_hit_program", &NativeMaterialWrapper::set_closest_hit_program)
            .def("set_any_hit_program", &NativeMaterialWrapper::set_any_hit_program);
}
