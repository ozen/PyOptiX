#include "material.h"


NativeMaterialWrapper::NativeMaterialWrapper(optix::Material material) {
    this->material = material;
    this->set_scoped_object(this->material.get());
}

NativeMaterialWrapper::~NativeMaterialWrapper() {
    if(this->material.get() != 0) this->material->destroy();
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

void NativeMaterialWrapper::export_for_python() {
    boost::python::class_<NativeMaterialWrapper, boost::python::bases<NativeScopedWrapper> >(
                "NativeMaterialWrapper",
                "NativeMaterialWrapper docstring",
                boost::python::init<optix::Material>())

            .def("_set_closest_hit_program", &NativeMaterialWrapper::set_closest_hit_program)
            .def("_set_any_hit_program", &NativeMaterialWrapper::set_any_hit_program);
}
