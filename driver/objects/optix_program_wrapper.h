#ifndef OPTIX_PROGRAM_WRAPPER_H
#define OPTIX_PROGRAM_WRAPPER_H

#include "shared_includes.h"

#include "optix_scoped_object_wrapper.h"

class OptixProgramWrapper : public OptixScopedObjectWrapper
{
private:
    optix::Program program;

public:
    OptixProgramWrapper(optix::Program program);
    ~OptixProgramWrapper();

    optix::Variable get_assignable_variable(const std::string& variable_name);

    int get_id();
    optix::Program get_native_program();

    static void export_for_python();
};


#endif
