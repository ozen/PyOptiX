#pragma once
#include "shared_includes.h"


class NativeDestroyableWrapper
{
private:
    optix::DestroyableObj* object;
    bool is_destroyed;
public:
    NativeDestroyableWrapper();
    ~NativeDestroyableWrapper();
    void set_destroyable_object(optix::DestroyableObj* object);
    void destroy();
    void validate();
    void set_destroyed();
    static void export_for_python();
};
