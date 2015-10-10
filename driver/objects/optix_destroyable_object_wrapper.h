#ifndef OPTIX_DESTROYABLE_OBJECT_H
#define OPTIX_DESTROYABLE_OBJECT_H

#include "shared_includes.h"


class OptixDestroyableObject
{
private:
    optix::DestroyableObj* object;
public:
    OptixDestroyableObject();
    ~OptixDestroyableObject();

    void set_destroyable_object(optix::DestroyableObj* object);

    void destroy();
    void validate();

    static void export_for_python();
};

#endif
