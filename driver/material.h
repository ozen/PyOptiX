#pragma once
#include "shared_includes.h"
#include "program.h"
#include "scoped.h"

class NativeMaterialWrapper : public NativeScopedWrapper
{
private:
    optix::Material material;

public:
    NativeMaterialWrapper(optix::Material material);
    ~NativeMaterialWrapper();
    void set_closest_hit_program(unsigned int ray_type_index, NativeProgramWrapper* program);
    void set_any_hit_program(unsigned int ray_type_index, NativeProgramWrapper* program);
    optix::Material get_native();
    static void boost_python_expose();
};
