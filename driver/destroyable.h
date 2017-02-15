#pragma once
#include "shared_includes.h"


class NativeDestroyableWrapper
{
private:
    optix::DestroyableObj* object;
protected:
    bool is_destroyed;
    bool auto_destroy;
public:
    NativeDestroyableWrapper();
    ~NativeDestroyableWrapper();
    void set_destroyable_object(optix::DestroyableObj* object);
    void validate();
    void mark_destroyed();
    bool get_auto_destroy();
    void set_auto_destroy(bool destroy);
    static void boost_python_expose();
};
