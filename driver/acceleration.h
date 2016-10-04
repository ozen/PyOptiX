#pragma once
#include "shared_includes.h"
#include "destroyable.h"

class NativeAccelerationWrapper: public NativeDestroyableWrapper
{
private:
    optix::Acceleration acceleration;

public:
    NativeAccelerationWrapper(optix::Acceleration acceleration);
    ~NativeAccelerationWrapper();
    void set_property(const std::string& name, const std::string& value);
    std::string get_property(const std::string& name);
    void mark_dirty();
    bool is_dirty();
    optix::Acceleration get_native();
    static void export_for_python();
};
