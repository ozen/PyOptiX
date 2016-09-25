#pragma once
#include "shared_includes.h"
#include "destroyable.h"

class NativeAccelerationWrapper: public NativeDestroyableWrapper
{
private:
    optix::Acceleration acceleration;

public:
    NativeAccelerationWrapper(optix::Acceleration acceleration);
    void set_property(std::string name, std::string value_name);
    void mark_dirty();
    bool is_dirty();
    optix::Acceleration get_native();
    static void export_for_python();
};
