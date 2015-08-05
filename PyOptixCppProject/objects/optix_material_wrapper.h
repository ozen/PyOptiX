#ifndef OPTIX_MATERIAL_WRAPPER_H
#define OPTIX_MATERIAL_WRAPPER_H

#include "optix_shared_includes.h"
#include "optix_program_wrapper.h"

#include "optix_scoped_object_wrapper.h"
class OptixMaterialWrapper : public OptixScopedObjectWrapper
{
private:
    optix::Material material;

public:
    OptixMaterialWrapper(optix::Material material);
    ~OptixMaterialWrapper();


    void set_closest_hit_program(unsigned int ray_type_index, OptixProgramWrapper*  program);
    void set_any_hit_program(unsigned int ray_type_index, OptixProgramWrapper*  program);


    optix::Material get_native();


    static void export_for_python();
};


#endif
