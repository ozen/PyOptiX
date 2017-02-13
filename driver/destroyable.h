#pragma once
#include "shared_includes.h"


class NativeDestroyableWrapper
{
private:
    optix::DestroyableObj* object;
protected:
    bool is_destroyed;
public:
    NativeDestroyableWrapper();
    void set_destroyable_object(optix::DestroyableObj* object);
    void validate();
    void set_destroyed();
    static void boost_python_expose();
};
