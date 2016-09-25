#pragma once
#include "shared_includes.h"
#include "acceleration.h"
#include "geometry_instance.h"
#include "transform.h"
#include "scoped.h"
#include "destroyable.h"

class NativeGeometryGroupWrapper;
class NativeSelectorWrapper;

class NativeGroupWrapper : public NativeDestroyableWrapper
{
private:
    optix::Group group;

public:
    NativeGroupWrapper(optix::Group group);
    void set_acceleration(NativeAccelerationWrapper* acceleration);
    void set_child_count(unsigned int count);
    unsigned int get_child_count();
    void set_child_geometry_group(unsigned int index, NativeGeometryGroupWrapper* child);
    void set_child_group(unsigned int index, NativeGroupWrapper* child);
    void set_child_selector(unsigned int index, NativeSelectorWrapper* child);
    void set_child_transform(unsigned int index, NativeTransformWrapper* child);
    void set_child_acceleration(unsigned int index, NativeAccelerationWrapper* child);
    void remove_child(unsigned int index);
    optix::Group get_native();
    static void export_for_python();
};
