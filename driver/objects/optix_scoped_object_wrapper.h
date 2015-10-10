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
    optix::Variable declare_variable(const std::string name);
    optix::Variable query_variable(const std::string name);
    optix::Variable get_variable(int index);
    void remove_variable(optix::Variable optix_variable_wrapper);
    unsigned int get_variable_count();

    static void export_for_python();
};


#endif
