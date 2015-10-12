#ifndef OPTIX_SCOPED_OBJECT_WRAPPER_H
#define OPTIX_SCOPED_OBJECT_WRAPPER_H

#include "shared_includes.h"
#include "optix_variable_wrapper.h"
#include "optix_destroyable_object_wrapper.h"

class OptixScopedObjectWrapper: public OptixDestroyableObject
{
private:
    optix::ScopedObj* scoped_object;
protected:
    OptixScopedObjectWrapper();
    void set_scoped_object(optix::ScopedObj* scoped_object);

public:
    OptixVariableWrapper* query_variable(const std::string name);
    OptixVariableWrapper* declare_variable(const std::string name);
    OptixVariableWrapper* get_variable(int index);
    void remove_variable(OptixVariableWrapper* optix_variable_wrapper);
    unsigned int get_variable_count();

    static void export_for_python();
};


#endif
