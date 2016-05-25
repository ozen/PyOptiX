#pragma once
#include "shared_includes.h"


class NativeDestroyableWrapper
{
private:
    optix::DestroyableObj* object;
public:
    NativeDestroyableWrapper();
    ~NativeDestroyableWrapper();
    void set_destroyable_object(optix::DestroyableObj* object);
    void destroy();
    void validate();
    static void export_for_python();
};
