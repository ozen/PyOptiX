#pragma once
#include "shared_includes.h"
#include "acceleration.h"
#include "geometry_instance.h"
#include "scoped.h"
#include "destroyable.h"


class NativeGeometryGroupWrapper : public NativeDestroyableWrapper
{
private:
    optix::GeometryGroup geometry_group;

public:
    NativeGeometryGroupWrapper(optix::GeometryGroup geometry_group);
    ~NativeGeometryGroupWrapper();
    void set_acceleration(NativeAccelerationWrapper* acceleration);
    void set_child_count(unsigned int count);
    unsigned int get_child_count();
    void set_child_geometry_instance(unsigned int index, NativeGeometryInstanceWrapper* geometry_instance);
    void remove_child(unsigned int index);
    optix::GeometryGroup get_native();
    static void export_for_python();
};
