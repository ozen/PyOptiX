#include "optix_material_wrapper.h"
#include "Python.h"
#include <boost/python.hpp>

OptixMaterialWrapper::OptixMaterialWrapper(optix::Material material)
{
    this->material = material;
    this->set_scoped_object(this->material.get());
}

OptixMaterialWrapper::~OptixMaterialWrapper()
{
    std::cout<<"OptixMaterialWrapper deconstruction"<<std::endl;
    if(this->material.get() != 0)
        this->material->destroy();
}

void OptixMaterialWrapper::set_closest_hit_program(unsigned int ray_type_index, OptixProgramWrapper* program)
{
    this->material->setClosestHitProgram(ray_type_index, program->get_native_program());
}

void OptixMaterialWrapper::set_any_hit_program(unsigned int ray_type_index, OptixProgramWrapper* program)
{
    this->material->setAnyHitProgram(ray_type_index, program->get_native_program());
}

optix::Material OptixMaterialWrapper::get_native()
{
    return this->material;
}

void OptixMaterialWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixMaterialWrapper, bp::bases<OptixScopedObjectWrapper> >(
                "_OptixMaterialWrapper",
                "_OptixMaterialWrapper docstring",
                bp::init<optix::Material>())

            .def("_set_closest_hit_program", &OptixMaterialWrapper::set_closest_hit_program)
            .def("_set_any_hit_program", &OptixMaterialWrapper::set_any_hit_program);
}
